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
		addr_reg <= addr;
	end
	
	assign q = ram[addr_reg];
endmodule
