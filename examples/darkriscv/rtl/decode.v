`timescale 1ns / 1ps
`include "./define.vh"

module decode
(
    input        XRES,
    input        FLUSH,
    input [31:0] IDATA,

    output       LUI,
    output       AUIPC,
    output       JAL,
    output       JALR,
    output       BCC,
    output       LCC,
    output       SCC,
    output       MCC,

    output       RCC,
    output       CUS,
    output       CCC,

    output [4:0] DPTR,
    output [4:0] S1PTR,
    output [4:0] S2PTR,
    output [6:0] OPCODE,
    output [2:0] FCT3,
    output [6:0] FCT7
);

    // decode: IDATA is break apart as described in the RV32I specification

    wire [31:0] XIDATA;

    assign XIDATA = XRES ? 0 : IDATA;

    // main opcode decoder:

    assign LUI      = FLUSH||XRES ? 0 : IDATA[6:0]==`LUI;   //OPCODE==7'b0110111;
    assign AUIPC    = FLUSH||XRES ? 0 : IDATA[6:0]==`AUIPC; //OPCODE==7'b0010111;
    assign JAL      = FLUSH||XRES ? 0 : IDATA[6:0]==`JAL;   //OPCODE==7'b1101111;
    assign JALR     = FLUSH||XRES ? 0 : IDATA[6:0]==`JALR;  //OPCODE==7'b1100111;

    assign BCC      = FLUSH||XRES ? 0 : IDATA[6:0]==`BCC;   //OPCODE==7'b1100011; // FCT3
    assign LCC      = FLUSH||XRES ? 0 : IDATA[6:0]==`LCC;   //OPCODE==7'b0000011; // FCT3
    assign SCC      = FLUSH||XRES ? 0 : IDATA[6:0]==`SCC;   //OPCODE==7'b0100011; // FCT3
    assign MCC      = FLUSH||XRES ? 0 : IDATA[6:0]==`MCC;   //OPCODE==7'b0010011; // FCT3

    assign RCC      = FLUSH||XRES ? 0 : IDATA[6:0]==`RCC;   //OPCODE==7'b0110011; // FCT3
    assign CUS      = FLUSH||XRES ? 0 : IDATA[6:0]==`CUS;   //OPCODE==7'b0001011; // FCT3
    // assign FCC      = FLUSH||XRES ? 0 : IDATA[6:0]==`FCC;   //OPCODE==7'b0001111; // FCT3
    assign CCC      = FLUSH||XRES ? 0 : IDATA[6:0]==`CCC;   //OPCODE==7'b1110011; // FCT3

    assign DPTR   = XRES ? 0 : XIDATA[11: 7]; // set SP_RESET when RES==1
    assign S1PTR  = XIDATA[19:15];
    assign S2PTR  = XIDATA[24:20];

    assign OPCODE = FLUSH ? 0 : XIDATA[6:0];
    assign FCT3   = XIDATA[14:12];
    assign FCT7   = XIDATA[31:25];

endmodule
