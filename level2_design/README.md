# Bitmanipulation Coprocessor Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![image](https://user-images.githubusercontent.com/55503850/181906030-61126964-5b2d-471e-8edd-c2ec17053ceb.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (Bitmanipulation Coprocessor module here) which takes in 4 input, among the ```4 mav_putvalue_instr``` is instruction input, and other 3 are data values.

The values are assigned to the input port using 
```
  mav_putvalue_src1 = 0x5
  mav_putvalue_src2 = 0x10
  mav_putvalue_src3 = 0x20
  mav_putvalue_instr = 0x101010B3

```

The assert statement is used for comparing the Bitmanipulation Coprocessor  output to the expected value.

The following error is seen:
```
run_test failed
                     Traceback (most recent call last):
                       File "/workspace/challenges-tanay-das/level2_design/test_mkbitmanip.py", line 62, in run_test
                         assert dut_output == expected_mav_putvalue, error_message
                     AssertionError: Value mismatch DUT = 0xa does not match MODEL = 0x0
```

## Test Scenario **(Important)**

## case 1 (Bug 1):

- mav_putvalue_src1 = 0x5
- mav_putvalue_src2 = 0x10
- mav_putvalue_src3 = 0x20
- mav_putvalue_instr = 0b00000000000000000111000000110011
![image](https://user-images.githubusercontent.com/55503850/181906766-d074df71-97a3-438e-91c3-6833f4c96c18.png)

### Bug :
## Output of the DUT match with the model output for this pattern of inputs
```
 mav_putvalue_src1 = 0x0
 mav_putvalue_src2 = 0x10
 mav_putvalue_src3 = 0x20
 mav_putvalue_instr = 0b00000000000000000111000000110011
```
![image](https://user-images.githubusercontent.com/55503850/181906785-82c699b0-cd1b-49c4-84e2-4b8fc01ed0dc.png)

## In this design when the mav_putvalue_src1 input is equal to 0, then it is not showing any type of error, but when the mav_putvalue_src1!= 0 then the DUT output does not match the model output.
For this input pattern the design fails all the time.
All the instructions for which this design does not provide correct output are listed below.

```
mav_putvalue_instr  = 0b00000000000000000111000000110011
mav_putvalue_instr = 0b00000000000000000110000000110011
mav_putvalue_instr = 0b00000000000000000100000000110011
mav_putvalue_instr = 0b01000000000000000111000000110011
mav_putvalue_instr = 0b01000000000000000111000000110011
mav_putvalue_instr = 0b00000000000000000001000000110011
mav_putvalue_instr = 0b00000000000000000101000000110011
mav_putvalue_instr = 0b01000000000000000101000000110011 
mav_putvalue_instr = 0b00000000000000000001000000010011
mav_putvalue_instr = 0b00000000000000000101000000010011

```

Output mismatches for the above inputs proving that there is a design bug

## Verification Strategy

- In this design I run all the instruction for different inputs , and from the testing result I conclude that the DUT is not working for a particular pattern of inputs. That are mentioned above. Other than that the design is working properly.

## Is the verification complete ?
 According to me Verificationprocess is completed, I found the bugs or the pattern of inputs for that this design is not working.
