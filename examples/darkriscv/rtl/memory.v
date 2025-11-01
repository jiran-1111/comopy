`timescale 1ns / 1ps
`include "./config.vh"

module memory
(
    input             CLK,
    input             RES,

    input  [31:0]     IADDR,
    input  [31:0]     DADDR,
    input  [31:0]     DATAI,
    input             WR,
    input             RD,
    input  [3:0]      BE,

    output reg [31:0] XADDR,
    output reg [31:0] ROMFF,
    output reg [31:0] DATAO,
    output            HLT
);

    reg [31:0] MEM [0:2**`MLEN/4-1];

    // instruction bus

    always@(posedge CLK) // stage #0.5
    begin
        ROMFF <= MEM[IADDR[`MLEN-1:2]];
    end

    // data bus

    // for single phase clock: 1 wait state in read op always required!

    reg [1:0] DACK = 0;

    wire WHIT = 1;
    wire DHIT = !((RD) && DACK!=1); // the WR operatio does not need ws. in this config.

    always@(posedge CLK) // stage #1.0
    begin
        DACK <= RES ? 0 : DACK ? DACK-1 : (RD) ? 1 : 0; // wait-states
    end

    always@(posedge CLK) // stage #1.5
    begin
        DATAO <= RES ? 0 : MEM[DADDR[`MLEN-1:2]];
    end

    always@(posedge CLK)
    begin
        // write-only operation w/ 0 wait-states:
        if(!HLT&&WR&&DADDR[31]==0&&/*DADDR[`MLEN-1]==1&&*/BE[3]) MEM[DADDR[`MLEN-1:2]][3 * 8 + 7: 3 * 8] <= DATAI[3 * 8 + 7: 3 * 8];
        if(!HLT&&WR&&DADDR[31]==0&&/*DADDR[`MLEN-1]==1&&*/BE[2]) MEM[DADDR[`MLEN-1:2]][2 * 8 + 7: 2 * 8] <= DATAI[2 * 8 + 7: 2 * 8];
        if(!HLT&&WR&&DADDR[31]==0&&/*DADDR[`MLEN-1]==1&&*/BE[1]) MEM[DADDR[`MLEN-1:2]][1 * 8 + 7: 1 * 8] <= DATAI[1 * 8 + 7: 1 * 8];
        if(!HLT&&WR&&DADDR[31]==0&&/*DADDR[`MLEN-1]==1&&*/BE[0]) MEM[DADDR[`MLEN-1:2]][0 * 8 + 7: 0 * 8] <= DATAI[0 * 8 + 7: 0 * 8];
        XADDR <= RES ? 0 : DADDR; // 1 clock delayed
        //IOMUXFF <= IOMUX[DADDR[4:2]==3'b100 ? 3'b100 : DADDR[3:2]]; // read w/ 2 wait-states
    end

    assign HLT = !DHIT||!WHIT;

endmodule
