from comopy import BaseTestCase, Input, IOStruct, Output

from ..lsu import LSU
from .utils import translate_sv, write_sv

XB = 0b000  # LB SB
XH = 0b001  # LH SH
XW = 0b010  # LW SW
XBU = 0b100  # LBU
XHU = 0b101  # LHU


class TestLSU(BaseTestCase):
    class IO(IOStruct):
        fct3 = Input(3)
        data_addr = Input(32)
        data_in = Input(32)
        rs2_reg = Input(32)

        ld_data = Output(32)
        st_data = Output(32)
        byte_en = Output(4)

    TV = [
        IO(),
        # F3, daddr, data_in,   R2,  ld,   st,   be
        # LB
        (XB, 0x200, 0x12345678, 0x0, 0x78, None, 0b0001),
        (XB, 0x201, 0x12345678, 0x0, 0x56, None, 0b0010),
        (XB, 0x202, 0x12345678, 0x0, 0x34, None, 0b0100),
        (XB, 0x203, 0x12345678, 0x0, 0x12, None, 0b1000),
        (XB, 0x200, 0xF2F4F6F8, 0x0, 0xFFFFFFF8, None, 0b0001),
        (XB, 0x201, 0xF2F4F6F8, 0x0, 0xFFFFFFF6, None, 0b0010),
        (XB, 0x202, 0xF2F4F6F8, 0x0, 0xFFFFFFF4, None, 0b0100),
        (XB, 0x203, 0xF2F4F6F8, 0x0, 0xFFFFFFF2, None, 0b1000),
        # LH
        (XH, 0x200, 0x12345678, 0x0, 0x5678, None, 0b0011),
        (XH, 0x201, 0x12345678, 0x0, 0x5678, None, 0b0011),
        (XH, 0x202, 0x12345678, 0x0, 0x1234, None, 0b1100),
        (XH, 0x200, 0xF234F678, 0x0, 0xFFFFF678, None, 0b0011),
        (XH, 0x202, 0xF234F678, 0x0, 0xFFFFF234, None, 0b1100),
        # LW
        (XW, 0x200, 0x12345678, 0x0, 0x12345678, None, 0b1111),
        # LBU
        (XBU, 0x200, 0xF2F4F6F8, 0x0, 0xF8, None, 0b0001),
        (XBU, 0x201, 0xF2F4F6F8, 0x0, 0xF6, None, 0b0010),
        (XBU, 0x202, 0xF2F4F6F8, 0x0, 0xF4, None, 0b0100),
        (XBU, 0x203, 0xF2F4F6F8, 0x0, 0xF2, None, 0b1000),
        # LHU
        (XHU, 0x200, 0xF234F678, 0x0, 0xF678, None, 0b0011),
        (XHU, 0x202, 0xF234F678, 0x0, 0xF234, None, 0b1100),
        # SB
        (XB, 0x200, 0x0, 0x12345678, None, 0x00000078, 0b0001),
        (XB, 0x201, 0x0, 0x12345678, None, 0x00007800, 0b0010),
        (XB, 0x202, 0x0, 0x12345678, None, 0x00780000, 0b0100),
        (XB, 0x203, 0x0, 0x12345678, None, 0x78000000, 0b1000),
        # SH
        (XH, 0x200, 0x0, 0x12345678, None, 0x00005678, 0b0011),
        (XH, 0x202, 0x0, 0x12345678, None, 0x56780000, 0b1100),
        # SW
        (XW, 0x200, 0x0, 0x12345678, None, 0x12345678, 0b1111),
    ]

    def test(self):
        top = LSU(name="top")
        self.simulate(top, self.TV)


def test_translate():
    top = LSU(name="LSU")
    sv = translate_sv(top)
    write_sv(sv, "lsu.sv")
