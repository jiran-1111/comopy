from comopy import BaseTestCase, Input, IOStruct, Output

from ..alu import *
from .utils import translate_sv, write_sv


class TestALU(BaseTestCase):
    class IO(IOStruct):
        rcc = Input()
        fct3 = Input(3)
        fct7 = Input(7)
        rs1 = Input(32)
        s2_regx = Input(32)
        u2_regx = Input(32)
        result = Output(32)

    TV = [
        IO(),
        # rcc fct3 fct7 rs1     s2         u2  res
        # AND
        (1, AND, 0, 0xFF3344EE, 0xEE1177FF, 0, 0xEE1144EE),
        (0, AND, 0, 0x332299FF, 0xDD2288CC, 0, 0x112288CC),
        # OR
        (1, OR, 0, 0x11223344, 0x12345678, 0, 0x1336777C),
        (1, OR, 0, 0x55667788, 0x12345678, 0, 0x577677F8),
        # SRL
        (1, SRX, 0, 0x12000000, 0, 0xC, 0x00012000),
        (1, SRX, 0, 0x12000000, 0, 0x1C, 0x00000001),
        # SRA
        (1, SRX, 0b0100000, 0xF2000000, 0, 0xC, 0xFFFF2000),
        (1, SRX, 0b0100000, 0x72000000, 0, 0xC, 0x00072000),
        # XOR
        (1, XOR, 0, 0x11223344, 0x12345678, 0, 0x0316653C),
        (1, XOR, 0, 0x55667788, 0x12345678, 0, 0x475221F0),
        # SLTU
        (1, SLTU, 0, 0x4, 0x5, 0, 0x1),
        (1, SLTU, 0, 0x6, 0x5, 0, 0x0),
        (1, SLTU, 0, 0xF0000000, 0x70000000, 0, 0x0),
        (1, SLTU, 0, -3, -2, 0, 0x1),
        (1, SLTU, 0, 3, -2, 0, 0x1),
        # SLT
        (1, SLT, 0, 0x4, 0x5, 0, 0x1),
        (1, SLT, 0, 0x6, 0x5, 0, 0x0),
        (1, SLT, 0, 0xF0000000, 0x70000000, 0, 0x1),
        (1, SLT, 0, -3, -2, 0, 0x1),
        (1, SLT, 0, 3, -2, 0, 0x0),
        # SLL
        (1, SLL, 0, 0x00000012, 0, 0xC, 0x00012000),
        (1, SLL, 0, 0x00000012, 0, 0x1C, 0x20000000),
        # ADD
        (1, ADD, 0, 0x123, 0x123, 0, 0x246),
        (1, ADD, 0, 0xFFFF_F123, 0xFFFF_F123, 0, 0xFFFFE246),
        # SUB
        (1, ADD, 0b0100000, 0x123, 0x123, 0, 0),
        (1, ADD, 0b0100000, 0x123, 0x223, 0, 0xFFFFFF00),
        (1, ADD, 0b0100000, 0x123, 0xFFFFFFFF, 0, 0x124),
    ]

    def test(self):
        top = ALU(name="top")
        self.simulate(top, self.TV)


def test_translate():
    top = ALU(name="ALU")
    sv = translate_sv(top)
    write_sv(sv, "alu.sv")
