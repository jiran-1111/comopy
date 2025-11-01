`timescale 1ns / 1ps

module alu
(
    input         RCC,
    input  [2:0]  FCT3,
    input  [6:0]  FCT7,
    input  [31:0] U1REG,
    input  [31:0] S1REG,
    input  [31:0] U2REGX,
    input  [31:0] S2REGX,

    output [31:0] RMDATA
);

    // RM-group of instructions (OPCODEs==7'b0010011/7'b0110011), merged!
    // src=immediate(M)/register(R)

    assign RMDATA = FCT3==7 ? U1REG&S2REGX :
                    FCT3==6 ? U1REG|S2REGX :
                    FCT3==4 ? U1REG^S2REGX :
                    FCT3==3 ? U1REG<U2REGX : // unsigned
                    FCT3==2 ? S1REG<S2REGX : // signed
                    FCT3==0 ? (RCC&&FCT7[5] ? U1REG-S2REGX : U1REG+S2REGX) :
                    FCT3==1 ? S1REG<<U2REGX[4:0] :
                    //FCT3==5 ?
                    !FCT7[5] ? S1REG>>U2REGX[4:0] :
                               $signed(S1REG)>>>U2REGX[4:0];  // (FCT7[5] ? U1REG>>>U2REG[4:0] :

endmodule
