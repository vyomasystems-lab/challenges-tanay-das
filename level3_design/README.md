# 64 X 8 bit Memory Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![image](https://user-images.githubusercontent.com/55503850/181925769-1a083a43-7106-427d-ab48-4f787ef2a6bd.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (64 X 8 bit Memory here) which takes in 3 input, one is write enable line (we), another one is the data which have to store in the memory and the last input is memory address.

The values are assigned to the input port using 
```
  dut.we.value = 1
  dut.data.value = 19
  dut.addr.value = 26

```

The assert statement is used for comparing the DUT output to the stored data value.

The following error is seen:
```
test_ram_bug1 failed
Traceback (most recent call last):
 File "/workspace/challenges-tanay-das/level3_design/Single_port_ram_test.py", line 26, in test_ram_bug1
  assert dut.q.value==dut.ram[26].value, f"Output of the DUT are not matching with the stored data"

```

## Test Scenario **(Important)**

## case 1 (Bug 1):

    await FallingEdge(dut.clk) 
    dut.we.value = 1
    dut.data.value = 19
    dut.addr.value = 26
    
    await FallingEdge(dut.clk) 
    dut.we.value = 0
    await FallingEdge(dut.clk) 
    dut._log.info((dut.q.value))
    dut._log.info(dut.ram[26].value)
    assert dut.q.value==dut.ram[26].value, f"Output of the DUT are not matching with the stored data"


![image](https://user-images.githubusercontent.com/55503850/181926080-6fea4cbf-ab55-42da-b5c1-79668625ea3d.png)

Here in the 26 address value data value 19 is stored as write enable is high.
After that when write eneble is low the data value is not present as output.

![image](https://user-images.githubusercontent.com/55503850/181926182-98c2452a-92a9-43c9-a810-4fa61a4e3c58.png)

## Design Bug
Based on the above test input and analysing the design, we see the following

```
  // Buggy Design

`timescale 1ns / 1ps
module Single_Port_RAM_64x8bit(
    input [7:0] data,
    input [5:0] addr,
    input we,
    input clk,
    output [7:0] q
    );


	reg [7:0] ram [63:0];
	reg [5:0] addr_reg;
	
	always @(posedge clk) begin
	if(we)
		ram[addr] <= data;
	else
		addr_reg <= ram[addr];          ===> Bug
	end
	
	assign q = ram[addr_reg];
endmodule

```
For the 64 X 8 bit Memory design, the logic should be 
```
// Buggy Design

`timescale 1ns / 1ps
module Single_Port_RAM_64x8bit(
    input [7:0] data,
    input [5:0] addr,
    input we,
    input clk,
    output [7:0] q
    );


	reg [7:0] ram [63:0];
	reg [5:0] addr_reg;
	
	always @(posedge clk) begin
	if(we)
		ram[addr] <= data;
	else
		addr_reg <= addr;       ===> Bug fix
	end
	
	assign q = ram[addr_reg];
endmodule

```
## Design Fix
Updating the design and re-running the test makes the test pass.

## *For the above mentioned code*
![image](https://user-images.githubusercontent.com/55503850/181926380-b7cdeffe-2962-4123-a3a4-5fe915c0e69f.png)

## Verification Strategy

- At first make the ```we``` line high and store the data at particular address.
- Next make the `we` line low and check that address, in that address data is present or not.
- If stored data and DUT output is not matching, then it is a bug.

## Is the verification complete ?

According to me Verification process is complete.
