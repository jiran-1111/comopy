from __future__ import annotations
import cocotb
from cocotb.triggers import Timer
import comopy_tools  
from cocotb_tools.runner import get_runner
import os
import sys
from pathlib import Path

@cocotb.test()
async def test_Gates100(dut):
    await Timer(1, units='step')

    vectors = [
        (0, 0, 0, 0),
        (2882400254, 0, 1, 0),
        (4294967295, 0, 1, 0),
        (4581298449, 0, 1, 1),
    ]

    for vec in vectors:
        dut.in_.value = vec[0]
        await Timer(1, units='step')
        assert dut.out_and.value == vec[1]
        assert dut.out_or.value == vec[2]
        assert dut.out_xor.value == vec[3]

def run_test():
    runner = get_runner("comopy")
    runner.build(
        sources=[Path(__file__).parent / "model_Gates100.py"], # 指向硬件定义
        hdl_toplevel="Gates100", # 指向硬件类名
    )
    runner.test(
        hdl_toplevel="Gates100",
        hdl_toplevel_lang="verilog",
        test_module="cocotb_Gates100"
    )

if __name__ == "__main__":
    run_test()
