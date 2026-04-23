TOPLEVEL_LANG = verilog
SIM = icarus
TOPLEVEL = Xnorgate
MODULE = test_Xnorgate_auto
VERILOG_SOURCES = $(PWD)/Xnorgate.sv
include $(shell cocotb-config --makefiles)/Makefile.sim
.PHONY: clean_all

clean_all: clean
	rm -f Xnorgate.sv test_Xnorgate_auto.py
	rm -rf dump.vcd sim_build/
	rm -rf __pycache__ .pytest_cache
