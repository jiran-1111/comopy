
from typing import Any

import comopy.hdl as HDL
from comopy.hdl import HDLStage
from comopy.ir import IRStage
from comopy.simulator import BaseSimulator, SimulatorStage
from comopy.translator import BaseTranslator, TranslatorStage
from comopy.utils import JobPipeline, match_lines


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

    

