"""
Configuration constants for the DarkRiscv SoC.
"""

from comopy.bits import b32  # type: ignore

# Reset PC
RESET_PC = b32(0x0)

# Memory address length
MLEN = 13
