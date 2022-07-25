# MULTIPLIER DESIGN VERIFICATION

The verification environment is setup using Vyoma's UpTickPro provided for the hackathon.

# VERIFICATION ENVIRONMENT:

The CoCoTb based Python test is developed. The test drives inputs to the Design Under Test (multiplexer 31:1 module-mux.v) which takes in 31 2-bit inputs inp0.....inp30 and gives 2-bit output out.The selection input is given using 5-bit sel. 

The values assigned:
1) First Test:
```
 SEL=13
    INP12=3
    INP13=2

    dut.sel.value=SEL
    dut.inp12.value=INP12
    dut.inp13.value=INP13
 
 ```
   The assert statement is used to compare the output of the mutiplexer to the expected output[i.e 2(10)]
   
   Following error statement encountered:
   ```
    test_mux failed
                     Traceback (most recent call last):
                       File "/workspace/challenges-div1010/level1_design1/test_mux.py", line 22, in test_mux
                         assert dut.out.value == INP13, f"Multiplexer result incorrect :{dut.out.value}!=10"
                     AssertionError: Multiplexer result incorrect :11!=10
     ```                
 2)Second Test:
 
 ```
    SEL=30
    INP30=1
    
    dut.sel.value=SEL
    dut.inp30.value=INP30
    
  ```
   The assert statement is used to compare the output of the mutiplexer to the expected output[i.e 1(01)]
   
   Following error statement encountered:
   
   ```
    test_mux_1 failed
                     Traceback (most recent call last):
                       File "/workspace/challenges-div1010/level1_design1/test_mux.py", line 35, in test_mux_1
                         assert dut.out.value == INP30, f"Multiplexer result incorrect :{dut.out.value}!=01"
                     AssertionError: Multiplexer result incorrect :00!=01
    ```                 
                     
   ![image](https://user-images.githubusercontent.com/78270386/180756460-fb5cd49e-43f5-4985-acc2-27d80ce10b7e.png)


# Test Scenario

1)1st Test:

Test inputs: inp12=3,inp13=2
Expected Output: out= 2 (10)
Observed Output: out= 3 (11)

2)2nd Test:

Test inputs: inp30=1
Expected Output: out= 1 (01)
Observed Output: out= 0 (00)


 Output mismatch singnals to presence of bugs in design
 
 # Design Bug
 
 Analysing the design it is found that 2 bugs are present:
 ```
      5'b01101: out = inp12;
      5'b01101: out = inp13;
```

For the case of out=inp12 the sel input should be 5'b01100 instead of 5'b01101.

Also

The case statement for the sel input = 30(5'b11110) is missing leading to default case being called for the sel=30.

The correction:

```
5'b11110: out = inp30;

```

# Design Fix:

After fixing the bugs the design passes both the test cases


![image](https://user-images.githubusercontent.com/78270386/180758548-299e8544-7c1a-4c0f-9a05-1b35559ebb9d.png)




                     
                     



