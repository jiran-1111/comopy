"""
ALU of DarkRiscv core.
"""

from comopy import Bool, Input, Logic, Output, RawModule, build
from comopy.bits import b3  # type: ignore

# FCT3 opcodes for ALU
ADD = b3(0b000)  # ADD: FCT7 = 0000000, SUB: FCT7 = 0100000
SLL = b3(0b001)
SLT = b3(0b010)
SLTU = b3(0b011)
XOR = b3(0b100)
SRX = b3(0b101)  # SRL: FCT7 = 0000000, SRA: FCT7 = 0100000
OR = b3(0b110)
AND = b3(0b111)


class ALU(RawModule):
    @build
    def ports(s):
        s.rcc = Input()
        s.fct3 = Input(3)
        s.fct7 = Input(7)
        s.rs1 = Input(32)
        s.s2_regx = Input(32)
        s.u2_regx = Input(32)
        s.result = Output(32)

    @build
    def calculate(s):
        s.d_add = Logic(32)
        s.d_add @= (
            s.rs1 - s.s2_regx if s.rcc & s.fct7[5] else s.rs1 + s.s2_regx
        )

        s.d_sll = Logic(32)
        s.d_sll @= s.rs1 << s.u2_regx[:5]

        s.d_slt = Logic(32)
        s.d_slt @= (s.rs1.S < s.s2_regx.S).ext(32)

        s.d_sltu = Logic(32)
        s.d_sltu @= (s.rs1 < s.s2_regx).ext(32)

        s.d_xor = Logic(32)
        s.d_xor @= s.rs1 ^ s.s2_regx

        s.d_srx = Logic(32)
        s.d_srx @= (
            s.rs1.S >> s.u2_regx[:5] if s.fct7[5] else s.rs1 >> s.u2_regx[:5]
        )

        s.d_or = Logic(32)
        s.d_or @= s.rs1 | s.s2_regx

        s.d_and = Logic(32)
        s.d_and @= s.rs1 & s.s2_regx

        s.result @= (
            s.d_add
            if s.fct3 == ADD
            else s.d_sll
            if s.fct3 == SLL
            else s.d_slt
            if s.fct3 == SLT
            else s.d_sltu
            if s.fct3 == SLTU
            else s.d_xor
            if s.fct3 == XOR
            else s.d_srx
            if s.fct3 == SRX
            else s.d_or
            if s.fct3 == OR
            else s.d_and
        )
