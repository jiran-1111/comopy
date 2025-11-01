"""
DarkRiscv SoC.
"""

from comopy import Input, Logic, Module, Output, build, cat
from comopy.bits import b1

from .darkriscv import DarkRiscv
from .memory import Memory


class DarkSocv(Module):
    @build
    def ports(s):
        s.reset = Input()
        s.debug = Output(4)

    @build
    def submodules(s):
        s.xaddr = Logic(32)
        s.xdata_in = Logic(32)

        s.core = DarkRiscv(reset=s.reset)
        s.memory = Memory(
            reset=s.reset,
            insn_addr=s.core.insn_addr,
            data_addr=s.core.data_addr,
            data_in=s.core.data_out,
            write=s.core.write,
            read=s.core.read,
            byte_en=s.core.byte_en,
            mem_waddr=s.xaddr,
        )

        s.xdata_in @= s.memory.data_out  # IOMUX

        s.core.insn_data @= s.memory.insn_data
        s.core.data_in @= s.xdata_in

        s.debug @= cat(b1(0), s.core.debug[:3])
