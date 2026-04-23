TOPLEVEL_LANG = verilog
SIM = icarus
TOPLEVEL = Conditional
MODULE = test_Conditional_auto
VERILOG_SOURCES = $(PWD)/Conditional.sv
include $(shell cocotb-config --makefiles)/Makefile.sim
.PHONY: clean_all

clean_all: clean
	rm -f Conditional.sv test_Conditional_auto.py
	rm -rf dump.vcd sim_build/
	rm -rf __pycache__ .pytest_cache
