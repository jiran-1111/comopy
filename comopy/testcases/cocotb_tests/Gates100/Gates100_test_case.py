import comopy.testcases.ex_HDLBits_features as ex
from comopy.hdl import Input, IOStruct, Output
from comopy.testcases.Cocotb_base_test_case import CocotbBaseTestCase



class TestGates100(CocotbBaseTestCase):

    class IO(IOStruct):
        in_ = Input(100)
        out_and = Output()
        out_or = Output()
        out_xor = Output()

    TV = [
        IO(),
        (0x0, 0, 0, 0),
        (0xABCDEFFE, 0, 1, 0),
        (0xFFFFFFFF, 0, 1, 0),
        (0x111111111, 0, 1, 1),
    ]

    def test(self):
        self.simulate(ex.Gates100(), self.TV)

if __name__ == "__main__":
    t = TestGates100()
    t.test()