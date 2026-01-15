import comopy.testcases.ex_HDLBits_features as ex
from comopy.hdl import Input, IOStruct, Output
from comopy.testcases.base_test_case import BaseTestCase

class TestReduction(BaseTestCase):
    class IO(IOStruct):
        in_ = Input(8)
        parity = Output()

    TV = [IO(), (0x00, 0), (0x01, 1), (0x0F, 0), (0xFF, 0), (0xAB, 1)]

    def test(self):
        self.cocotb_simulate("Reduction", self.TV)


if __name__ == "__main__":
    t = TestReduction()
    t.test()