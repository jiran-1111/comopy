TOPLEVEL_LANG = verilog
SIM = icarus
TOPLEVEL = Notgate
MODULE = test_Notgate_auto
VERILOG_SOURCES = $(PWD)/Notgate.sv
include $(shell cocotb-config --makefiles)/Makefile.sim
.PHONY: clean_all

clean_all: clean
	rm -f Notgate.sv test_Notgate_auto.py
	rm -rf dump.vcd sim_build/
	rm -rf __pycache__ .pytest_cache
