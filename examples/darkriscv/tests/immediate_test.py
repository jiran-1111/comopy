from comopy import BaseTestCase, Input, IOStruct, Output

from ..immediate import Immediate
from ..opcodes import *
from .utils import translate_sv, write_sv

IMM = 0b0010011


class TestImmediate(BaseTestCase):
    class IO(IOStruct):
        xreset = Input()
        insn = Input(32)
        simm = Output(32)
        uimm = Output(32)

    TV = [
        IO(),
        # XR, insn, simm, uimm
        # Reset
        (1, 0, 0, 0),
        # SCC-like instruction
        (
            0,
            0b1100011_00000_00000_000_11011_0000000 | SCC.ext(32),
            0xFFFFF000 | 0b1100011_11011,
            0b1100011_11011,
        ),
        (
            0,
            0b0100011_00000_00000_000_11011_0000000 | SCC.ext(32),
            0b0100011_11011,
            0b0100011_11011,
        ),
        # BCC-like instruction
        (
            0,
            0b1100011_00000_00000_000_11011_0000000 | BCC.ext(32),
            0xFFFFE000 | 0b1_1_100011_1101_0,
            0b1_1_100011_1101_0,
        ),
        (
            0,
            0b0100011_00000_00000_000_11011_0000000 | BCC.ext(32),
            0b0_1_100011_1101_0,
            0b0_1_100011_1101_0,
        ),
        # JAL-like instruction
        (
            0,
            0b1_1000110000_0_00000101_00000_0000000 | JAL.ext(32),
            0xFFE00000 | 0b1_00000101_0_1000110000_0,
            0b1_00000101_0_1000110000_0,
        ),
        (
            0,
            0b0_1000110000_0_00000101_00000_0000000 | JAL.ext(32),
            0b0_00000101_0_1000110000_0,
            0b0_00000101_0_1000110000_0,
        ),
        # LUI and AUIPC-like instruction
        (0, 0xF3212_000 | LUI.ext(32), 0xF3212_000, 0xF3212_000),
        (0, 0x73212_000 | AUIPC.ext(32), 0x73212_000, 0x73212_000),
        # I-like instruction
        (0, 0xF12_00000 | IMM, 0xFFFFF_000 | 0xF12, 0xF12),
        (0, 0x712_00000 | IMM, 0x712, 0x712),
    ]

    def test(self):
        top = Immediate(name="top")
        self.simulate(top, self.TV)


def test_translate():
    top = Immediate(name="Immediate")
    sv = translate_sv(top)
    write_sv(sv, "immediate.sv")
