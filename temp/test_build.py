from typing import Any, Tuple
import importlib.util
import os

import comopy.hdl as HDL
from comopy.hdl import HDLStage, IOStruct
from comopy.ir import IRStage
from comopy.simulator import BaseSimulator, SimulatorStage
from cocotb_tools.runner import Runner, get_abs_path
from comopy.translator import BaseTranslator, TranslatorStage
from comopy.utils import JobPipeline, match_lines
import os
import sys
import logging
from pathlib import Path
from typing import Any, Mapping, Sequence
from pathlib import Path
import importlib
import os
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

# 先补全你提供的 RunnerBaseTestCase 完整代码（补充缺失的导入和定义）
class RunnerBaseTestCase:
    """Base class for test cases."""

    def simulate(
        self, top: HDL.RawModule, tv: list, init: dict[str, Any] = {}
    ) -> HDL.RawModule:
        # 空测试向量异常处理
        if not tv:
            raise RuntimeError(f"No TV for DUT module {top}.")
        # 获取测试向量的IO结构
        io = self._get_tv_io(tv)

        pipeline = JobPipeline(HDLStage(), IRStage(), SimulatorStage())
        pipeline(top)

        # 端口一致性检查
        self._check_module_io(top, io)
        # 初始化数据
        self._init_data(top, init)
        return top

    # 第0行为IO模版
    def _get_tv_io(self, tv: list) -> HDL.IOStruct:
        io = tv[0]
        if not isinstance(io, HDL.IOStruct):
            raise RuntimeError("No IOStruct at TV[0].")
        for i, data in enumerate(tv[1:], 1):
            # 检查输入数量与类型一致性
            if not io.match_data(data):
                io_cls = io.__class__.__name__
                raise RuntimeError(f"TV[{i}] doesn't match {io_cls}: {data}")
        return io

    # 比较电路端口 测试端口一致
    def _check_module_io(self, top: HDL.RawModule, io: HDL.IOStruct):
        if not io.match_module_io(top):
            io_cls = io.__class__.__name__
            raise RuntimeError(
                f"{io_cls}() at TV[0] doesn't match module {top}."
            )

    # 初始化寄存器
    def _init_data(self, top: HDL.RawModule, init: dict[str, Any]):
        root = top.node
        assert isinstance(root, HDL.CircuitNode)
        assert root.is_root
        for name, value in init.items():
            node = root.get_element(name)
            assert isinstance(node, HDL.CircuitNode)
            obj = node.obj
            assert isinstance(obj, HDL.SignalArray)
            # 把初始数据写入
            obj.read_mem(value)


# 核心实现：ComoPy 类
class ComoPy(Runner, RunnerBaseTestCase):
    """
    ComoPy 运行器，集成了模块构建、IO包装和仿真能力
    """
    def build(self, module_path: str, top_module_name: str) -> HDL.RawModule:
        """
        构建待测试模块的 RawModule 实例
        
        Args:
            module_path: 模块文件的绝对/相对路径（如 "model/adder.py"）
            top_module_name: 顶层模块类名（如 "Adder"）
        
        Returns:
            构建好的 RawModule 实例
        """
        # 1. 动态导入指定路径的模块文件
        top_module = self._import_module_from_path(module_path, top_module_name)
        
        # 2. 实例化顶层模块（如 Adder）
        dut_instance = top_module()
        
        # 3. 为模块构建 IO 结构（核心包装逻辑）
        self._build_module_io(dut_instance)
        
        # 4. 构建 RawModule 并返回
        raw_module = HDL.RawModule(dut_instance)
        
        # 可选：执行基础的 HDL 阶段处理，确保模块结构完整
        hdl_stage = HDLStage()
        hdl_stage(raw_module)
        
        return raw_module

    def _import_module_from_path(self, module_path: str, class_name: str):
        """
        从指定文件路径动态导入类
        
        Args:
            module_path: 模块文件路径
            class_name: 要导入的类名
        
        Returns:
            导入的类对象
        """
        # 检查文件是否存在
        if not os.path.exists(module_path):
            raise FileNotFoundError(f"模块文件不存在: {module_path}")
        
        # 构建模块规范
        spec = importlib.util.spec_from_file_location(
            f"dut_module_{class_name}",  # 模块名（自定义）
            module_path
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"无法加载模块: {module_path}")
        
        # 加载模块
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 获取指定类
        if not hasattr(module, class_name):
            raise AttributeError(f"模块 {module_path} 中未找到类 {class_name}")
        
        return getattr(module, class_name)

    def _build_module_io(self, module_instance):
        """
        为模块实例构建 IO 结构（核心包装逻辑）
        
        Args:
            module_instance: 顶层模块实例（如 Adder 实例）
        """
        # 检查模块是否已构建端口
        if not hasattr(module_instance, 'ports_built'):
            # 执行 ports 构建方法（对应 Adder 中的 @build 装饰器方法）
            if hasattr(module_instance, 'ports'):
                module_instance.ports()
                module_instance.ports_built = True  # 标记端口已构建
            else:
                raise RuntimeError(f"模块 {module_instance.__class__.__name__} 未定义 ports 方法")
        
        # 构建 IOStruct（映射模块的输入输出端口）
        io_struct = HDL.IOStruct()
        
        # 遍历模块的输入端口
        for attr_name, port in module_instance.__dict__.items():
            if isinstance(port, HDL.Input):
                io_struct.add_input(attr_name, port.width)
            elif isinstance(port, HDL.Output):
                io_struct.add_output(attr_name, port.width)
        
        # 将 IO 结构绑定到模块实例
        module_instance.io_struct = io_struct
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

# ------------------- 测试示例 -------------------
if __name__ == "__main__":
    # 初始化 ComoPy 运行器
    runner = ComoPy()
    
    # 构建 Adder 模块（替换为你的实际文件路径）
    adder_module = runner.build(
        module_path="model/adder.py",
        top_module_name="Adder"
    )
    
    # 准备测试向量（TV）：[IO结构, 测试数据1, 测试数据2, ...]
    test_vectors = [
        adder_module.io_struct,  # 第0行：IO模版
        {"A": 0b00000001, "B": 0b00000010, "X": 0b00000011},  # 1+2=3
        {"A": 0b00000100, "B": 0b00000101, "X": 0b00001001},  # 4+5=9
    ]
    
    # 执行仿真
    simulated_top = runner.simulate(
        top=adder_module,
        tv=test_vectors,
        init={}  # 无初始寄存器数据
    )
    
    print("模块仿真完成，顶层模块:", simulated_top)