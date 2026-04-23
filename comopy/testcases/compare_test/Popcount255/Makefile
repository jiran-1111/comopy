TOPLEVEL_LANG = verilog
SIM = icarus
TOPLEVEL = Popcount255
MODULE = test_Popcount255_auto
VERILOG_SOURCES = $(PWD)/Popcount255.sv
include $(shell cocotb-config --makefiles)/Makefile.sim
.PHONY: clean_all

clean_all: clean
	rm -f Popcount255.sv test_Popcount255_auto.py
	rm -rf dump.vcd sim_build/
	rm -rf __pycache__ .pytest_cache
