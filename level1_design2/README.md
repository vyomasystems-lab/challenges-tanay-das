# TestSequence Detector with overlapping on the non sequence

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![image](https://user-images.githubusercontent.com/55503850/181060268-6565b357-bd69-45d7-932a-87f6bb252c6b.png)


## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (mux module here) which takes in 5-bit select inputs *sel* and 2 bit input *inp i* and gives 2-bit output *out*

The values are assigned to the input port using array and for loop
```
seq = [1,1,0,1,1]
    n = len(seq)
    for i in range(n):
        leng =0
        count+=1
        dut.inp_bit.value = seq[i]
        await FallingEdge(dut.clk)
        if(dut.seq_seen.value == 1):
            dut._log.info(f'Output = 1 at the count = {count}, with sequence parameter in binary= {dut.current_state.value}')
            leng+=1
```

The assert statement is used for comparing the number of detected sequence value to the expected value.

The following error is seen:
<!-- Here for the above sequence number of detected sequence = 1 -->
```
 assert len == 1 , (f'output number is not appripriate')
                     AssertionError: output number is not appripriate
        
```

## Test Scenario **(Important)**

## case 1 (Bug 1):

- For the sequence, 10111011 
- output =1 at 5th cycle and 9th cycle
- In buggy design it only shows one output only at 5th cycle

![image](https://user-images.githubusercontent.com/55503850/181057064-cdbcd964-84e7-4bd3-bcb2-4f722819eeb2.png)


## case 2 (Bug 2):

- For the sequence, 0101011011 
- output =1 at 8th cycle 
- In bugg design output is not observed 

![image](https://user-images.githubusercontent.com/55503850/181057787-4e749770-a890-4b97-b691-f4311935face.png)


## case 3 (Bug 3):

- For the sequence, 11011 
- output = 1 at 6th cycle
- In buggy design output is not observed

![image](https://user-images.githubusercontent.com/55503850/181058098-4de9f4cd-d12c-46a4-bd73-6fdb0111d36b.png)

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
   always @(inp_bit or current_state)
  begin
    case(current_state)
      IDLE:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;
        else
          next_state = IDLE;
      end
      SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = IDLE;  ====> Bug1 (After SEQ_1, if inp_bit ==1 then next sequence should be SEQ_1 not IDLE) 
        else
          next_state = SEQ_10;
      end
      SEQ_10:
      begin
        if(inp_bit == 1)
          next_state = SEQ_101;
        else
          next_state = IDLE;
      end
      SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011;
        else
          next_state = IDLE;   ====> Bug2 (After SEQ_101, if inp_bit ==0 then next sequence should be SEQ_10 not IDLE) 
      end
      SEQ_1011:
      begin
                               ====> Bug3 (Missing one condition, after SEQ_1011 ,if next bit is 1 then the next state should be SEQ_1 and if inp_bit =0 , next state  IDLE) 
          next_state = IDLE;
      end
    endcase
  end
```
For the Sequence Detector design, the logic should be 
```
always @(inp_bit or current_state)
  begin
    case(current_state)
      IDLE:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;
        else
          next_state = IDLE;
      end
      SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;
        else
          next_state = SEQ_10;
      end
      SEQ_10:
      begin
        if(inp_bit == 1)
          next_state = SEQ_101;
        else
          next_state = IDLE;
      end
      SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011;
        else
          next_state = SEQ_10;
      end
      SEQ_1011:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;
        else
          next_state = IDLE;
      end
    endcase
  end
```
## Design Fix
Updating the design and re-running the test makes the test pass.
## *For the sequence, 10111011*
![image](https://user-images.githubusercontent.com/55503850/181059761-a4024351-7cca-4f5a-9cf8-037f73dac1f5.png)


## *For the sequence, 0101011011*

![image](https://user-images.githubusercontent.com/55503850/181059197-cae40ba4-c47b-4b04-8a0d-525649a4aac4.png)

## *For the sequence, 11011*
![image](https://user-images.githubusercontent.com/55503850/181058434-74659010-ce83-4f66-9a21-52bd8b8ed8c5.png)


The updated design is checked in as seq_detect_1011.v

## Verification Strategy

- At first all the bits are taken in to array
- Then using a for loop and assign the value into the input 
- Then check if seq_Seen value = 1 print that the sequence is observed

## Is the verification complete ?

According to me Verification process is complete, I found total 3 bugs and I fixed it.
