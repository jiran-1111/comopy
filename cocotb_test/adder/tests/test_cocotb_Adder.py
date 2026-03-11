# tests/test_cocotb_Adder.py
from __future__ import annotations

import os
import random
import sys
from pathlib import Path
import comopy_tools  
import cocotb
from cocotb.triggers import Timer
from cocotb_tools.runner import get_runner


# 加法器的基本测试
@cocotb.test()
async def adder_basic_test(dut):
    """Test for 5 + 10 == 15"""

    A = 5
    B = 10

    dut.A.value = A
    dut.B.value = B

    await Timer(2, unit="ns")

    assert dut.X.value == A + B, (
        f"Adder result is incorrect: {dut.X.value} != 15"
    )

# pytest入口 启动仿真
def test_adder_runner():

    runner = get_runner("comopy")
    runner.build(
        sources=[Path(__file__).parent.parent / "model" / "adder.py"], # 指向硬件定义
        hdl_toplevel="Adder", # 指向硬件类名
    )
    runner.test(
        hdl_toplevel="Adder",
        hdl_toplevel_lang="verilog",
        test_module="test_cocotb_Adder"
    )
if __name__ == "__main__":
    test_adder_runner()
