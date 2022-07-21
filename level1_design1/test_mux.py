# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    dut.inp0.value = 3
    await Timer(2, units='ns')
    dut.sel.value = 00000
    
    await Timer(5, units='ns')
    a = dut.out.value
    dut._log.info('hello this is the value')
    dut._log.info(a)
    dut._log.info(dut.inp0.value)