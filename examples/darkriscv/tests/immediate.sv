module Immediate(
  input  wire        xreset,
  input  wire [31:0] insn,
  output wire [31:0] simm,
                     uimm
);

  // Variables for output ports
  logic      [31:0] __simm_bits;
  logic      [31:0] __uimm_bits;

  // Local parameters
  localparam [6:0]  SCC = 35;
  localparam [6:0]  BCC = 99;
  localparam [6:0]  JAL = 111;
  localparam [6:0]  LUI = 55;
  localparam [6:0]  AUIPC = 23;

  logic      [31:0] simm_i;
  logic      [31:0] simm_s;
  logic      [31:0] simm_b;
  logic      [31:0] simm_j;
  logic      [31:0] simm_u;
  logic      [31:0] uimm_i;
  logic      [31:0] uimm_s;
  logic      [31:0] uimm_b;
  logic      [31:0] uimm_j;
  logic      [31:0] uimm_u;
  assign simm_i = {{20{insn[31]}}, insn[31:20]};
  assign simm_s = {{20{insn[31]}}, insn[31:25], insn[11:7]};
  assign simm_b = {{19{insn[31]}}, insn[31], insn[7], insn[30:25], insn[11:8], 1'h0};
  assign simm_j = {{11{insn[31]}}, insn[31], insn[19:12], insn[20], insn[30:21], 1'h0};
  assign simm_u = {insn[31:12], 12'h0};
  assign __simm_bits =
    xreset
      ? 32'h0
      : insn[6:0] == SCC
          ? simm_s
          : insn[6:0] == BCC
              ? simm_b
              : insn[6:0] == JAL
                  ? simm_j
                  : insn[6:0] == LUI | insn[6:0] == AUIPC ? simm_u : simm_i;
  assign uimm_i = {20'h0, insn[31:20]};
  assign uimm_s = {20'h0, insn[31:25], insn[11:7]};
  assign uimm_b = {19'h0, insn[31], insn[7], insn[30:25], insn[11:8], 1'h0};
  assign uimm_j = {11'h0, insn[31], insn[19:12], insn[20], insn[30:21], 1'h0};
  assign uimm_u = {insn[31:12], 12'h0};
  assign __uimm_bits =
    xreset
      ? 32'h0
      : insn[6:0] == SCC
          ? uimm_s
          : insn[6:0] == BCC
              ? uimm_b
              : insn[6:0] == JAL
                  ? uimm_j
                  : insn[6:0] == LUI | insn[6:0] == AUIPC ? uimm_u : uimm_i;

  assign simm = __simm_bits;
  assign uimm = __uimm_bits;
endmodule
