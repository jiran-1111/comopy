"""
Decoder of DarkRiscv core.
"""

from comopy import Bool, Input, Logic, Output, RawModule, build

from .opcodes import *


class Decoder(RawModule):
    @build
    def in_ports(s):
        s.xreset = Input()
        s.flush = Input()
        s.insn = Input(32)

    @build
    def out_controls(s):
        s.lui = Output()
        s.auipc = Output()
        s.jal = Output()
        s.jalr = Output()
        s.bcc = Output()
        s.lcc = Output()
        s.scc = Output()
        s.mcc = Output()
        s.rcc = Output()
        # s.cus = OutPort()
        s.ccc = Output()

    @build
    def out_fields(s):
        s.rd_ptr = Output(5)
        s.rs1_ptr = Output(5)
        s.rs2_ptr = Output(5)
        s.opcode = Output(7)
        s.fct3 = Output(3)
        s.fct7 = Output(7)

    @build
    def assign_control(s):
        s.invalid = Logic()
        s.invalid @= s.flush or s.xreset
        s.lui @= 0 if s.invalid else s.insn[:7] == LUI
        s.auipc @= 0 if s.invalid else s.insn[:7] == AUIPC
        s.jal @= 0 if s.invalid else s.insn[:7] == JAL
        s.jalr @= 0 if s.invalid else s.insn[:7] == JALR
        s.bcc @= 0 if s.invalid else s.insn[:7] == BCC
        s.lcc @= 0 if s.invalid else s.insn[:7] == LCC
        s.scc @= 0 if s.invalid else s.insn[:7] == SCC
        s.mcc @= 0 if s.invalid else s.insn[:7] == MCC
        s.rcc @= 0 if s.invalid else s.insn[:7] == RCC
        s.ccc @= 0 if s.invalid else s.insn[:7] == CCC

    @build
    def assign_fields(s):
        s.insn_data = Logic(32)
        s.insn_data @= 0 if s.xreset else s.insn
        s.rd_ptr @= 0 if s.xreset else s.insn_data[7:12]
        s.rs1_ptr @= s.insn_data[15:20]
        s.rs2_ptr @= s.insn_data[20:25]
        s.opcode @= 0 if s.flush else s.insn_data[:7]
        s.fct3 @= s.insn_data[12:15]
        s.fct7 @= s.insn_data[25:]
