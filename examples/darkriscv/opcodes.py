"""
RISC-V opcodes.
"""

from comopy.bits import b7  # type: ignore

# lui   rd,imm[31:12]
LUI = b7(0b01101_11)

# auipc rd,imm[31:12]
AUIPC = b7(0b00101_11)

# jal   rd,imm[xxxxx]
JAL = b7(0b11011_11)

# jalr  rd,rs1,imm[11:0]
JALR = b7(0b11001_11)

# bcc   rs1,rs2,imm[12:1]
BCC = b7(0b11000_11)

# lxx   rd,rs1,imm[11:0]
LCC = b7(0b00000_11)

# sxx   rs1,rs2,imm[11:0]
SCC = b7(0b01000_11)

# xxxi  rd,rs1,imm[11:0]
MCC = b7(0b00100_11)

# xxx   rd,rs1,rs2
RCC = b7(0b01100_11)

# custom-0
# CUS = b7(0b00010_11)

# exx, csrxx, mret
CCC = b7(0b11100_11)
