# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)
    count = 0

   
    # overlapping with non sequence
    # 1011011 => output = 1 at 5th cycle
    # 10111011 => output =1 at 5th cycle and 9th cycle, in buggy design it only shows one output only at 5th cyle
    # 101101011 => output =1 at 5th cycle and 10th cycle
    # 0101011011 => output =1 at 8th cycle  in bugg design output is not observed 

    seq = [0,1,0,1,0,1,1,0,1,1]
    n = len(seq)
    for i in range(n):
        leng =0
        count+=1
        dut.inp_bit.value = seq[i]
        await FallingEdge(dut.clk)
        if(dut.seq_seen.value == 1):
            dut._log.info(f'Output = 1 at the count = {count}, with sequence parameter in binary= {dut.current_state.value}')
            leng+=1
        # assert leng == 1 , (f'output number is not appripriate')    
    