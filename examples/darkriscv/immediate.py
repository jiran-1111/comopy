"""
Immediate operand of DarkRiscv core.
"""

from comopy import Input, Logic, Output, RawModule, build, cat
from comopy.bits import *

from .opcodes import *


class Immediate(RawModule):
    @build
    def ports(s):
        s.xreset = Input()
        s.insn = Input(32)
        s.simm = Output(32)
        s.uimm = Output(32)

    @build
    def signed_imm(s):
        s.simm_i = Logic(32)
        s.simm_i @= cat(s.insn[31] ** 20, s.insn[20:])
        s.simm_s = Logic(32)
        s.simm_s @= cat(s.insn[31] ** 20, s.insn[25:], s.insn[7:12])
        s.simm_b = Logic(32)
        s.simm_b @= cat(
            s.insn[31] ** 19,
            s.insn[31],
            s.insn[7],
            s.insn[25:31],
            s.insn[8:12],
            b1(0),
        )
        s.simm_j = Logic(32)
        s.simm_j @= cat(
            s.insn[31] ** 11,
            s.insn[31],
            s.insn[12:20],
            s.insn[20],
            s.insn[21:31],
            b1(0),
        )
        s.simm_u = Logic(32)
        s.simm_u @= cat(s.insn[12:], b12(0))

        s.simm @= (
            0
            if s.xreset
            else s.simm_s
            if s.insn[:7] == SCC
            else s.simm_b
            if s.insn[:7] == BCC
            else s.simm_j
            if s.insn[:7] == JAL
            else s.simm_u
            if s.insn[:7] == LUI or s.insn[:7] == AUIPC
            else s.simm_i
        )

    @build
    def unsigned_imm(s):
        s.uimm_i = Logic(32)
        s.uimm_i @= cat(b20(0), s.insn[20:])
        s.uimm_s = Logic(32)
        s.uimm_s @= cat(b20(0), s.insn[25:], s.insn[7:12])
        s.uimm_b = Logic(32)
        s.uimm_b @= cat(
            b19(0), s.insn[31], s.insn[7], s.insn[25:31], s.insn[8:12], b1(0)
        )
        s.uimm_j = Logic(32)
        s.uimm_j @= cat(
            b11(0), s.insn[31], s.insn[12:20], s.insn[20], s.insn[21:31], b1(0)
        )
        s.uimm_u = Logic(32)
        s.uimm_u @= cat(s.insn[12:], b12(0))

        s.uimm @= (
            0
            if s.xreset
            else s.uimm_s
            if s.insn[:7] == SCC
            else s.uimm_b
            if s.insn[:7] == BCC
            else s.uimm_j
            if s.insn[:7] == JAL
            else s.uimm_u
            if s.insn[:7] == LUI or s.insn[:7] == AUIPC
            else s.uimm_i
        )
