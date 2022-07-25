# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""

    #cocotb.log.info('##### CTB: Develop your test here ########')
    #1st bug:
    SEL=13
    INP12=3
    INP13=2

    dut.sel.value=SEL
    dut.inp12.value=INP12
    dut.inp13.value=INP13

    await Timer(2,units='ns')

    assert dut.out.value == INP13, f"Multiplexer result incorrect :{dut.out.value}!=10"

async def test_mux_1(dut):
    SEL=30
    INP30=1
    #2nd bug:

    dut.sel.value=SEL
    dut.inp30.value=INP30

    await Timer(2,units='ns')

    assert dut.out.value == INP30, f"Multiplexer result incorrect :{dut.out.value}!=01"


