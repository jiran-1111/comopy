from comopy import BaseTestCase, Input, IOStruct, Output

from ..decoder import Decoder
from .utils import translate_sv, write_sv


class TestDecoder(BaseTestCase):
    class IO_control(IOStruct):
        xreset = Input()
        flush = Input()
        insn = Input(32)
        lui = Output()
        auipc = Output()
        jal = Output()
        jalr = Output()
        bcc = Output()
        lcc = Output()
        scc = Output()
        mcc = Output()
        rcc = Output()
        ccc = Output()

    TV_control = [
        IO_control(),
        # XR,Flush,Insn, lui,auipc,jal,jalr,bcc,lcc,scc,mcc,rcc,ccc
        # Reset
        (1, 0, 0x0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        # lui
        (0, 0, 0b0110111, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        # auipc
        (0, 0, 0b0010111, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
        # jal
        (0, 0, 0b1101111, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
        # jalr
        (0, 0, 0b1100111, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
        # bcc
        (0, 0, 0b1100011, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
        # lcc
        (0, 0, 0b0000011, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
        # scc
        (0, 0, 0b0100011, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0),
        # mcc
        (0, 0, 0b0010011, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0),
        # rcc
        (0, 0, 0b0110011, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
        # ccc
        (0, 0, 0b1110011, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    ]

    class IO_fields(IOStruct):
        xreset = Input()
        flush = Input()
        insn = Input(32)
        rd_ptr = Output(5)
        rs1_ptr = Output(5)
        rs2_ptr = Output(5)
        opcode = Output(7)
        fct3 = Output(3)
        fct7 = Output(7)

    TV_fields = [
        IO_fields(),
        # XR, Flush, Insn, InPtr, S1Ptr, S2Ptr, Opcode, Fct3, Fct7
        # Reset
        (1, 0, 0x0, None, None, None, None, None, None),
        # Instruction
        (0, 0, 0x1234_5678, 0xC, 0x8, 0x3, 0x78, 0b101, 0b001001),
        (0, 0, 0x8765_4321, 0x6, 0xA, 0x16, 0x21, 0b100, 0b1000011),
        # Flush
        (0, 1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0),
    ]

    def test(self):
        top = Decoder(name="top")
        self.simulate(top, self.TV_control)
        top = Decoder(name="top")
        self.simulate(top, self.TV_fields)


def test_translate():
    top = Decoder(name="Decoder")
    sv = translate_sv(top)
    write_sv(sv, "decoder.sv")
