在编写cocotb脚本的时（例如 run_test.py）中，需要多加一行 import comopy_tools：

```Python
import comopy_tools  # 这一行会自动完成“注册”
from cocotb_tools.runner import get_runner # 正常加入get_runner

def test_run():
    # 现在你可以直接传 "comopy" 了！
    runner = get_runner("comopy")
    
    runner.build(...)
    runner.test(
        hdl_toplevel="MyDesign",
        test_module="test_script"
    )
```


任务拆解：

1、get_runner

给cocotb打个补丁

2、build

和basetestcase相似的使用方法

先把上面两个实现

3、test 较为复杂

先看一下comopy的仿真信号是如何传递的



逻辑顺序：

test包含一个cocotb测试脚本+一个comopy测试脚本


comopy:的内容主要是sv模块的pyhton脚本 确定谁是input 谁是output


cocotb:赋值，测试成功条件，确定模块