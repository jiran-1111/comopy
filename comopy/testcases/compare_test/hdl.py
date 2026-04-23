# Tests for HDLBits examples, more Verilog features
#

import comopy.testcases.ex_HDLBits_features as ex
from comopy.hdl import Input, IOStruct, Output
from comopy.testcases.Cocotb_base_test_case import CocotbBaseTestCase
import comopy.testcases.ex_HDLBits_conn as ex_conn
import comopy.testcases.ex_HDLBits_no_conn as ex_comb

class TestConditional(CocotbBaseTestCase):
    class IO(IOStruct):
        a = Input(8)
        b = Input(8)
        c = Input(8)
        d = Input(8)
        min = Output(8)

    TV = [
        IO(),
        (0x12, 0x34, 0x56, 0x78, 0x12),
        (0x34, 0x12, 0x56, 0x78, 0x12),
        (0x56, 0x34, 0x12, 0x78, 0x12),
        (0x78, 0x34, 0x56, 0x12, 0x12),
    ]

    def test(self):
        self.simulate(ex.Conditional(), self.TV)

class TestReduction(CocotbBaseTestCase):
    class IO(IOStruct):
        in_ = Input(8)
        parity = Output()

    TV = [IO(), (0x00, 0), (0x01, 1), (0x0F, 0), (0xFF, 0), (0xAB, 1)]

    def test(self):
        self.simulate(ex.Reduction(), self.TV)

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

class TestVector100r(CocotbBaseTestCase):
    class IO(IOStruct):
        in_ = Input(100)
        out = Output(100)

    TV = [
        IO(),
        (0, 0),
        (-1, -1),
        (0x55555555_55555555_55555555_5, 0xAAAAAAAA_AAAAAAAA_AAAAAAAA_A),
    ]

    def test(self):
        self.simulate(ex.Vector100r(), self.TV)

class TestPopcount255(CocotbBaseTestCase):
    class IO(IOStruct):
        in_ = Input(255)
        out = Output(8)

    TV = [
        IO(),
        (0, 0),
        (1, 1),
        (0b1111_1111, 8),
        (0b1010_1010, 4),
    ]

    def test(self):
        self.simulate(ex.Popcount255(), self.TV)

class TestConditional(CocotbBaseTestCase):
    class IO(IOStruct):
        a = Input(8)
        b = Input(8)
        c = Input(8)
        d = Input(8)
        min = Output(8)

    TV = [
        IO(),
        (0x12, 0x34, 0x56, 0x78, 0x12),
        (0x34, 0x12, 0x56, 0x78, 0x12),
        (0x56, 0x34, 0x12, 0x78, 0x12),
        (0x78, 0x34, 0x56, 0x12, 0x12),
    ]

    def test(self):
        self.simulate(ex.Conditional(), self.TV)

class TestReduction(CocotbBaseTestCase):
    class IO(IOStruct):
        in_ = Input(8)
        parity = Output()

    TV = [IO(), (0x00, 0), (0x01, 1), (0x0F, 0), (0xFF, 0), (0xAB, 1)]

    def test(self):
        self.simulate(ex.Reduction(), self.TV)

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

class TestVector100r(CocotbBaseTestCase):
    class IO(IOStruct):
        in_ = Input(100)
        out = Output(100)

    TV = [
        IO(),
        (0, 0),
        (-1, -1),
        (0x55555555_55555555_55555555_5, 0xAAAAAAAA_AAAAAAAA_AAAAAAAA_A),
    ]

    def test(self):
        self.simulate(ex.Vector100r(), self.TV)

class TestPopcount255(CocotbBaseTestCase):
    class IO(IOStruct):
        in_ = Input(255)
        out = Output(8)

    TV = [
        IO(),
        (0, 0),
        (1, 1),
        (0b1111_1111, 8),
        (0b1010_1010, 4),
    ]

    def test(self):
        self.simulate(ex.Popcount255(), self.TV)

class TestWire1(CocotbBaseTestCase):
    class IO(IOStruct):
        in_ = Input()
        out = Output()

    TV = [IO(), (0b1, 0b1), (0b0, 0b0)]

    def test(self):
        self.simulate(ex_comb.Wire1(), self.TV)
        self.simulate(ex_conn.Wire1(), self.TV)

class TestWire4(CocotbBaseTestCase):
    class IO(IOStruct):
        a = Input()
        b = Input()
        c = Input()
        w = Output()
        x = Output()
        y = Output()
        z = Output()

    TV = [
        IO(),
        (0b1, 0b0, 0b1, 0b1, 0b0, 0b0, 0b1),
        (0b0, 0b1, 0b0, 0b0, 0b1, 0b1, 0b0),
    ]

    def test(self):
        self.simulate(ex_comb.Wire4(), self.TV)
        self.simulate(ex_conn.Wire4(), self.TV)

class TestNotgate(CocotbBaseTestCase):
    class IO(IOStruct):
        in_ = Input()
        out = Output()

    TV = [IO(), (0b1, 0b0), (0b0, 0b1)]

    def test(self):
        self.simulate(ex_comb.Notgate(), self.TV)
        self.simulate(ex_conn.Notgate(), self.TV)

class TestAndgate(CocotbBaseTestCase):
    class IO(IOStruct):
        a = Input()
        b = Input()
        out = Output()

    TV = [
        IO(),
        (0b0, 0b0, 0b0),
        (0b1, 0b0, 0b0),
        (0b0, 0b1, 0b0),
        (0b1, 0b1, 0b1),
    ]

    def test(self):
        self.simulate(ex_comb.Andgate(), self.TV)
        self.simulate(ex_conn.Andgate(), self.TV)

class TestNorgate(CocotbBaseTestCase):
    class IO(IOStruct):
        a = Input()
        b = Input()
        out = Output()

    TV = [
        IO(),
        (0b0, 0b0, 0b1),
        (0b1, 0b0, 0b0),
        (0b0, 0b1, 0b0),
        (0b1, 0b1, 0b0),
    ]

    def test(self):
        self.simulate(ex_comb.Norgate(), self.TV)
        self.simulate(ex_conn.Norgate(), self.TV)

class TestXnorgate(CocotbBaseTestCase):
    class IO(IOStruct):
        a = Input()
        b = Input()
        out = Output()

    TV = [
        IO(),
        (0b0, 0b0, 0b1),
        (0b1, 0b0, 0b0),
        (0b0, 0b1, 0b0),
        (0b1, 0b1, 0b1),
    ]

    def test(self):
        self.simulate(ex_comb.Xnorgate(), self.TV)
        self.simulate(ex_conn.Xnorgate(), self.TV)

class TestWireDecl(CocotbBaseTestCase):
    class IO(IOStruct):
        a = Input()
        b = Input()
        c = Input()
        d = Input()
        out = Output()
        out_n = Output()

    TV = [
        IO(),
        (0b0, 0b0, 0b0, 0b0, 0b0, 0b1),
        (0b0, 0b0, 0b0, 0b1, 0b0, 0b1),
        (0b0, 0b1, 0b1, 0b1, 0b1, 0b0),
        (0b1, 0b1, 0b1, 0b1, 0b1, 0b0),
    ]

    def test(self):
        self.simulate(ex_comb.WireDecl(), self.TV)
        self.simulate(ex_conn.WireDecl(), self.TV)

if __name__ == "__main__":
    t = TestConditional()
    t.test()
    t = TestReduction()
    t.test()
    t = TestGates100()
    t.test()
    t = TestVector100r()
    t.test()
    t = TestPopcount255()
    t.test()
    t = TestWire1()
    t.test()
    t = TestWire4()
    t.test()
    t = TestNotgate()
    t.test()
    t = TestAndgate()
    t.test()
    t = TestNorgate()
    t.test()
    t = TestXnorgate()
    t.test()
    t = TestWireDecl()
    t.test()
