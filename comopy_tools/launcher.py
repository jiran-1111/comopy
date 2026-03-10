"""
这是核心的衔接点。当 Runner 启动子进程时，这个脚本会运行。
它负责实例化 ComoPy 的硬件模型，并告诉 cocotb：“这就是你的 DUT，请开始测试”。
"""
import argparse
import cocotb
from cocotb.regression import RegressionManager
import comopy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--toplevel", required=True)
    parser.add_argument("--module", required=True)
    args = parser.parse_args()

    # 1. 使用 ComoPy 加载你的硬件模型
    # 假设你的 comopy 有一个从名称加载模块的方法
    dut = comopy.load_module(args.toplevel)

    # 2. 启动 cocotb 回归测试管理器
    # 这会直接在当前 Python 进程中运行 test_module 里的 @cocotb.test
    reg = RegressionManager(dut, args.module)
    reg.execute()

if __name__ == "__main__":
    main()