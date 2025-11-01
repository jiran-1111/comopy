"""
Program counter of DarkRiscv core.
"""

from comopy import Input, Module, Output, build, seq

from .config import RESET_PC


class PC(Module):
    @build
    def ports(s):
        s.xreset = Input()
        s.halt = Input()
        s.jreq = Input()
        s.jval = Input(32)
        s.pc = Output(32)
        s.next_pc = Output(32)

    @seq
    def update_pc(s):
        if s.xreset:
            s.next_pc <<= RESET_PC
            s.pc <<= RESET_PC
        else:
            s.next_pc <<= (
                s.next_pc if s.halt else s.jval if s.jreq else s.next_pc + 4
            )
            s.pc <<= s.pc if s.halt else s.next_pc
