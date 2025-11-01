from comopy import BaseTestCase, Input, IOStruct, Output

from ..memory import MLEN, Memory
from .utils import translate_sv, write_sv


class TestMemory(BaseTestCase):
    class IO(IOStruct):
        reset = Input()
        insn_addr = Input(32)
        data_addr = Input(32)
        data_in = Input(32)
        write = Input()
        read = Input()
        byte_en = Input(4)
        mem_waddr = Output(32)
        insn_data = Output(32)
        data_out = Output(32)
        halt = Output()

    TV = [
        IO(),
        # R, IA, DA,  DI, WR, RD, BE, MWA,  IData, DO, HLT
        # Reset
        (1, 0x0, 0x0, 0x0, 0, 0, 0xF, 0x0, 0x0, 0x0, 0),
        # Read instruction
        (0, 0x0, 0x0, 0x0, 0, 0, 0xF, 0x0, 0xDB000000, 0xDB000000, 0),
        # Write word & Read instruction
        (0, 0x4, 0x20, 0xDEADBEEF, 1, 0, 0xF, 0x20, 0xDB010001, 0xDB080008, 0),
        # Write half word & Read instruction
        (0, 0x8, 0x24, 0xDEADBEEF, 1, 0, 0x3, 0x24, 0xDB020002, 0xDB090009, 0),
        # Read word
        (0, 0xC, 0x20, 0x0, 0, 1, 0x0, 0x20, 0xDB030003, 0xDEADBEEF, 0),
        # Write byte & Read instruction
        (0, 0x10, 0x28, 0x11, 1, 0, 0x1, 0x28, 0xDB040004, 0xDB0A000A, 0),
        # Write byte & Read instruction
        (0, 0x14, 0x28, 0x330000, 1, 0, 0x4, 0x28, 0xDB050005, 0xDB0A0011, 0),
        # Read word
        (0, 0x18, 0x24, 0x0, 0, 1, 0x0, 0x24, 0xDB060006, 0xDB09BEEF, 0),
        # Read word
        (0, 0x1C, 0x28, 0x0, 0, 1, 0x0, 0x28, 0xDB070007, 0xDB330011, 0),
        (0, 0x20, 0x28, 0x0, 0, 1, 0x0, 0x28, 0xDEADBEEF, 0xDB330011, 0),
        # Read instruction
        (0, 0x24, 0x0, 0x0, 0, 0, 0x0, None, 0xDB09BEEF, None, 0),
        (0, 0x28, 0x0, 0x0, 0, 0, 0x0, None, 0xDB330011, None, 0),
    ]

    Mem = {
        "top.mem": [
            0xDB000000 | (k << 16) | k for k in range((1 << MLEN) // 4)
        ]
    }

    def test(self):
        top = Memory(name="top")
        self.simulate(top, self.TV, self.Mem)


def test_translate():
    top = Memory(name="Memory")
    sv = translate_sv(top)
    write_sv(sv, "memory.sv")
