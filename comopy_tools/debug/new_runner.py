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

# 导入comopy依赖
import comopy.hdl as HDL
from comopy.hdl import IOStruct, Input, Output
from comopy_tools.Runner_base_test_case import RunnerBaseTestCase

# ---------------- ComoPy 核心实现（继承 Cocotb 2.0.1 Runner） ----------------
class ComoPy(Runner, RunnerBaseTestCase):
    """
    适配 Cocotb 2.0.1 的 Comopy 仿真器 Runner 实现
    遵循 Runner 抽象类规范，实现所有抽象方法
    """
    # 1. 定义支持的 GPI 接口（comopy 适配 python 语言）
    supported_gpi_interfaces = {"python": ["vpi"]}  # 自定义 python 语言类型

    def __init__(self, *args, **kwargs):
        """初始化：兼容 Cocotb Runner 父类参数"""
        super().__init__(*args, **kwargs)  # 必须先调用父类初始化
        self._top_inst: Optional[HDL.RawModule] = None  # comopy顶层模块
        self._io_instance: Optional[IOStruct] = None     # 自动生成的IO实例
        self.top = None  # 兼容你原有代码的实例属性
        self.io = None
        self.tv = []

    # ---------------- 实现 Runner 抽象方法 ----------------
    def _simulator_in_path(self) -> None:
        """检查 comopy 仿真器是否存在（自定义逻辑）"""
        # 此处替换为 comopy 仿真器的存在性检查逻辑
        try:
            import comopy  # 检查 comopy 是否安装
        except ImportError:
            raise SystemExit("ERROR: comopy 仿真器未安装！请执行 pip install comopy")

    def _build_command(self) -> Sequence[_Command]:
        """
        实现父类抽象方法：生成构建命令
        Comopy 为纯 Python 仿真，无需外部构建命令，返回空列表
        """
        return []

    def _test_command(self) -> Sequence[_Command]:
        """
        实现父类抽象方法：生成测试命令
        Comopy 为纯 Python 仿真，无需外部测试命令，返回空列表
        """
        return []

    def _get_include_options(self, includes: Sequence[Path]) -> _Command:
        """实现父类抽象方法：返回仿真器特定的 include 选项"""
        return [f"-I{include}" for include in includes]

    def _get_define_options(self, defines: Mapping[str, object]) -> _Command:
        """实现父类抽象方法：返回仿真器特定的 define 选项"""
        return [f"-D{name}={value}" for name, value in defines.items()]

    def _get_parameter_options(self, parameters: Mapping[str, object]) -> _Command:
        """实现父类抽象方法：返回仿真器特定的 parameter 选项"""
        return [f"-P{self.hdl_toplevel}.{name}={value}" for name, value in parameters.items()]

    # ---------------- 重写 Runner 核心方法（适配 comopy 逻辑） ----------------
    def build(
        self,
        hdl_files: List[Union[str, Path]],  # Cocotb 2.0.1 标准参数
        toplevel: str,
        init: dict[str, Any] = {},
        **kwargs
    ) -> None:
        """
        重写 build 方法：集成 comopy 模块解析和实例化逻辑
        完全兼容 Cocotb 2.0.1 build 方法参数规范
        """
        if not isinstance(hdl_files, list):
            raise TypeError(f"hdl_files 必须是列表类型，当前类型：{type(hdl_files)}")
        if len(hdl_files) == 0:
            raise ValueError("hdl_files 列表不能为空")
        
        # 关键修复2：取列表第一个元素作为文件路径
        file_path = hdl_files[0]
        # 转为 Path 对象并校验有效性
        file_path_obj = Path(file_path).resolve()
        if not file_path_obj.exists():
            raise FileNotFoundError(f"文件不存在：{file_path_obj}")
        if file_path_obj.is_dir():
            raise IsADirectoryError(f"路径是目录，不是文件：{file_path_obj}")
        file_path = str(file_path_obj)
        top_module_name = toplevel  


        
        # 读取文件内容并解析端口定义
        #print(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        port_defs = self._parse_ports_from_text(file_content)
        if not port_defs:
            raise RuntimeError(f"在文件 {file_path} 中未解析到任何端口定义！")
        
        # 生成IO类代码并动态创建IO类
        io_class_code = self._generate_io_class_code(port_defs)
        loc = {}
        exec(io_class_code, globals(), loc)
        IO = loc['IO']

        # 动态导入模块并实例化顶层模块
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        top_cls = getattr(module, top_module_name, None)
        if top_cls is None:
            raise RuntimeError(f"在文件 {file_path} 中找不到模块 {top_module_name}。")
        
        self.top = top_cls()  # 实例属性
        self.io = IO()
        self.tv = [self.io]
        self.top = self.simulate(self.top, self.tv, init)
        
        if self.top is None:
            print("仿真失败：self.top 为 None（simulate 方法未返回有效实例）")
        elif hasattr(self.top, 'simulator') and self.top.simulator is not None:
            print("仿真成功，返回了包含有效 simulator 属性的实例")
        else:
            # 打印调试信息
            print(f"仿真失败：返回的实例无有效 simulator 属性")
            print(f"  - 实例类型：{type(self.top)}")
            print(f"  - 是否有 simulator 属性：{hasattr(self.top, 'simulator')}")
            if hasattr(self.top, 'simulator'):
                print(f"  - simulator 属性值：{self.top.simulator}")

    # ---------------- 自定义辅助方法（保留原有逻辑） ----------------
    def _parse_ports_from_text(self, file_content: str) -> dict:
        """正则匹配解析端口定义"""
        pattern = r's\.(\w+)\s*=\s*(Input|Output)\((\d+)\)'
        matches = re.findall(pattern, file_content)
        
        port_defs = {}
        for port_name, port_type, width in matches:
            port_defs[port_name] = (port_type, int(width))
        return port_defs

    def _generate_io_class_code(self, port_defs: dict) -> str:
        """根据端口定义生成IO类代码字符串"""
        code_lines = [
            "from comopy.hdl import IOStruct, Input, Output",
            "",
            "class IO(IOStruct):",
            "    \"\"\"自动生成的IOStruct类\"\"\""
        ]
        for port_name, (port_type, width) in port_defs.items():
            code_lines.append(f"    {port_name} = {port_type}({width})")
        
        return '\n'.join(code_lines)

    # ---------------- 重写 Runner 钩子方法（避免父类报错） ----------------
    def _check_hdl_toplevel_lang(self, hdl_toplevel_lang: str | None) -> str:
        """重写：适配 comopy 的 python 语言类型"""
        if hdl_toplevel_lang is None:
            return "python"
        if hdl_toplevel_lang not in self.supported_gpi_interfaces:
            raise ValueError(
                f"ComoPy 不支持 {hdl_toplevel_lang} 语言类型，仅支持 python"
            )
        return hdl_toplevel_lang

    def _execute(self, command: list[str], **kwargs: Any) -> None:
        """重写：禁用外部命令执行（comopy 纯 Python 仿真）"""
        pass

    def _set_env_build(self) -> None:
        """重写：自定义 comopy 构建环境变量"""
        self.env = os.environ.copy()
        # 可添加 comopy 所需的环境变量

    def _set_env_test(self) -> None:
        """重写：自定义 comopy 测试环境变量"""
        self.env = os.environ.copy()
        self.env["COCOTB_TOPLEVEL"] = self.sim_hdl_toplevel if hasattr(self, 'sim_hdl_toplevel') else self.hdl_toplevel
        self.env["TOPLEVEL_LANG"] = "python"

# ---------------- 适配 Cocotb 2.0.1 get_runner 方法 ----------------
"""
def get_runner(simulator_name: str) -> Runner:
    
    扩展 Cocotb 2.0.1 get_runner：添加 comopy 仿真器支持
    
    # 先导入 Cocotb 原生 get_runner
    from cocotb_tools.runner import get_runner as _cocotb_get_runner

    # 自定义仿真器映射
    custom_sims = {
        "comopy": ComoPy,
    }

    # 优先处理自定义仿真器
    if simulator_name.lower() in custom_sims:
        return custom_sims[simulator_name.lower()]()
    # 其他仿真器使用 Cocotb 原生实现
    return _cocotb_get_runner(simulator_name)
"""
# ---------------- 测试示例（Cocotb 2.0.1 标准调用方式） ----------------
if __name__ == "__main__":
    # 1. 获取 ComoPy Runner 实例
    runner = get_runner("comopy")
    adder_path = [str(Path(__file__).parent /"model" / "adder.py")]
    
    try:
        runner.build(
            hdl_files=adder_path,  # 必须传入列表
            toplevel="Adder"
        )
    except Exception as e:
        print(f"运行失败：{type(e).__name__}: {e}")
        # 打印详细的错误堆栈（方便调试）
        import traceback
        traceback.print_exc()
        sys.exit(1)
    


