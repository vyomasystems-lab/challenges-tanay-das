# See LICENSE.vyoma for details

TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)

VERILOG_SOURCES = $(PWD)/Single_Port_RAM_64x8bit.v               # provide your design path

TOPLEVEL := Single_Port_RAM_64x8bit       # design file
MODULE   := Single_port_ram_test   # test file

include $(shell cocotb-config --makefiles)/Makefile.sim

clean_all: clean
	rm -rf *.xml sim_build __pycache__ 
