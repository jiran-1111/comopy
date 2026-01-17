# ComoPy: Co-modeling tools for hardware generation with Python
#
# Copyright (C) 2024-2025 Microprocessor R&D Center (MPRC), Peking University
# SPDX-License-Identifier: MIT
#
# Author: Chun Yang
#         Shixuan Chen

"""
Base class for test cases.
"""

from typing import Any

import comopy.hdl as HDL
from comopy.hdl import HDLStage
from comopy.ir import IRStage
from comopy.simulator import BaseSimulator, SimulatorStage
from comopy.translator import BaseTranslator, TranslatorStage
from comopy.utils import JobPipeline, match_lines


class BaseTestCase:

    """Base class for test cases."""

    def simulate(
        self, top: HDL.RawModule, tv: list, init: dict[str, Any] = {}
    ):
        # 空测试向量异常处理
        if not tv:
            raise RuntimeError(f"No TV for DUT module {top}.")
        # 获取测试向量的IO结构
        io = self.__get_tv_io(tv)

        pipeline = JobPipeline(HDLStage(), IRStage(), SimulatorStage())
        pipeline(top)

        # 端口一致性检查
        self.__check_module_io(top, io)
        # 初始化数据
        self.__init_data(top, init)
        # 运行仿真循环
        self.__run_ticks(top, io, tv)

    # 第0行为IO模版
    def __get_tv_io(self, tv: list) -> HDL.IOStruct:
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
    def __check_module_io(self, top: HDL.RawModule, io: HDL.IOStruct):
        if not io.match_module_io(top):
            io_cls = io.__class__.__name__
            raise RuntimeError(
                f"{io_cls}() at TV[0] doesn't match module {top}."
            )

    # 初始化寄存器
    def __init_data(self, top: HDL.RawModule, init: dict[str, Any]):
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

    def __run_ticks(self, top: HDL.RawModule, io: HDL.IOStruct, tv: list):
        sim = top.simulator
        # isinstance是检查某个东西是不是某个类型的
        assert isinstance(sim, BaseSimulator)
        # 启动仿真 推进时钟周期 组合逻辑重新计算 结束仿真 这里等价于timer readonlu nexttimestep
        sim.start()
        # 每一行测试向量 把输入信号送进电路
        for i, data in enumerate(tv[1:], 1):
            io.assign_inputs(top, data)
            # 等价于 dut.in,_value = data[0] GPI写信号
            assert isinstance(top, HDL.RawModule)
            if isinstance(top, HDL.Module):
                sim.tick()
            else:
                sim.evaluate()
            try:
                # 比对
                io.verify_outputs(top, data)
                # 等价于 assert dut.out_and.value == expected  GPI读信号
            except Exception as e:
                raise RuntimeError(f"{e} : TV[{i}] {data}")
        sim.stop()



    # 验证生成的verilgo是否符合预期  可用来生成sv代码
    def translate(self, top: HDL.RawModule, match: str):
        pipeline = JobPipeline(HDLStage(), IRStage(), TranslatorStage())
        pipeline(top)

        trans = top.translator
        assert isinstance(trans, BaseTranslator)
        sv = trans.emit()
        assert isinstance(sv, str)
        match_lines(sv, match)

