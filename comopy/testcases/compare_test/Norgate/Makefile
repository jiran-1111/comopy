TOPLEVEL_LANG = verilog
SIM = icarus
TOPLEVEL = Norgate
MODULE = test_Norgate_auto
VERILOG_SOURCES = $(PWD)/Norgate.sv
include $(shell cocotb-config --makefiles)/Makefile.sim
.PHONY: clean_all

clean_all: clean
	rm -f Norgate.sv test_Norgate_auto.py
	rm -rf dump.vcd sim_build/
	rm -rf __pycache__ .pytest_cache
