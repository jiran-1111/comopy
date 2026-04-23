TOPLEVEL_LANG = verilog
SIM = icarus
TOPLEVEL = Andgate
MODULE = test_Andgate_auto
VERILOG_SOURCES = $(PWD)/Andgate.sv
include $(shell cocotb-config --makefiles)/Makefile.sim
.PHONY: clean_all

clean_all: clean
	rm -f Andgate.sv test_Andgate_auto.py
	rm -rf dump.vcd sim_build/
	rm -rf __pycache__ .pytest_cache
