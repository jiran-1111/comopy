# 使用comopy仿真器测试
"""
所以本质上这个文件是可以不用的
只需要一个adder.py作为model即可

cocotb方面的测试样例放在tests文件夹下，表明model的文件位置即可

"""
import comopy.testcases.ex_HDLBits_conn as ex_conn   # 如果也要测连续赋值风格，但这里只测 Adder
from comopy.hdl import Input, IOStruct, Output
from comopy.testcases.base_test_case import BaseTestCase

import cocotb_test.adder.model.adder as adder   # 导入我们要测试的 Adder 模块

class TestAdder(BaseTestCase):
    class IO(IOStruct):
        A = Input(8)
        B = Input(8)
        X = Output(8)

    # 测试向量：每个元组对应 (A, B, 预期X)
    TV = [
        IO(),                # 默认值（通常为0）
        (5, 10, 15),         # 5 + 10 = 15
        (0, 0, 0),
        (255, 1, 0),         # 8位溢出：255+1=256 → 0（因为输出只有8位）
        (127, 127, 254),
        (0xAA, 0x55, 0xFF),  # 0xAA + 0x55 = 0xFF
    ]

    def test_adder(self):
        self.simulate(adder.Adder(), self.TV)
