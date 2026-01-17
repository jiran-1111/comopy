TOPLEVEL_LANG = verilog
SIM = icarus
TOPLEVEL = Reduction
MODULE = test_Reduction_auto
VERILOG_SOURCES = $(PWD)/Reduction.sv
include $(shell cocotb-config --makefiles)/Makefile.sim
.PHONY: clean_all

clean_all: clean
	rm -f Reduction.sv test_Reduction_auto.py
