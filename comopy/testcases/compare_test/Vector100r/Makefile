TOPLEVEL_LANG = verilog
SIM = icarus
TOPLEVEL = Vector100r
MODULE = test_Vector100r_auto
VERILOG_SOURCES = $(PWD)/Vector100r.sv
include $(shell cocotb-config --makefiles)/Makefile.sim
.PHONY: clean_all

clean_all: clean
	rm -f Vector100r.sv test_Vector100r_auto.py
	rm -rf dump.vcd sim_build/
	rm -rf __pycache__ .pytest_cache
