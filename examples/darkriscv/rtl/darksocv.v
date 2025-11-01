// darksocv
// disable:
//__THREADS__ __3STAGE__ __INTERRUPT__ __FLEXBUZZ__ __HARVARD__
//XILINX_SIMULATOR

`timescale 1ns / 1ps
`include "./config.vh"

module darksocv
(
    input        XCLK,      // external clock
    input        XRES,      // external reset

    input        UART_RXD,  // UART receive line
    output       UART_TXD,  // UART transmit line

    output [3:0] LED,       // on-board leds
    output [3:0] DEBUG      // osciloscope
);

    wire CLK,RES;
    // darkpll darkpll0(.XCLK(XCLK),.XRES(XRES),.CLK(CLK),.RES(RES));
    assign CLK = XCLK;
    assign RES = XRES;

    // darkriscv bus interface

    wire [31:0] IADDR;
    wire [31:0] DADDR;
    wire [31:0] ROMFF;  // comopy: ROMFF from memory
    wire [31:0] DATAO;
    wire [31:0] DATAI;
    wire        WR,RD;
    wire [3:0]  BE;

    wire [31:0] IOMUX [0:4];

    reg  [15:0] GPIOFF = 0;
    reg  [15:0] LEDFF  = 0;

    wire HLT;

    wire [31:0] XADDR;  // comopy: data addr from memory
    wire [31:0] XDATAI; // comopy: data to core

    memory memory0(
        .CLK(CLK),
        .RES(RES),
        .IADDR(IADDR),
        .DADDR(DADDR),
        .XADDR(XADDR),
        .ROMFF(ROMFF),
        .DATAI(DATAO),
        .DATAO(DATAI),

        .WR(WR),
        .RD(RD),
        .BE(BE)
    );

    assign XDATAI = XADDR[31] ? IOMUX[XADDR[4:2]==3'b100 ? 3'b100 : XADDR[3:2]] : DATAI;

    // io for debug

    reg XTIMER = 0;

    // darkuart

    wire [3:0] UDEBUG;

    wire FINISH_REQ;

    // darkriscv

    wire [3:0] KDEBUG;

    wire IDLE;

    darkriscv
    //#(
    //    .RESET_PC(32'h00000000),
    //    .RESET_SP(32'h00002000)
    //)
    core0
    (
        .CLK(CLK),
        .RES(RES),
        //.IDATA(IDATA),
        .ROMFF(ROMFF),
        .IADDR(IADDR),
        .DADDR(DADDR),


        .DATAI(XDATAI),
        .DATAO(DATAO),
        .BE(BE),
        .WR(WR),
        .RD(RD),

        .IDLE(IDLE),
`ifdef SIMULATION
        .HLT(HLT),
`endif
        .DEBUG(KDEBUG)
    );

    assign LED   = LEDFF[3:0];

    assign DEBUG = { XTIMER, KDEBUG[2:0] }; // UDEBUG;

`ifdef SIMULATION

    `ifdef __PERFMETER__

        integer clocks=0, running=0, load=0, store=0, flush=0, halt=0;

        always@(posedge CLK)
        begin
            if(!RES)
            begin
                clocks = clocks+1;

                if(HLT)
                begin
                         if(WR)	store = store+1;
                    else if(RD)	load  = load +1;
                    else 		halt  = halt +1;
                end
                else
                if(IDLE)
                begin
                    flush=flush+1;
                end
                else
                begin
                    running = running +1;
                end

                if(FINISH_REQ)
                begin
                    $display("****************************************************************************");
                    $display("DarkRISCV Pipeline Report (%0d clocks):",clocks);

                    $display("core0: %0d%% run, %0d%% wait (%0d%% i-bus, %0d%% d-bus/rd, %0d%% d-bus/wr), %0d%% idle",
                        100.0*running/clocks,
                        100.0*(load+store+halt)/clocks,
                        100.0*halt/clocks,
                        100.0*load/clocks,
                        100.0*store/clocks,
                        100.0*flush/clocks);

                    $display("****************************************************************************");
                    $finish();
                end
            end
        end
    `else
        always@(posedge CLK) if(FINISH_REQ) $finish();
    `endif

`endif

endmodule
