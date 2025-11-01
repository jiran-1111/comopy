"""
Load-store unit of DarkRiscv core.
"""

from comopy import Input, Logic, Output, RawModule, build, cat
from comopy.bits import *


class LSU(RawModule):
    @build
    def ports(s):
        s.fct3 = Input(3)
        s.data_addr = Input(32)
        s.data_in = Input(32)
        s.rs2_reg = Input(32)
        s.ld_data = Output(32)
        s.st_data = Output(32)
        s.byte_en = Output(4)

    @build
    def load_data(s):
        s.ld_b = Logic(32)
        s.ld_b @= (
            s.data_in[24:].S.ext(32)
            if s.data_addr[:2] == 3
            else s.data_in[16:24].S.ext(32)
            if s.data_addr[:2] == 2
            else s.data_in[8:16].S.ext(32)
            if s.data_addr[:2] == 1
            else s.data_in[:8].S.ext(32)
        )
        s.ld_bu = Logic(32)
        s.ld_bu @= (
            s.data_in[24:].ext(32)
            if s.data_addr[:2] == 3
            else s.data_in[16:24].ext(32)
            if s.data_addr[:2] == 2
            else s.data_in[8:16].ext(32)
            if s.data_addr[:2] == 1
            else s.data_in[:8].ext(32)
        )
        s.ld_h = Logic(32)
        s.ld_h @= (
            s.data_in[16:].S.ext(32)
            if s.data_addr[1] == 1
            else s.data_in[:16].S.ext(32)
        )
        s.ld_hu = Logic(32)
        s.ld_hu @= (
            s.data_in[16:].ext(32)
            if s.data_addr[1] == 1
            else s.data_in[:16].ext(32)
        )
        s.ld_w = Logic(32)
        s.ld_w @= s.data_in

        s.ld_data @= (
            s.ld_b
            if s.fct3 == 0
            else s.ld_h
            if s.fct3 == 1
            else s.ld_bu
            if s.fct3 == 4
            else s.ld_hu
            if s.fct3 == 5
            else s.ld_w
        )

    @build
    def store_data(s):
        s.st_b = Logic(32)
        s.st_b @= (
            cat(s.rs2_reg[:8], b24(0))
            if s.data_addr[:2] == 3
            else cat(b8(0), s.rs2_reg[:8], b16(0))
            if s.data_addr[:2] == 2
            else cat(b16(0), s.rs2_reg[:8], b8(0))
            if s.data_addr[:2] == 1
            else cat(b24(0), s.rs2_reg[:8])
        )
        s.st_h = Logic(32)
        s.st_h @= (
            cat(s.rs2_reg[:16], b16(0))
            if s.data_addr[1] == 1
            else cat(b16(0), s.rs2_reg[:16])
        )
        s.st_w = Logic(32)
        s.st_w @= s.rs2_reg

        s.st_data @= (
            s.st_b if s.fct3 == 0 else s.st_h if s.fct3 == 1 else s.st_w
        )

    @build
    def byte_enable(s):
        s.be_b = Logic(4)
        s.be_b @= (
            b4(0b1000)
            if s.data_addr[:2] == 3
            else b4(0b0100)
            if s.data_addr[:2] == 2
            else b4(0b0010)
            if s.data_addr[:2] == 1
            else b4(0b0001)
        )
        s.be_h = Logic(4)
        s.be_h @= b4(0b1100) if s.data_addr[1] else b4(0b0011)
        s.be_w = Logic(4)
        s.be_w @= b4(0b1111)

        s.byte_en @= (
            s.be_b
            if s.fct3 == 0 or s.fct3 == 4
            else s.be_h
            if s.fct3 == 1 or s.fct3 == 5
            else s.be_w
        )
