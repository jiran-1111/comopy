import os
import re
import sys
import asyncio
import importlib
import shutil
from pathlib import Path
from typing import Any, List, Dict, Optional, Union, Sequence, Mapping, TextIO

# 导入仿真适配器核心类
from adapter import ComopyDUT, RisingEdge, ComopySignal
# 导入仿真器基础类型
from comopy.simulator import BaseSimulator, SimulatorStage

# ---------------- 导入并校验 Cocotb 2.0.1 ----------------
try:
    import cocotb
    from cocotb_tools.runner import Runner
    from cocotb_tools.runner import get_abs_path, _Command, _ValueAndTag, _ValueAndOptionalTag
    from cocotb_tools.runner import VHDL, Verilog, VerilatorControlFile
    from cocotb_tools.runner import get_runner
    print(f"Cocotb版本: {cocotb.__version__} (适配2.0.1成功)")
    
    # 版本警告
    if cocotb.__version__ != "2.0.1":
        print(f"警告：当前Cocotb版本为{cocotb.__version__}，建议使用2.0.1版本")
except ImportError as e:
    raise ImportError(
        f"导入Cocotb 2.0.1 Runner失败: {e}\n"
        "请安装指定版本：pip install cocotb==2.0.1"
    )

# ---------------- 导入 CoMopy 硬件描述依赖 ----------------
import comopy
import comopy.hdl as HDL
from comopy.hdl import IOStruct, Input, Output
from comopy_tools.runner_base_test_case import RunnerBaseTestCase

# ---------------- ComoPy 仿真核心类 ----------------
class ComoPy(Runner, RunnerBaseTestCase):
    """
    适配 Cocotb 2.0.1 的 CoMopy 仿真运行器
    功能：编译Python版HDL → 自动生成IO端口 → 运行仿真测试
    """
    # 声明支持的接口（用于Cocotb兼容）
    supported_gpi_interfaces = {"python": ["vpi"]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._top_inst: Optional[HDL.RawModule] = None  # 顶层硬件模块
        self._io_instance: Optional[IOStruct] = None     # IO端口实例
        self.top = None    # 顶层模块对象
        self.io = None     # IO端口对象（IOStruct类型）
        self.dut = None    # 测试设备适配器
        self.tv = []       # 仿真事务列表

    # ---------------- Cocotb Runner 抽象方法实现 ----------------
    def _simulator_in_path(self) -> None:
        """检查CoMopy是否安装"""
        try:
            import comopy
        except ImportError:
            raise SystemExit("ERROR: comopy 未安装！执行：pip install comopy")

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

    # ---------------- 核心：编译硬件文件 ----------------
    def build(
        self,
        hdl_files: List[Union[str, Path]],
        toplevel: str,
        init: dict[str, Any] = {},
        **kwargs
    ) -> None:
        """
        新版：不再自动解析端口！
        直接使用 adder.py 里你手写的 IO 类！
        """
        # 基础检查
        if not isinstance(hdl_files, list) or len(hdl_files) == 0:
            raise ValueError("hdl_files 必须是非空列表")
        
        file_path_obj = Path(hdl_files[0]).resolve()
        if not file_path_obj.exists():
            raise FileNotFoundError(f"文件不存在：{file_path_obj}")

        file_path = str(file_path_obj)
        top_module_name = toplevel

        # 动态导入硬件文件（adder.py）
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 拿到顶层模块 Adder
        top_cls = getattr(module, top_module_name, None)
        if top_cls is None:
            raise RuntimeError(f"找不到模块 {top_module_name}")
        
        IOClass = module.IO

        # 创建 IO 实例
        self.io = IOClass()

        # 实例化硬件
        self.top = top_cls()
        self.tv = [self.io]
        self.top = self.simulate(self.top, self.tv, init)

        # 创建 DUT
        self.dut = ComopyDUT(self)

        # 状态输出
        if hasattr(self.top, 'simulator'):
            print(f"最终模拟器：{self.top.simulator.__class__.__name__}")
    # ---------------- 运行测试 ----------------

    
    def test(self, test_module):
        import importlib
        import inspect

        sim = self.top.simulator
        sim.start()

        # 导入测试文件
        mod = importlib.import_module(test_module)

        # 自动找出所有 @cocotb.test() （安全，永不循环导入）
        tests = []
        for name, member in inspect.getmembers(mod):
            if inspect.iscoroutinefunction(member):
                # 识别 cocotb 测试用例
                if hasattr(member, "_decorated") and member._decorated == "test":
                    tests.append(member)

        # 批量运行
        for t in tests:
            print(f"\n运行测试: {t.__name__}")
            asyncio.run(t(self.dut))

        sim.stop()
        print("\n全部测试完成！")
    

    """
    # ---------------- 从代码文本解析端口 ----------------
    def _parse_ports_from_text(self, file_content: str) -> dict:
        #正则匹配：A.Input(8)  B.Output(16) 这类端口定义
        pattern = r'(\w+)[.](\w+)\s*=\s*(Input|Output)[(](\d+)[)]'
        matches = re.findall(pattern, file_content)
        
        port_defs = {}
        for _, port_name, port_type, width in matches:
            port_defs[port_name] = (port_type, int(width))
        return port_defs

    # ---------------- 动态生成 IO 类 ----------------
    def _generate_io_class(self, port_defs: dict) -> type:
        io_attrs = {}
        for port_name, (port_type, width) in port_defs.items():
            if port_type == "Input":
                io_attrs[port_name] = Input(width)
            elif port_type == "Output":
                io_attrs[port_name] = Output(width)
        
        # 动态创建类
        IO = type('IO', (IOStruct,), io_attrs)
        IO.__doc__ = "自动生成的IOStruct子类"
        return IO
    """

    # ---------------- 语言类型检查 ----------------
    def _check_hdl_toplevel_lang(self, hdl_toplevel_lang: str | None) -> str:
        if hdl_toplevel_lang is None:
            return "python"
        if hdl_toplevel_lang not in self.supported_gpi_interfaces:
            raise ValueError(f"ComoPy 仅支持 python 语言")
        return hdl_toplevel_lang

    # ---------------- 执行命令与环境变量 ----------------
    def _execute(self, command: list[str], **kwargs: Any) -> None:
        pass

    def _set_env_build(self) -> None:
        self.env = os.environ.copy()

    def _set_env_test(self) -> None:
        self.env = os.environ.copy()
        self.env["COCOTB_TOPLEVEL"] = self.sim_hdl_toplevel if hasattr(self, 'sim_hdl_toplevel') else self.hdl_toplevel
        self.env["TOPLEVEL_LANG"] = "python"