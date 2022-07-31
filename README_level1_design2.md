# SEQUENCE DETECTOR_1011(overlapping)  DESIGN VERIFICATION

The verification environment is setup using Vyoma's UpTickPro provided for the hackathon.

# VERIFICATION ENVIRONMENT

The CoCoTb based Python test is developed. The test drives inputs to the Design Under Test (sequence_detector module-seq_detect_1101.v) which takes in input inp_bit,reset and clock 
and give output seq_seen.

The values assigned

```
 clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    
    await FallingEdge(dut.clk)
    dut.inp_bit.value=1
    await FallingEdge(dut.clk)
    dut.inp_bit.value=0
    await FallingEdge(dut.clk)
    dut.inp_bit.value=1
    await FallingEdge(dut.clk)
    dut.inp_bit.value=1           //seq_seen becomes 1 at next postive edge as seq 1011 detected
    await FallingEdge(dut.clk)

    dut.inp_bit.value=0
    await FallingEdge(dut.clk)

    dut.inp_bit.value=1
    await FallingEdge(dut.clk)

    dut.inp_bit.value=1           // The sequence till here: 1011_011
    await FallingEdge(dut.clk)    //seq_seen should becomes 1 at the next positive edge.   
```

The assert statement is used to compare the output of the sequence detector(seq_seen) to the expected output [i.e 1]

```

 assert dut.seq_seen.value==1,f"Incorrect output {dut.seq_seen.value} !=1"

```

Following error statement encountered

```
 Traceback (most recent call last):
                       File "/workspace/challenges-div1010/level1_design2/test_seq_detect_1011.py", line 45, in test_seq_bug1
                         assert dut.seq_seen.value==1,f"Incorrect output {dut.seq_seen.value} !=1"
                     AssertionError: Incorrect output 0 !=1

```

![image](https://user-images.githubusercontent.com/78270386/180813961-6c3d2c95-26dd-4199-8ab1-992fea713982.png)



# TEST SCENARIO:

Test inputs: reset=1 
             , reset=0 (next falling edge)

clock:10 us clock period

inp_bit =1_0_1_1_0_1_1 each bit at subsequent falling edges of the clock.

Expected output: seq_seen=1

Observed output: seq_seen=0


# DESIGN BUG - 1

Analysing the design it was found that bugs were present:

```
SEQ_1011:
      begin
        next_state = IDLE;
      end


```

In the state SEQ_1011 in which the sequnce is detected and seq_seen goes to 1.As the sequence_detector is overlapping this 1 should be treated as the starting of another
sequence which can be 1011.So the next state should not be IDLE.

The following correction are done:

```

 SEQ_1011:
      begin
        if(inp_bit==0)
            next_state = SEQ_10;
        else
            next_state = SEQ_1;

       end

```

This leads to the last 1 being considered as starting of another sequence with next state being either SEQ_10 or SEQ_1 despending on the input bit.


# DESIGN FIX - 1

After fixing the bug for the same test case and input sequnece the design passes and the seq_seen bit is 1, hence completing overlapping function.


![image](https://user-images.githubusercontent.com/78270386/180815693-abfbad6c-aae5-43ca-b51c-c791806e630e.png)



# DESIGN BUG - 2
For the values assigned 

```

    clock = Clock(dut.clk, 10, units="us")  
    cocotb.start_soon(clock.start())        

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    
    await FallingEdge(dut.clk)
    dut.inp_bit.value=1
    await FallingEdge(dut.clk)
    dut.inp_bit.value=1
    await FallingEdge(dut.clk)
    dut.inp_bit.value=0
    await FallingEdge(dut.clk)

    dut.inp_bit.value=1
    await FallingEdge(dut.clk)

    dut.inp_bit.value=1
    await FallingEdge(dut.clk)
    
```

AND the assertion statement

```

assert dut.seq_seen.value==1,f"Incorrect output {dut.seq_seen.value} !=1"

```


For a input of 1_1_0_1_1 the output after a falling edge should be 1 ,as the dectector is overlapping the second 1 in the sequence should be considered the start of a correct statement.

But the test case is not passed with following traceback:

```

65000.00ns INFO     test_seq_bug1 failed
                     Traceback (most recent call last):
                       File "/workspace/challenges-div1010/level1_design2/test_seq_detect_1011_1.py", line 42, in test_seq_bug1
                         assert dut.seq_seen.value==1,f"Incorrect output {dut.seq_seen.value} !=1"
                     AssertionError: Incorrect output 0 !=1
 65000.00ns INFO     **********************************************************************************************
                     ** TEST                                  STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                     **********************************************************************************************
                     ** test_seq_detect_1011_1.test_seq_bug1   FAIL       65000.00           0.00   27776848.11  **
                     **********************************************************************************************
                     ** TESTS=1 PASS=0 FAIL=1 SKIP=0                      65000.00           0.02    3416884.08  **
                     **********************************************************************************************

```


![test_fifo py - challenges-div1010 - Gitpod Code - Google Chrome 01-08-2022 01_54_23](https://user-images.githubusercontent.com/78270386/182043937-99b0f3c1-98f3-4bf8-8f39-aff28b18ad14.png)



# Design Fix -2

Upon analysing the design another bug is found:

In the SEQ_1 description:

```
SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = IDLE;
        else
          next_state = SEQ_10;
          
```

The state after encountering a 1 is going back to the idle state, but as this design is a overlapping detector the 1 should be considered a valid start of a correct sequence so the state should remain SEQ_1 instead of going back to idle.This is causing the error and hence the test failed.


The code is corrected as:

```

SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;
        else
          next_state = SEQ_10;
      end

```

After the code is corrected the design passes the test case for the same test scenario and inputs:

![test_seq_detect_1011 py - challenges-div1010 - Gitpod Code - Google Chrome 25-07-2022 21_40_41](https://user-images.githubusercontent.com/78270386/182043371-b3ebb5db-8878-45d8-94ea-47c28cde83cd.png)


                     



