"""
Memory of DarkRiscv SoC.
"""

from comopy import Bool, Input, Logic, Module, Output, build, seq
from comopy.bits import FALSE, TRUE

from .config import MLEN


class Memory(Module):
    @build
    def in_ports(s):
        s.reset = Input()
        s.insn_addr = Input(32)
        s.data_addr = Input(32)
        s.data_in = Input(32)
        s.write = Input()
        s.read = Input()
        s.byte_en = Input(4)

    @build
    def out_ports(s):
        s.mem_waddr = Output(32)
        s.insn_data = Output(32)  # ROMFF
        s.data_out = Output(32)
        s.halt = Output()

    @build
    def memory(s):
        s.mem = Logic(32) @ ((1 << MLEN) // 4)

    @seq
    def insn_bus(s):
        s.insn_data <<= 0 if s.reset else s.mem[s.insn_addr[2:MLEN]]

    @build
    def data_bus(s):
        s.d_ack = Logic()
        s.d_hit = Logic()
        s.w_hit = Logic()

        # Note: In a zero-delay simulation, d_hit is always 1.
        # This behavior differs from the original DarkRiscv.
        s.d_hit @= not (s.read and s.d_ack != 1)
        s.w_hit @= 1
        s.halt @= not s.d_hit or not s.w_hit

    @seq
    def update_dack(s):  # stage #1.0
        # wait-states
        # Fix for zero-delay simulation
        # 0 if s.reset else s.d_ack - 1 if s.d_ack else 1 if s.read else 0
        s.d_ack <<= FALSE if s.reset else TRUE if s.read else FALSE

    @seq
    def read_data(s):  # stage #1.5
        s.data_out <<= 0 if s.reset else s.mem[s.data_addr[2:MLEN]]

    @seq
    def write_data(s):
        # write-only operation with 0 wait-state:
        for i in range(4):
            if (
                not s.halt
                and s.write
                and s.data_addr[31] == 0
                and s.byte_en[i]
            ):
                s.mem[s.data_addr[2:MLEN]][i * 8, 8] <<= s.data_in[i * 8, 8]
        s.mem_waddr <<= 0 if s.reset else s.data_addr  # 1 clock delayed
