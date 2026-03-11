import os
import sys
import logging
from pathlib import Path
from typing import Any, Mapping, Sequence
from pathlib import Path
import importlib
import os
from comopy.hdl import IOStruct, Input, Output
import comopy.hdl as HDL
from comopy.hdl import HDLStage
from comopy.ir import IRStage
from comopy.simulator import BaseSimulator, SimulatorStage
from comopy.translator import BaseTranslator, TranslatorStage
from comopy.utils import JobPipeline, match_lines
from cocotb_tools.runner import Runner, get_abs_path
from comopy_tools.Runner_base_test_case import RunnerBaseTestCase
import comopy.testcases.ex_HDLBits_features as ex
from comopy_tools.signal import ComoPySignal
from comopy_tools.dut import ComoPyDUT
from comopy_tools.trigger import ComoPyTimer
import asyncio
from cocotb.regression import RegressionManager

class ComoPy(Runner,RunnerBaseTestCase):
    def build(self, file_path: str, top_module_name: str, init: dict[str, Any] = {}):
        """
        构建待测试模块的 RawModule 实例
        
        Args:
            module_path: 模块文件的绝对/相对路径（如 "model/adder.py"）
            top_module_name: 顶层模块类名（如 "Adder"）
        
        Returns:
            构建好的 RawModule 实例
        """

        # 第一步：加载HDL模块文件
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"HDL文件 {file_path} 未找到。")
        
        # 动态导入模块
        module_name = os.path.splitext(os.path.basename(file_path))[0]  # 获取文件名（不带扩展名）
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 第二步：从加载的文件中获取顶层模块（例如 Adder 或其他模块）
        top = getattr(module, top_module_name, None)
        if top is None:
            raise RuntimeError(f"在文件 {file_path} 中找不到模块 {top_module_name}。")

        # 第三步：动态生成 IO 类
        io_class = self.generate_io_class(top)
        
        # 创建一个 IO 实例（可以直接作为测试用例）
        io = io_class()

        # 第四步：将顶层模块包装到 RunnerBaseTestCase 中进行仿真
        pipeline = JobPipeline(HDLStage(), IRStage(), SimulatorStage())
        pipeline(top)  # 处理模块

        # 执行端口一致性检查和初始化数据
        self._check_module_io(top, io)
        self._init_data(top, init)

        # 第五步：运行仿真（或返回模块以供进一步使用）
        return self.simulate(top, [io], init)

    
    def generate_io_class(seld,top: HDL.RawModule) -> type:
        """自动生成IOStruct类"""
    
        # 动态创建一个新的类，继承自IOStruct
        class DynamicIOStruct(IOStruct):
            pass
        
        # 遍历并动态地为DynamicIOStruct添加端口
        for name, port in vars(top).items():
            if isinstance(port, HDL.Signal):
                if port.direction == HDL.IODirection.In:
                    setattr(DynamicIOStruct, name, Input(port.nbits))
                elif port.direction == HDL.IODirection.Out:
                    setattr(DynamicIOStruct, name, Output(port.nbits))

        # 返回生成的IOStruct类
        return DynamicIOStruct

    def test(self, **kwargs):
        return []
    # --- 必须实现的抽象方法 (Abstract Methods) ---


    def _check_hdl_toplevel_lang(self, hdl_toplevel_lang):
        return "python"
    
    def _simulator_in_path(self) -> str:
        # 这个方法通常检查仿真器可执行文件是否存在。
        # 对于 ComoPy，我们直接返回一个虚拟路径或库名
        return "comopy"

    def _build_command(self) -> list[str]:
        # ComoPy 是在 Python 内部 build 的，不需要外部 shell 命令
        return []

    def _test_command(self) -> list[str]:
        # 同理，测试也不需要外部命令行驱动
        return []

    def _get_include_options(self, includes: Sequence[Path]) -> list[str]:
        return []

    def _get_define_options(self, defines: Mapping[str, Any]) -> list[str]:
        return []

    def _get_parameter_options(self, parameters: Mapping[str, Any]) -> list[str]:
        return []

    # 另外建议重写这个方法，防止父类去执行空的命令导致报错
    def _execute(self, command: list[str], **kwargs: Any) -> None:
        if not command:
            return 
        super()._execute(command, **kwargs)