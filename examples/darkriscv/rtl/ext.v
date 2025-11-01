`timescale 1ns / 1ps
`include "./define.vh"

module ext
(
    input         RES,
    input  [31:0] IDATA,
    output [31:0] SIMM,
    output [31:0] UIMM
);

    wire [31:0] ALL0 = 0;
    wire [31:0] ALL1 = -1;

    // signed extended immediate, according to the instruction type:

    assign SIMM  = RES ? 0 :
                IDATA[6:0]==`SCC ? { IDATA[31] ? ALL1[31:12]:ALL0[31:12], IDATA[31:25],IDATA[11:7] } : // s-type
                IDATA[6:0]==`BCC ? { IDATA[31] ? ALL1[31:13]:ALL0[31:13], IDATA[31],IDATA[7],IDATA[30:25],IDATA[11:8],ALL0[0] } : // b-type
                IDATA[6:0]==`JAL ? { IDATA[31] ? ALL1[31:21]:ALL0[31:21], IDATA[31], IDATA[19:12], IDATA[20], IDATA[30:21], ALL0[0] } : // j-type
                IDATA[6:0]==`LUI||
                IDATA[6:0]==`AUIPC ? { IDATA[31:12], ALL0[11:0] } : // u-type
                                        { IDATA[31] ? ALL1[31:12]:ALL0[31:12], IDATA[31:20] }; // i-type

    // unsigned extended immediate, according to the instruction type:

    assign UIMM  = RES ? 0:
                IDATA[6:0]==`SCC ? { ALL0[31:12], IDATA[31:25],IDATA[11:7] } : // s-type
                IDATA[6:0]==`BCC ? { ALL0[31:13], IDATA[31],IDATA[7],IDATA[30:25],IDATA[11:8],ALL0[0] } : // b-type
                IDATA[6:0]==`JAL ? { ALL0[31:21], IDATA[31], IDATA[19:12], IDATA[20], IDATA[30:21], ALL0[0] } : // j-type
                IDATA[6:0]==`LUI||
                IDATA[6:0]==`AUIPC ? { IDATA[31:12], ALL0[11:0] } : // u-type
                                        { ALL0[31:12], IDATA[31:20] }; // i-type

endmodule
