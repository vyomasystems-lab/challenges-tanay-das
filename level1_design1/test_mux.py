# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    sel1 = 5'b00000
    sel2 = 5'b00010

    dut.sel.value = sel1
    cocotb.log.info(f'sel0={sel1} inp0={dut.inp0.value} model={dut.inp0.value} DUT={int(dut.out.value)}')

    assert dut.out.value == dut.inp0.value, f"Adder result is incorrect: {dut.out.value} != {inp0}"

