from pathlib import Path
import sys
import traceback  # 必加！

sys.path.append(str(Path(__file__).parent.parent))

import cocotb
from comopy_tools.adapter import RisingEdge

# 测试用例1
@cocotb.test()
async def test_adder_1(dut):
    dut.A.value = 5
    dut.B.value = 10
    await RisingEdge(dut.A)
    assert dut.X.value == 15
    print("✅ 测试1：5 + 10 = 15 成功")

# 测试用例2
@cocotb.test()
async def test_adder_2(dut):
    dut.A.value = 0
    dut.B.value = 0
    await RisingEdge(dut.A)
    assert dut.X.value == 0
    print("✅ 测试2：0 + 0 = 0 成功")

if __name__ == "__main__":
    from cocotb_tools.runner import get_runner

    runner = get_runner("comopy")
    adder_path = [str(Path(__file__).parent / "adder.py")]
    
    try:
        runner.build(
            hdl_files=adder_path,
            toplevel="Adder"
        )

        # ✅ 完全对齐
        runner.test(test_module="test_new_adder")

    except Exception as e:
        print(f"运行失败：{type(e).__name__}: {e}")
        traceback.print_exc()
        sys.exit(1)