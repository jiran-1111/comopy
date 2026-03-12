import os
import re
import sys
import importlib
import shutil
from pathlib import Path
from typing import Any, List, Dict, Optional, Union, Sequence, Mapping, TextIO

# ---------------- 正确导入 Cocotb 2.0.1 Runner ----------------
try:
    import cocotb
    from cocotb_tools.runner import Runner  # Cocotb 2.0.1 原生 Runner 抽象类
    from cocotb_tools.runner import get_abs_path, _Command, _ValueAndTag, _ValueAndOptionalTag
    from cocotb_tools.runner import VHDL, Verilog, VerilatorControlFile
    from cocotb_tools.runner import get_runner
    print(f"Cocotb版本: {cocotb.__version__} (适配2.0.1成功)")
    if cocotb.__version__ != "2.0.1":
        print(f"警告：当前Cocotb版本为{cocotb.__version__}，建议使用2.0.1版本")
except ImportError as e:
    raise ImportError(
        f"导入Cocotb 2.0.1 Runner失败: {e}\n"
        "请安装指定版本：pip install cocotb==2.0.1"
    )

# 导入comopy依赖（统一命名空间，避免冲突）
import comopy
import comopy.hdl as HDL
from comopy.hdl import IOStruct, Input, Output  # 直接导入，确保全局可用
from comopy_tools.Runner_base_test_case import RunnerBaseTestCase

# ---------------- ComoPy 核心实现（修复 IO 类型问题） ----------------
class ComoPy(Runner, RunnerBaseTestCase):
    """
    适配 Cocotb 2.0.1 的 Comopy 仿真器 Runner 实现
    修复：确保 self.io 是 IOStruct 子类实例
    """
    # 1. 定义支持的 GPI 接口（comopy 适配 python 语言）
    supported_gpi_interfaces = {"python": ["vpi"]}  # 仅为兼容Cocotb接口校验

    def __init__(self, *args, **kwargs):
        """初始化：兼容 Cocotb Runner 父类参数"""
        super().__init__(*args, **kwargs)  
        self._top_inst: Optional[HDL.RawModule] = None  
        self._io_instance: Optional[IOStruct] = None     
        self.top = None  
        self.io = None  # 确保类型为 IOStruct
        self.tv = []

    # ---------------- 实现 Runner 抽象方法 ----------------
    def _simulator_in_path(self) -> None:
        try:
            import comopy
        except ImportError:
            raise SystemExit("ERROR: comopy 仿真器未安装！请执行 pip install comopy")

    def _build_command(self) -> Sequence[_Command]:
        return []

    def _test_command(self) -> Sequence[_Command]:
        return []

    def _get_include_options(self, includes: Sequence[Path]) -> _Command:
        return [f"-I{include}" for include in includes]

    def _get_define_options(self, defines: Mapping[str, object]) -> _Command:
        return [f"-D{name}={value}" for name, value in defines.items()]

    def _get_parameter_options(self, parameters: Mapping[str, object]) -> _Command:
        return [f"-P{self.hdl_toplevel}.{name}={value}" for name, value in parameters.items()]

    # ---------------- 核心修复：build 方法（确保 IO 是 IOStruct 类型） ----------------
    def build(
        self,
        hdl_files: List[Union[str, Path]],
        toplevel: str,
        init: dict[str, Any] = {},
        **kwargs
    ) -> None:
        """
        重写 build 方法：修复 IO 类型问题，确保 self.io 是 IOStruct 子类实例
        """
        # 1. 基础参数校验
        if not isinstance(hdl_files, list):
            raise TypeError(f"hdl_files 必须是列表类型，当前类型：{type(hdl_files)}")
        if len(hdl_files) == 0:
            raise ValueError("hdl_files 列表不能为空")
        
        file_path_obj = Path(hdl_files[0]).resolve()
        if not file_path_obj.exists():
            raise FileNotFoundError(f"文件不存在：{file_path_obj}")
        if file_path_obj.is_dir():
            raise IsADirectoryError(f"路径是目录，不是文件：{file_path_obj}")
        file_path = str(file_path_obj)
        top_module_name = toplevel  

        # 2. 读取文件并解析端口定义
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        port_defs = self._parse_ports_from_text(file_content)
        if not port_defs:
            raise RuntimeError(f"在文件 {file_path} 中未解析到任何端口定义！")
        
        # 3. 生成IO类代码（关键修复：使用全局导入的 IOStruct，避免作用域问题）
        io_class = self._generate_io_class(port_defs)  # 直接返回IO类，而非代码字符串
        # 4. 验证IO类是否继承自 IOStruct
        if not issubclass(io_class, IOStruct):
            raise RuntimeError(f"生成的IO类未正确继承 IOStruct！当前父类：{io_class.__bases__}")
        
        # 5. 实例化IO并验证类型
        self.io = io_class()
        if not isinstance(self.io, IOStruct):
            raise RuntimeError(f"IO实例类型错误！期望 IOStruct，实际：{type(self.io)}")
        print(f"✅ IO实例类型验证通过：{type(self.io)} (继承自 {IOStruct})")

        # 6. 动态导入并实例化顶层模块
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        top_cls = getattr(module, top_module_name, None)
        if top_cls is None:
            raise RuntimeError(f"在文件 {file_path} 中找不到模块 {top_module_name}。")
        
        self.top = top_cls()  
        self.tv = [self.io]  # TV第一个元素必须是IOStruct实例
        self.top = self.simulate(self.top, self.tv, init)
        
        # 7. 模拟器验证
        if hasattr(self.top, 'simulator') and self.top.simulator is not None:
            sim_type = self.top.simulator.__class__.__name__
            print(f"✅ simulate后最终模拟器：{sim_type}")
        if self.top is None:
            print("仿真失败：self.top 为 None（simulate 方法未返回有效实例）")
        elif hasattr(self.top, 'simulator') and self.top.simulator is not None:
            print("仿真成功，返回了包含有效 simulator 属性的实例")
        else:
            print(f"仿真失败：返回的实例无有效 simulator 属性")
            print(f"  - 实例类型：{type(self.top)}")
            print(f"  - 是否有 simulator 属性：{hasattr(self.top, 'simulator')}")
            if hasattr(self.top, 'simulator'):
                print(f"  - simulator 属性值：{self.top.simulator}")

    def _parse_ports_from_text(self, file_content: str) -> dict:
        """解析端口定义（修复Python3.10转义警告）"""
        # 关键修复：用[.]替代\.，避免转义警告，同时不影响匹配
        pattern = r'(\w+)[.](\w+)\s*=\s*(Input|Output)[(](\d+)[)]'
        matches = re.findall(pattern, file_content)
        
        port_defs = {}
        for _, port_name, port_type, width in matches:
            port_defs[port_name] = (port_type, int(width))
        return port_defs
   
    def _generate_io_class(self, port_defs: dict) -> type:
        """
        核心修复：直接生成IO类（而非代码字符串），确保继承自IOStruct
        :return: 继承自 IOStruct 的 IO 类
        """
        # 定义IO类的属性字典
        io_attrs = {}
        for port_name, (port_type, width) in port_defs.items():
            # 直接创建 Input/Output 实例，绑定到类属性
            if port_type == "Input":
                io_attrs[port_name] = Input(width)
            elif port_type == "Output":
                io_attrs[port_name] = Output(width)
        
        # 动态创建IO类，显式继承自 IOStruct
        IO = type(
            'IO',  # 类名
            (IOStruct,),  # 父类（必须是IOStruct）
            io_attrs  # 类属性（端口定义）
        )
        # 设置类文档字符串
        IO.__doc__ = "自动生成的IOStruct子类（修复类型问题）"
        return IO

    # ---------------- 重写 Runner 方法 ----------------
    def _check_hdl_toplevel_lang(self, hdl_toplevel_lang: str | None) -> str:
        if hdl_toplevel_lang is None:
            return "python"
        if hdl_toplevel_lang not in self.supported_gpi_interfaces:
            raise ValueError(
                f"ComoPy 不支持 {hdl_toplevel_lang} 语言类型，仅支持 python"
            )
        return hdl_toplevel_lang

    def _execute(self, command: list[str], **kwargs: Any) -> None:
        pass

    def _set_env_build(self) -> None:
        self.env = os.environ.copy()

    def _set_env_test(self) -> None:
        self.env = os.environ.copy()
        self.env["COCOTB_TOPLEVEL"] = self.sim_hdl_toplevel if hasattr(self, 'sim_hdl_toplevel') else self.hdl_toplevel
        self.env["TOPLEVEL_LANG"] = "python"
