import comopy.testcases.ex_HDLBits_features as ex
from comopy.hdl import Input, IOStruct, Output
from comopy_tools.Runner_base_test_case import RunnerBaseTestCase
from comopy_tools.dut import ComoPyDUT

class TestGates100(RunnerBaseTestCase):

    class IO(IOStruct):
        in_ = Input(100)
        out_and = Output()
        out_or = Output()
        out_xor = Output()

    TV = [
        IO()
    ]

    def test(self):
        return self.simulate(ex.Gates100(), self.TV)

if __name__ == "__main__":
    t = TestGates100()
    top = t.test()
    # 假设你已经有了 top 和 simulator
    print("Top 对象的属性列表:", [n for n in dir(top) if not n.startswith('_')])
    sim = top.simulator
    sim.start()
    # 检查其中一个属性的类型
    print("in_ 的具体类型是:", type(top.in_))
    dut = ComoPyDUT(top)

    # 验证 1：属性访问
    print(dut.in_) # 应该输出 <ComoPySignal object ...>

    # 验证 2：逻辑联动（核心验证！）
    dut.in_.value = 0
    old_out = dut.out_and.value

    dut.in_.value = (1 << 100) - 1
    new_out = dut.out_and.value

    print("old:", old_out)
    print("new:", new_out)

    if old_out != new_out:
        print("✅ 适配器工作正常")
    else:
        print("❌ 输出没变")