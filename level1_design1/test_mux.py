# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""

    #cocotb.log.info('##### CTB: Develop your test here ########')
    SEL=13
    INP12=3
    INP13=2

    dut.sel.value=SEL
    dut.inp12.value=INP12
    dut.inp13.value=INP13

    await Timer(2,units='ns')

    assert dut.out.value == INP13, f"Multiplexer result incorrect :{dut.out.value}!=2"
