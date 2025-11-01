//`define __3STAGE__
//`define __THREADS__ 3
//`define __MAC16X16__
//`define __FLEXBUZZ__
//`define __INTERRUPT__

`define __RESETPC__ 32'd0

//`define __INTERACTIVE__

`define __PERFMETER__

//`define __REGDUMP__
//`define __HARVARD__

`ifdef __HARVARD__
    `define MLEN 13 // MEM[12:0] ->  8KBytes LENGTH = 0x2000
`else
    `define MLEN 12 // MEM[12:0] -> 4KBytes LENGTH = 0x1000
    //`define MLEN 15 // MEM[12:0] -> 32KBytes LENGTH = 0x8000 for coremark!
`endif

//`define __RMW_CYCLE__
//`define __UARTSPEED__ 115200
//`define __UARTQUEUE__
