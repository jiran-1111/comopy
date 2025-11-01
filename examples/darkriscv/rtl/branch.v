`timescale 1ns / 1ps

module branch
(
    input  [2:0]  FCT3,
    input  [31:0] U1REG,
    input  [31:0] S1REG,
    input  [31:0] U2REG,
    input  [31:0] S2REG,
    input  [31:0] U2REGX,
    input  [31:0] S2REGX,
    input  [31:0] DADDR,
    input  [31:0] SIMM,
    input  [31:0] PC,
    input         JAL,
    input         JALR,
    input         BCC,

    output [31:0] PCSIMM,
    output        JREQ,
    output [31:0] JVAL
);

    // J/B-group of instructions (OPCODE==7'b1100011)

    wire BMUX;

    assign BMUX     = FCT3==7 && U1REG>=U2REG  || // bgeu
                      FCT3==6 && U1REG< U2REGX || // bltu
                      FCT3==5 && S1REG>=S2REG  || // bge
                      FCT3==4 && S1REG< S2REGX || // blt
                      FCT3==1 && U1REG!=U2REGX || // bne
                      FCT3==0 && U1REG==U2REGX; // beq

    assign PCSIMM = PC+SIMM;
    assign JREQ = JAL||JALR||(BCC && BMUX);
    assign JVAL = JALR ? DADDR : PCSIMM; // SIMM + (JALR ? U1REG : PC);

endmodule
