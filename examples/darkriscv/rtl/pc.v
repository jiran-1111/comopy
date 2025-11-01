`timescale 1ns / 1ps
`include "./config.vh"

module pc
(
    input         CLK,
    input         XRES,
    input         HLT,
    input         JREQ,
    input  [31:0] JVAL,

    output [31:0] PCO,
    output [31:0] NXPCO
);

    reg [31:0] NXPC;        // 32-bit program counter t+1
    reg [31:0] PC;		    // 32-bit program counter t+0

    assign NXPCO = NXPC;
    assign PCO = PC;

    always@(posedge CLK)
    begin
        NXPC <= XRES ? `__RESETPC__ : HLT ? NXPC : // reset and halt
                JREQ ? JVAL :    // jmp/bra
                       NXPC + 4; // normal flow
        PC   <= /*XRES ? `__RESETPC__ :*/ HLT ? PC : NXPC; // current program counter
    end

endmodule
