# Example: DarkRISCV

DarkRISCV is an open-source 32-bit RISC-V implementation written from scratch in Verilog.
See the [original project repository](https://github.com/darklife/darkriscv) for more details.

This example demonstrates a ComoPy reimplementation of DarkRISCV, based on the original Verilog code.

The `rtl/` directory contains Verilog code that is organized into modules based on the original DarkRISCV implementation, but with improved modular design.

The `tests/` directory contains unit tests for the Python modules implemented using ComoPy.


## Boot images
Build a boot image to `src/darkriscv.mem`:
```sh
cd .../src
export CCPATH=.../bin  # RISC-V riscv32-elf toolchain path
make
```

`boot_memcpy.mem` is the pre-built image for `boot_memcpy.s`.
