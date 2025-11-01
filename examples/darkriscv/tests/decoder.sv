module Decoder(
  input  wire        xreset,
                     flush,
  input  wire [31:0] insn,
  output wire        lui,
                     auipc,
                     jal,
                     jalr,
                     bcc,
                     lcc,
                     scc,
                     mcc,
                     rcc,
                     ccc,
  output wire [4:0]  rd_ptr,
                     rs1_ptr,
                     rs2_ptr,
  output wire [6:0]  opcode,
  output wire [2:0]  fct3,
  output wire [6:0]  fct7
);

  // Variables for output ports
  logic             __lui_bits;
  logic             __auipc_bits;
  logic             __jal_bits;
  logic             __jalr_bits;
  logic             __bcc_bits;
  logic             __lcc_bits;
  logic             __scc_bits;
  logic             __mcc_bits;
  logic             __rcc_bits;
  logic             __ccc_bits;
  logic      [4:0]  __rd_ptr_bits;
  logic      [4:0]  __rs1_ptr_bits;
  logic      [4:0]  __rs2_ptr_bits;
  logic      [6:0]  __opcode_bits;
  logic      [2:0]  __fct3_bits;
  logic      [6:0]  __fct7_bits;

  // Local parameters
  localparam [6:0]  LUI = 55;
  localparam [6:0]  AUIPC = 23;
  localparam [6:0]  JAL = 111;
  localparam [6:0]  JALR = 103;
  localparam [6:0]  BCC = 99;
  localparam [6:0]  LCC = 3;
  localparam [6:0]  SCC = 35;
  localparam [6:0]  MCC = 19;
  localparam [6:0]  RCC = 51;
  localparam [6:0]  CCC = 115;

  logic             invalid;
  logic      [31:0] insn_data;
  assign invalid = flush | xreset;
  assign __lui_bits = invalid ? 1'h0 : insn[6:0] == LUI;
  assign __auipc_bits = invalid ? 1'h0 : insn[6:0] == AUIPC;
  assign __jal_bits = invalid ? 1'h0 : insn[6:0] == JAL;
  assign __jalr_bits = invalid ? 1'h0 : insn[6:0] == JALR;
  assign __bcc_bits = invalid ? 1'h0 : insn[6:0] == BCC;
  assign __lcc_bits = invalid ? 1'h0 : insn[6:0] == LCC;
  assign __scc_bits = invalid ? 1'h0 : insn[6:0] == SCC;
  assign __mcc_bits = invalid ? 1'h0 : insn[6:0] == MCC;
  assign __rcc_bits = invalid ? 1'h0 : insn[6:0] == RCC;
  assign __ccc_bits = invalid ? 1'h0 : insn[6:0] == CCC;
  assign insn_data = xreset ? 32'h0 : insn;
  assign __rd_ptr_bits = xreset ? 5'h0 : insn_data[11:7];
  assign __rs1_ptr_bits = insn_data[19:15];
  assign __rs2_ptr_bits = insn_data[24:20];
  assign __opcode_bits = flush ? 7'h0 : insn_data[6:0];
  assign __fct3_bits = insn_data[14:12];
  assign __fct7_bits = insn_data[31:25];

  assign lui = __lui_bits;
  assign auipc = __auipc_bits;
  assign jal = __jal_bits;
  assign jalr = __jalr_bits;
  assign bcc = __bcc_bits;
  assign lcc = __lcc_bits;
  assign scc = __scc_bits;
  assign mcc = __mcc_bits;
  assign rcc = __rcc_bits;
  assign ccc = __ccc_bits;
  assign rd_ptr = __rd_ptr_bits;
  assign rs1_ptr = __rs1_ptr_bits;
  assign rs2_ptr = __rs2_ptr_bits;
  assign opcode = __opcode_bits;
  assign fct3 = __fct3_bits;
  assign fct7 = __fct7_bits;
endmodule
