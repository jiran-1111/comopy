安装cocotb 和 cocotb-bus 环境

pip install cooctb

pip install cocotb-bus

打开 comopy/testcases/cocotb_tests/Reduction/ 或其他测试


运行 python3 Reduction_test_case.py 生成sv + Makefile + test_Reduction_auto.py(runner)

运行 python -m pytest test_Reduction_auto.py 测试 

    也可使用 make 命令运行仿真器

使用 make clean_all 删除生成文件
