"""
DarkRiscv core.
"""

from comopy import Bool, Input, Logic, Module, Output, build, cat, seq
from comopy.bits import FALSE, TRUE

from .alu import ALU
from .branch import Branch
from .decoder import Decoder
from .immediate import Immediate
from .lsu import LSU
from .pc import PC


class DarkRiscv(Module):
    @build
    def ports(s):
        s.reset = Input()
        s.insn_data = Input(32)
        s.insn_addr = Output(32)
        s.data_in = Input(32)
        s.data_out = Output(32)
        s.data_addr = Output(32)
        s.write = Output()
        s.read = Output()
        s.byte_en = Output(4)
        s.idle = Output()
        s.debug = Output(4)

    @build
    def states(s):
        s.xreset = Logic()
        s.flush = Logic()
        s.dack = Logic()
        s.halt = Logic()
        s.halt2 = Logic()
        s.insn2 = Logic(32)
        s.insn = Logic(32)
        s.pc = Logic(32)
        s.jreq = Logic()

        s.insn @= s.insn2 if s.halt2 else s.insn_data
        s.idle @= s.flush

    @build
    def reg_file(s):
        s.regs = Logic(32) @ 32
        s.rd_ptr = Logic(5)
        s.rs1_ptr = Logic(5)
        s.rs2_ptr = Logic(5)
        s.rd_reg = Logic(32)
        s.rd_data = Logic(32)
        s.rs1_reg = Logic(32)
        s.rs2_reg = Logic(32)

        s.rd_reg @= s.regs[s.rd_ptr]
        s.rs1_reg @= s.regs[s.rs1_ptr]
        s.rs2_reg @= s.regs[s.rs2_ptr]

    @build
    def submodules(s):
        # Decoder
        s.dec = Decoder(
            xreset=s.xreset,
            flush=s.flush,
            insn=s.insn,
            # output
            rd_ptr=s.rd_ptr,
            rs1_ptr=s.rs1_ptr,
            rs2_ptr=s.rs2_ptr,
        )

        # Immediate
        s.s2_regx = Logic(32)
        s.u2_regx = Logic(32)
        s.imm = Immediate(xreset=s.xreset, insn=s.insn)
        s.s2_regx @= s.imm.simm if s.dec.mcc else s.rs2_reg
        s.u2_regx @= s.imm.uimm if s.dec.mcc else s.rs2_reg

        # ALU
        s.alu = ALU(
            rcc=s.dec.rcc,
            fct3=s.dec.fct3,
            fct7=s.dec.fct7,
            rs1=s.rs1_reg,
            s2_regx=s.s2_regx,
            u2_regx=s.u2_regx,
        )

        # Branch
        s.branch = Branch(
            fct3=s.dec.fct3,
            rs1=s.rs1_reg,
            rs2=s.rs2_reg,
            simm=s.imm.simm,
            data_addr=s.data_addr,
            pc=s.pc,
            jal=s.dec.jal,
            jalr=s.dec.jalr,
            bcc=s.dec.bcc,
            # output
            jreq=s.jreq,
        )

        # Load-store
        s.read @= s.dec.lcc
        s.write @= s.dec.scc
        s.halt @= s.read and not s.dack
        s.data_addr @= s.rs1_reg + s.imm.simm
        s.lsu = LSU(
            fct3=s.dec.fct3,
            data_addr=s.data_addr,
            data_in=s.data_in,
            rs2_reg=s.rs2_reg,
            # output
            st_data=s.data_out,
            byte_en=s.byte_en,
        )

        # Write back
        s.rd_data @= (
            s.lsu.ld_data
            if s.dec.lcc
            else s.branch.pc_simm
            if s.dec.auipc
            else s.insn_addr
            if s.dec.jal or s.dec.jalr
            else s.imm.simm
            if s.dec.lui
            else s.alu.result
            if s.dec.mcc or s.dec.rcc
            else s.rd_reg
        )

        # PC
        s.pc_gen = PC(
            xreset=s.xreset,
            halt=s.halt,
            jreq=s.jreq,
            jval=s.branch.jval,
        )
        s.pc @= s.pc_gen.pc
        s.insn_addr @= s.pc_gen.next_pc

        s.debug @= cat(s.xreset, s.idle, s.dec.scc, s.dec.lcc)

    @seq
    def update_states(s):
        s.xreset <<= s.reset
        if s.xreset:
            s.dack <<= FALSE
        else:
            s.dack <<= FALSE if s.dack else TRUE if s.read else FALSE
        if s.halt ^ s.halt2:
            s.insn2 <<= s.insn_data
        s.halt2 <<= s.halt
        s.flush <<= TRUE if s.xreset else s.flush if s.halt else s.jreq

    @seq
    def update_regs(s):
        if s.xreset:
            for i in range(32):
                s.regs[i] <<= 0
        else:
            s.regs[s.rd_ptr] <<= (
                0
                if Bool(s.xreset or s.rd_ptr) == 0
                else s.rd_reg
                if s.halt
                else s.rd_data
            )
