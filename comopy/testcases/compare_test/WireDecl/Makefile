TOPLEVEL_LANG = verilog
SIM = icarus
TOPLEVEL = WireDecl
MODULE = test_WireDecl_auto
VERILOG_SOURCES = $(PWD)/WireDecl.sv
include $(shell cocotb-config --makefiles)/Makefile.sim
.PHONY: clean_all

clean_all: clean
	rm -f WireDecl.sv test_WireDecl_auto.py
	rm -rf dump.vcd sim_build/
	rm -rf __pycache__ .pytest_cache
