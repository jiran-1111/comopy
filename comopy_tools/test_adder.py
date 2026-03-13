# test_adder.py
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))

import cocotb
from adapter import RisingEdge

# ==========================================
# ✅ 测试函数必须写在顶层！不能写在 main 里面！
# ==========================================

async def test_adder(dut):
    dut.A.value = 5
    dut.B.value = 10

    await RisingEdge(dut.A)

    # 错误：assert dut.C.value == 15
    # 正确：输出叫 X！！！
    assert dut.X.value == 15
    print("✅ 测试成功！5 + 10 = 15！！！")

if __name__ == "__main__":
    import comopy_tools
    from cocotb_tools.runner import get_runner

    runner = get_runner("comopy")
    adder_path = [str(Path(__file__).parent / "debug" / "model" / "adder.py")]
    
    try:
        runner.build(
            hdl_files=adder_path,
            toplevel="Adder"
        )
        
        # ✅ 这里必须写模块名：test_adder（无 .py）
        runner.test(test_func=test_adder)

    except Exception as e:
        print(f"运行失败：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)