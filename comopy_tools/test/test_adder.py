from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

import cocotb
from comopy_tools.adapter import RisingEdge

@cocotb.test()
async def test_adder(dut):
    # cocotb的测试脚本的引脚定义需要完全和 hdl module 一致
    dut.A.value = 5
    dut.B.value = 10

    await RisingEdge(dut.A)
   
    assert dut.X.value == 15
    print("测试成功！5 + 10 = 15")

if __name__ == "__main__":
    import comopy_tools
    from cocotb_tools.runner import get_runner

    runner = get_runner("comopy")
    adder_path = [str(Path(__file__).parent /  "adder.py")]
    
    try:
        runner.build(
            hdl_files=adder_path,
            toplevel="Adder"
        )
        
        runner.test(test_module = "test_adder")

    except Exception as e:
        print(f"运行失败：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)