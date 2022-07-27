# MUX Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![gitpod](https://user-images.githubusercontent.com/55503850/181066490-af18f5ac-21ba-442e-86f9-7604191db616.PNG)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (mux module here) which takes in 5-bit select inputs *sel* and 2 bit input *inp i* and gives 2-bit output *out*

The values are assigned to the input port using 
```
dut.sel.value = 30
dut.inp30.value = 1
```

The assert statement is used for comparing the mux outut to the expected value.

The following error is seen:
```
assert dut.inp30.value == dut.out.value, (f'Wrong output, expected output= {dut.inp30.value}, but output from the circuit= {dut.out.value}')
                     AssertionError: Wrong output, expected output= 01, but output from the circuit= 00
```
![level1_design1_1](https://user-images.githubusercontent.com/55503850/181067134-96b31e21-e092-4493-be5b-d31ba3e59d5c.PNG)

```
assert dut.inp12.value == dut.out.value, (f'Wrong output, expected output= {dut.inp12.value}, but output from the circuit= {dut.out.value}')
                     AssertionError: Wrong output, expected output= 11, but output from the circuit= 00
```
![level1_design1_2_inp12](https://user-images.githubusercontent.com/55503850/181067196-8ca2cb82-6afa-4c68-a28b-b6a6960b113f.PNG)

```
assert dut.inp13.value == dut.out.value, (f'Wrong output, expected output= {dut.inp13.value}, but output from the circuit= {dut.out.value}')
                     AssertionError: Wrong output, expected output= 10, but output from the circuit= 11
```
![level1_design1_2_inp13](https://user-images.githubusercontent.com/55503850/181067255-523a6a54-4242-4600-908c-86ddd97fdf01.PNG)


## Test Scenario **(Important)**

## case 1 (Bug 1):

- Test Inputs: dut.inp30.value = 1, dut.sel.value = 30
- Expected Output: out = inp30 = 01
- Observed Output in the DUT dut.out = 00

## case 2 (Bug 2):

- Test Inputs: dut.inp12.value = 3, dut.sel.value = 12
- Expected Output: out = inp12 = 11
- Observed Output in the DUT dut.out = 00

## case 3 (Bug 3):

- Test Inputs: dut.inp13.value = 2, dut.sel.value = 13
- Expected Output: out = inp13 = 10
- Observed Output in the DUT dut.out = 11

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
 begin
    case(sel)
      5'b00000: out = inp0;  
      5'b00001: out = inp1;  
      5'b00010: out = inp2;  
      5'b00011: out = inp3;  
      5'b00100: out = inp4;  
      5'b00101: out = inp5;  
      5'b00110: out = inp6;  
      5'b00111: out = inp7;  
      5'b01000: out = inp8;  
      5'b01001: out = inp9;  
      5'b01010: out = inp10;
      5'b01011: out = inp11;
      5'b01101: out = inp12;                ======> Bug (select line 12 is missing, instead of 12, this select line is 13)
      5'b01101: out = inp13;                ======> Bug (For select line 13 it provide inp12 as out, as above select line is also 13)
      5'b01110: out = inp14;
      5'b01111: out = inp15;
      5'b10000: out = inp16;
      5'b10001: out = inp17;
      5'b10010: out = inp18;
      5'b10011: out = inp19;
      5'b10100: out = inp20;
      5'b10101: out = inp21;
      5'b10110: out = inp22;
      5'b10111: out = inp23;
      5'b11000: out = inp24;
      5'b11001: out = inp25;
      5'b11010: out = inp26;
      5'b11011: out = inp27;
      5'b11100: out = inp28;
      5'b11101: out = inp29;                ======> Bug (Output for inp30 is missing)
      default: out = 0;
    endcase
  end
```
For the adder design, the logic should be ``5'b01100: out = inp12;`` instead of ``5'b01101: out = inp12;`` and ``5'b11110: out = inp30; ``  as in the design code.

## Design Fix
Updating the design and re-running the test makes the test pass.

## *For input 30*
![fix_bug_30](https://user-images.githubusercontent.com/55503850/181068505-d4842164-583d-4455-b469-811640a051ff.PNG)


## *For input 13*
![fix_bug_13](https://user-images.githubusercontent.com/55503850/181068605-29e850c1-d7a9-4539-9325-3c254673c550.PNG)

## *For input 12*
![fix_bug_12](https://user-images.githubusercontent.com/55503850/181068692-480dbeb6-1f7c-4460-bc6b-372462d9897d.PNG)

The updated design is checked in as mux.v

## Verification Strategy

- Here in this verification method, at first I assign some value to the input terminal
- Then assign the value in to the select input
- Then check that the output is matching with the input or not for specific select line

## Is the verification complete ?
 According to me Verificationprocess is completed, I found total 3 bugs for 3 different select lines.
 For select line 30, 13 and 12.

