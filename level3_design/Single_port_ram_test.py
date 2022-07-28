import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_ram_bug1(dut):
    """Test for ram output """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    await FallingEdge(dut.clk) 
    dut.we.value = 1
    dut.data.value = 19
    dut.addr.value = 26
    
    await FallingEdge(dut.clk) 
    dut.we.value = 0
    await FallingEdge(dut.clk) 
    dut._log.info((dut.q.value))
    dut._log.info(dut.ram[26].value)