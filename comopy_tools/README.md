## comopy_tools
基于 Cocotb 2.0.1 封装的 comopy 仿真适配器，用于在 Cocotb 生态中直接使用 Python 版 HDL 仿真。

### 文件作用

- init.py 
    
    全局扩展 Cocotb 的 get_runner，让系统支持 get_runner("comopy")。

- runner.py 

    实现新的Runner的子类 ComoPy 类，完整适配 Cocotb Runner 接口：

    自动加载并解析 .py 格式 HDL 文件

    自动生成 IO 结构体

    调用仿真流程得到.simulator

- runner_base_test_case.py

    提供底层仿真基类  RunnerBaseTestCase(类似原来的BaseTestCase)

    仿真入口 simulate()

    IO 与测试向量校验

    寄存器初始化

- test_comopy.py
    
    使用测试，直接运行即可测试加法器仿真。hdl文件位于/debug/model/adder.py