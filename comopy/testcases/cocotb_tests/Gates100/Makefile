TOPLEVEL_LANG = verilog
SIM = icarus
TOPLEVEL = Gates100
MODULE = test_Gates100_auto
VERILOG_SOURCES = $(PWD)/Gates100.sv
include $(shell cocotb-config --makefiles)/Makefile.sim
.PHONY: clean_all

clean_all: clean
	rm -f Gates100.sv test_Gates100_auto.py
	rm -rf dump.vcd sim_build/
	rm -rf __pycache__ .pytest_cache
