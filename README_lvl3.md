# SYNCHRONUS FIFO BUFFER DESIGN VERIFICATION
The verification environment is setup using Vyoma's UpTickPro provided for the hackathon.

# VERIFICATION ENVIRONMENT
The CoCoTb based Python test is developed. The test drives inputs to the Design Under Test (FIFO module-syn_fifo_v1_Nb) which takes in input RSTn,CLK,DATA_IN,RD_EN,WR_EN and give output DATA_OUT,FULL,EMPTY.

The values assigned

```

    dut.RSTn.value=0
    dut.WR_EN.value=0
    dut.RD_EN.value=0
    #dut.DATA_IN.value=0
    clock=Clock(dut.CLK,10, units="us")
    cocotb.start_soon(clock.start())

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
    dut.WR_EN.value=0

    await RisingEdge(dut.CLK)
    dut.RD_EN.value=1

    await RisingEdge(dut.CLK)
    await RisingEdge(dut.CLK)

    

```

The assert statement is used to compare the output of the fifo buffer(DATA_OUT) to the expected output [i.e 40]

```

assert dut.DATA_OUT.value==40,f"Incorrect output {dut.DATA_OUT.value} !=40"

```

As the design currently has no bugs the test case passes.

```
0.00ns INFO     running test_fifo (1/1)
 80000.00ns INFO     test_fifo passed
 80000.00ns INFO     **************************************************************************************
                     ** TEST                          STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                     **************************************************************************************
                     ** test_fifo.test_fifo            PASS       80000.00           0.00   31412125.46  **
                     **************************************************************************************
                     ** TESTS=1 PASS=1 FAIL=0 SKIP=0              80000.00           0.02    5323311.98  **
                     **************************************************************************************


```


![test_fifo py - challenges-div1010 - Gitpod Code - Google Chrome 01-08-2022 00_12_33](https://user-images.githubusercontent.com/78270386/182041222-d076a1a3-48d8-4c65-8f27-01b0f85980ea.png)


In the FIFO buffer the values passed at respective positive edge of clocks are {40,50,60,70} while reset(RSTn) is 1 and write enable(WR_EN) is 1.
When the read_enable(RD_EN) is made 1 and at the next positive edge of the clock the assertion is made as the code is bug free the first value out of the FIFO buffer is 40.


# TEST SCERNARIO

Test inputs: reset=0 
             , reset=1 (next rising edge)

WR_EN=1

clock:10 us clock period

DATA_IN ={40,50,60,70} @ positive edge of the clock.

RD_EN=1

Expected output: DATA_OUT=40

Observed output: DATA_OUT=40

# BUG INSERTION IN THE DESIGN

The following change is made in the design code so to make the FIFO buffer bug ridden.

To read out the data from the buffer the following code is used inside a always block sensitive to clock and reset.

```

 else if( count != 0 && RD_EN )
            begin
                count <= count - 1'b1;
                rd_count <= rd_count + 1'b1;
                DATA_OUT <= MEM[rd_count];

```

To insert bug following change is made

```

 else if( count != 0 && RD_EN )
            begin
                count <= count - 1'b1;
                rd_count <= rd_count + 1'b1;
                DATA_OUT <= MEM[rd_count+1];


```

The line of code DATA_OUT<= MEM[rd_count] is changed to DATA_OUT <= MEM[rd_count+1] this leads to data present at the second index of fifo buffer being output (i.e 50) insted of the data present at the first index of buffer(40).


# FAILED ASSERTION 

Under the same test conditions and test scenario the test fails due to the bug and the following message is given.


```

80000.00ns INFO     test_fifo failed
                     Traceback (most recent call last):
                       File "/workspace/challenges-div1010/level3_design/test_fifo.py", line 42, in test_fifo
                         assert dut.DATA_OUT.value==40,f"Incorrect output {dut.DATA_OUT.value} !=40"
                     AssertionError: Incorrect output 00110010 !=40
 80000.00ns INFO     **************************************************************************************
                     ** TEST                          STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                     **************************************************************************************
                     ** test_fifo.test_fifo            FAIL       80000.00           0.00   38795736.41  **
                     **************************************************************************************
                     ** TESTS=1 PASS=0 FAIL=1 SKIP=0              80000.00           0.01    6485326.82  **
                     **************************************************************************************



```


![test_fifo py - challenges-div1010 - Gitpod Code - Google Chrome 01-08-2022 00_20_52](https://user-images.githubusercontent.com/78270386/182041706-45c88bc3-83c7-460c-a8d6-e633cf52ad8b.png)


