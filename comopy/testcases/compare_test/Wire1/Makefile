TOPLEVEL_LANG = verilog
SIM = icarus
TOPLEVEL = Wire1
MODULE = test_Wire1_auto
VERILOG_SOURCES = $(PWD)/Wire1.sv
include $(shell cocotb-config --makefiles)/Makefile.sim
.PHONY: clean_all

clean_all: clean
	rm -f Wire1.sv test_Wire1_auto.py
	rm -rf dump.vcd sim_build/
	rm -rf __pycache__ .pytest_cache
