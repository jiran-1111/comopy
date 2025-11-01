from comopy import BaseTestCase, Input, IOStruct, Output

from ..pc import PC
from .utils import translate_sv, write_sv


class TestPC(BaseTestCase):
    class IO(IOStruct):
        xreset = Input()
        halt = Input()
        jreq = Input()
        jval = Input(32)
        pc = Output(32)
        next_pc = Output(32)

    TV = [
        IO(),
        # reset
        # XR, HLT, JREQ, JVAL, PC, NPC
        (1, 0, 0, 0x0, 0x0, 0x0),
        # Next PC
        (0, 0, 0, 0x0, 0x0, 0x4),
        (0, 0, 0, 0x0, 0x4, 0x8),
        # Halt
        (0, 1, 0, 0x0, 0x4, 0x8),
        (0, 0, 0, 0x0, 0x8, 0xC),
        # Jump
        (0, 0, 1, 0x20, 0xC, 0x20),
        (0, 0, 0, 0x0, 0x20, 0x24),
        (0, 0, 1, 0x30, 0x24, 0x30),
        (0, 0, 0, 0x30, 0x30, 0x34),
    ]

    def test(self):
        top = PC(name="top")
        self.simulate(top, self.TV)


def test_translate():
    top = PC(name="PC")
    sv = translate_sv(top)
    write_sv(sv, "pc.sv")
