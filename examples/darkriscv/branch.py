"""
Branch unit of DarkRiscv core.
"""

from comopy import Bool, Input, Logic, Output, RawModule, build
from comopy.bits import b3  # type: ignore

# FCT3 opcodes for branch
EQ = b3(0b000)
NE = b3(0b001)
LT = b3(0b100)
GE = b3(0b101)
LTU = b3(0b110)
GEU = b3(0b111)


class Branch(RawModule):
    @build
    def in_ports(s):
        s.fct3 = Input(3)
        s.rs1 = Input(32)
        s.rs2 = Input(32)
        s.simm = Input(32)
        s.data_addr = Input(32)
        s.pc = Input(32)
        s.jal = Input()
        s.jalr = Input()
        s.bcc = Input()

    @build
    def out_ports(s):
        s.pc_simm = Output(32)
        s.jreq = Output()
        s.jval = Output(32)

    @build
    def assign(s):
        s.bmux = Logic()
        s.bmux @= (
            (s.fct3 == GEU and s.rs1 >= s.rs2)
            or (s.fct3 == LTU and s.rs1 < s.rs2)
            or (s.fct3 == GE and s.rs1.S >= s.rs2.S)
            or (s.fct3 == LT and s.rs1.S < s.rs2.S)
            or (s.fct3 == NE and s.rs1 != s.rs2)
            or (s.fct3 == EQ and s.rs1 == s.rs2)
        )

        s.pc_simm @= s.pc + s.simm
        s.jreq @= s.jal or s.jalr or (s.bcc & s.bmux)
        s.jval @= s.data_addr if s.jalr else s.pc_simm
