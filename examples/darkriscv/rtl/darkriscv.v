`timescale 1ns / 1ps

module darkriscv
//#(
//    parameter [31:0] RESET_PC = 0,
//    parameter [31:0] RESET_SP = 4096
//)
(
    input             CLK,   // clock
    input             RES,   // reset

    //input      [31:0] IDATA, // instruction data bus
    input      [31:0] ROMFF, //
    output     [31:0] IADDR, // instruction addr bus

    input      [31:0] DATAI, // data bus (input)
    output     [31:0] DATAO, // data bus (output)
    output     [31:0] DADDR, // addr bus

    output     [ 3:0] BE,   // byte enable
    output            WR,    // write enable
    output            RD,    // read enable

    output            IDLE,   // idle output
    output            HLT,

    output [3:0]  DEBUG       // old-school osciloscope based debug! :)
);

    reg XRES = 1;

    // instruction bus

    reg [31:0] ROMFF2 = 0;
    reg        HLT2   = 0;

    always@(posedge CLK) // stage #0.5
    begin
        if(HLT^HLT2)
        begin
            ROMFF2 <= ROMFF;
        end

        HLT2 <= HLT;
    end

    wire[31:0] IDATA;
    assign IDATA = HLT2 ? ROMFF2 : ROMFF;

    wire [31:0] XSIMM;
    wire [31:0] XUIMM;

    ext ext_0
    (
        .RES(XRES),
        .IDATA(IDATA),

        .SIMM(XSIMM),
        .UIMM(XUIMM)
    );

    reg FLUSH = -1;  // flush instruction pipeline

    wire        LUI, AUIPC, JAL, JALR, BCC, LCC, SCC, MCC, RCC, CUS, CCC;//FC;
    wire [4:0]  DPTR, S1PTR, S2PTR;
    wire [6:0]  OPCODE;
    wire [2:0]  FCT3;
    wire [6:0]  FCT7;

    decode decode_0
    (
        .XRES(XRES),
        .FLUSH(FLUSH),
        .IDATA(IDATA),

        .LUI(LUI),
        .AUIPC(AUIPC),
        .JAL(JAL),
        .JALR(JALR),
        .BCC(BCC),
        .LCC(LCC),
        .SCC(SCC),
        .MCC(MCC),
        .RCC(RCC),
        .CUS(CUS),
        .CCC(CCC),

        .DPTR(DPTR),
        .S1PTR(S1PTR),
        .S2PTR(S2PTR),
        .OPCODE(OPCODE),
        .FCT3(FCT3),
        .FCT7(FCT7)
    );

    wire [31:0] SIMM  = XSIMM;
    wire [31:0] UIMM  = XUIMM;

    reg  [31:0] REGS [0:31]; // general-purpose 32x32-bit registers (s1)

    wire [31:0] NXPC;        // 32-bit program counter t+1
    wire [31:0] PC;		    // 32-bit program counter t+0

    // source-1 and source-2 register selection

    wire          [31:0] U1REG = REGS[S1PTR];
    wire          [31:0] U2REG = REGS[S2PTR];

    wire signed   [31:0] S1REG = U1REG;
    wire signed   [31:0] S2REG = U2REG;

    // L-group of instructions (OPCODE==7'b0000011)
    // S-group of instructions (OPCODE==7'b0100011)

    wire [31:0] LDATA;
    wire [31:0] SDATA;

    lsu lsu_0
    (
        .FCT3(FCT3),
        .DADDR(DADDR),
        .DATAI(DATAI),
        .U2REG(U2REG),

        .LDATA(LDATA),
        .SDATA(SDATA),
        .BE(BE)
    );

    // C-group: CSRRW

    wire EBRK = CCC && FCT3==0 && S2PTR==1;

    // RM-group of instructions (OPCODEs==7'b0010011/7'b0110011), merged! src=immediate(M)/register(R)

    wire signed [31:0] S2REGX = MCC ? SIMM : S2REG;
    wire        [31:0] U2REGX = MCC ? UIMM : U2REG;

    wire [31:0] RMDATA;

    alu alu_0
    (

        .RCC(RCC),
        .FCT3(FCT3),
        .FCT7(FCT7),
        .U1REG(U1REG),
        .S1REG(S1REG),
        .U2REGX(U2REGX),
        .S2REGX(S2REGX),

        .RMDATA(RMDATA)
    );

    // J/B-group of instructions (OPCODE==7'b1100011)

    wire [31:0] PCSIMM;
    wire        JREQ;
    wire [31:0] JVAL;

    branch branch_0
    (
        .FCT3(FCT3),
        .U1REG(U1REG),
        .S1REG(S1REG),
        .U2REG(U2REG),
        .S2REG(S2REG),
        .U2REGX(U2REGX),
        .S2REGX(S2REGX),
        .DADDR(DADDR),
        .SIMM(SIMM),
        .PC(PC),
        .JAL(JAL),
        .JALR(JALR),
        .BCC(BCC),

        .PCSIMM(PCSIMM),
        .JREQ(JREQ),
        .JVAL(JVAL)
    );

    pc pc_0
    (
        .CLK(CLK),
        .XRES(XRES),
        .HLT(HLT),
        .JREQ(JREQ),
        .JVAL(JVAL),
        .PCO(PC),
        .NXPCO(NXPC)
    );

    always@(posedge CLK)
    begin
        XRES <= RES;

        FLUSH <= XRES ? 1 : HLT ? FLUSH :        // reset and halt
                       JREQ;  // flush the pipeline!
    end

    always@(posedge CLK)
    begin
        if(XRES)
        begin
            for(int i =0;i<32;i=i+1)
            begin
                REGS[i] <= 0;
            end
        end
        else
        begin
            REGS[DPTR] <=   XRES||DPTR[4:0] == 0 ? 0 :  // reset sp
                            HLT ? REGS[DPTR] :          // halt
                            LCC ? LDATA :
                            AUIPC ? PCSIMM :
                            JAL||JALR ? NXPC :
                            LUI ? SIMM :
                            MCC||RCC ? RMDATA :
                            REGS[DPTR];
        end
    end

    reg DACK;

    always@(posedge CLK)
    begin
        if(XRES)
        begin
            DACK <= 0;
        end
        else if(DACK)
        begin
            DACK <= 0;
        end
        else if(RD)
        begin
            DACK <= 1;
        end
        else
            DACK <= 0;
    end

    assign HLT = RD && !DACK;

    // IO and memory interface

    assign DATAO = SDATA; // SCC ? SDATA : 0;
    assign DADDR = U1REG + SIMM; // (SCC||LCC) ? U1REG + SIMM : 0;

    // based in the Scc and Lcc

    assign RD = LCC;
    assign WR = SCC;

    assign IADDR = NXPC;

    assign IDLE = |FLUSH;

    assign DEBUG = { XRES, IDLE, SCC, LCC };

endmodule
