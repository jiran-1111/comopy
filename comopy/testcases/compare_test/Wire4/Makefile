TOPLEVEL_LANG = verilog
SIM = icarus
TOPLEVEL = Wire4
MODULE = test_Wire4_auto
VERILOG_SOURCES = $(PWD)/Wire4.sv
include $(shell cocotb-config --makefiles)/Makefile.sim
.PHONY: clean_all

clean_all: clean
	rm -f Wire4.sv test_Wire4_auto.py
	rm -rf dump.vcd sim_build/
	rm -rf __pycache__ .pytest_cache
