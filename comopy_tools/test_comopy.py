# test_comopy.py
from pathlib import Path
import sys
# 将项目根目录加入 Python 路径（确保能导入 comopy_tools）
sys.path.append(str(Path(__file__).parent))

# 导入 comopy_tools → 触发 __init__.py 执行，覆盖 get_runner
import comopy_tools
from cocotb_tools.runner import get_runner

if __name__ == "__main__":
    # 此时 get_runner 已被覆盖，能识别 comopy
    runner = get_runner("comopy")
    adder_path = [str(Path(__file__).parent  / "debug" / "model" / "adder.py")]
    
    try:
        runner.build(
            hdl_files=adder_path,
            toplevel="Adder"
        )
    except Exception as e:
        print(f"运行失败：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)