import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    clock=clock(dut.CLK,10, units="us")
    cocotb.start_soon(clock.start())
    dut.RSTn.value=0

    await RisingEdge(dut.CLK)
    dut.RSTn.value=1
    await RisingEdge(dut.CLK)
    dut.WR_EN.value=1
    dut.DATA_IN.value=40
    await RisingEdge(dut.CLK)
    dut.DATA_IN.value=50

    await RisingEdge(dut.CLK)
    dut.DATA_IN.value=60

    await RisingEdge(dut.CLK)
    dut.DATA_IN.value=70

    await RisingEdge(dut.CLK)
    dut.RD_EN.value=1
    dut.WR_EN.value=0

    await RisingEdge(dut.CLK)

    assert dut.DATA_OUT.value==60,f"Incorrect output {dut.DATA_OUT.value} !=60"

