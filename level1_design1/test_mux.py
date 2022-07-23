# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random
@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    
    dut.inp0.value = 1
    dut.inp1.value = 2
    dut.inp2.value = 3
    dut.inp3.value = 2
    dut.inp4.value = 3
    dut.inp5.value = 3
    dut.inp6.value = 3
    dut.inp7.value = 2
    dut.inp8.value = 1
    dut.inp9.value = 1
    dut.inp10.value = 3
    dut.inp11.value = 2
    dut.inp12.value =3
    dut.inp13.value = 2
    dut.inp14.value = 2
    dut.inp15.value = 3
    dut.inp16.value = 1
    dut.inp17.value = 3
    dut.inp18.value = 2
    dut.inp19.value = 2
    dut.inp20.value = 1
    dut.inp21.value = 3
    dut.inp22.value = 1
    dut.inp23.value = 2
    dut.inp24.value = 1
    dut.inp25.value = 2
    dut.inp26.value = 3
    dut.inp27.value = 2
    dut.inp28.value = 1
    dut.inp29.value = 3
    dut.inp30.value = 1

       
    await Timer(2, units='ns')
    i=30
    dut.sel.value = i
    await Timer(2, units='ns')
    if(dut.inp30.value != dut.out.value):
        dut._log.info(f'output missmatch due to this select value {i}')
        dut._log.info(f'input value {dut.inp30.value}')
        dut._log.info(f'output value {dut.out.value}')

    if(dut.inp30.value == dut.out.value):
        dut._log.info(f'output match due to this select value {i}')
        dut._log.info(f'input value {dut.inp30.value}')
        dut._log.info(f'output value {dut.out.value}')
    assert dut.inp30.value == dut.out.value, (f'Wrong output, expected output= {dut.inp30.value}, but output from the circuit= {dut.out.value}')
    
    