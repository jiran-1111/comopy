import comopy.testcases.ex_HDLBits_features as ex
from comopy.hdl import Input, IOStruct, Output
from comopy_tools.Runner_base_test_case import RunnerBaseTestCase

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
        self.simulate(ex.Gates100(), self.TV)

if __name__ == "__main__":
    t = TestGates100()
    t.test()