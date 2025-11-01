module ALU(
  input  wire        rcc,
  input  wire [2:0]  fct3,
  input  wire [6:0]  fct7,
  input  wire [31:0] rs1,
                     s2_regx,
                     u2_regx,
  output wire [31:0] result
);

  // Variables for output ports
  logic      [31:0] __result_bits;

  // Local parameters
  localparam [2:0]  ADD = 0;
  localparam [2:0]  SLL = 1;
  localparam [2:0]  SLT = 2;
  localparam [2:0]  SLTU = 3;
  localparam [2:0]  XOR = 4;
  localparam [2:0]  SRX = 5;
  localparam [2:0]  OR = 6;

  logic      [31:0] d_add;
  logic      [31:0] d_sll;
  logic      [31:0] d_slt;
  logic      [31:0] d_sltu;
  logic      [31:0] d_xor;
  logic      [31:0] d_srx;
  logic      [31:0] d_or;
  logic      [31:0] d_and;
  assign d_add = rcc & fct7[5] ? rs1 - s2_regx : rs1 + s2_regx;
  assign d_sll = rs1 << u2_regx[4:0];
  assign d_slt = {31'h0, $signed(rs1) < $signed(s2_regx)};
  assign d_sltu = {31'h0, rs1 < s2_regx};
  assign d_xor = rs1 ^ s2_regx;
  assign d_srx = fct7[5] ? $signed($signed(rs1) >>> u2_regx[4:0]) : rs1 >> u2_regx[4:0];
  assign d_or = rs1 | s2_regx;
  assign d_and = rs1 & s2_regx;
  assign __result_bits =
    fct3 == ADD
      ? d_add
      : fct3 == SLL
          ? d_sll
          : fct3 == SLT
              ? d_slt
              : fct3 == SLTU
                  ? d_sltu
                  : fct3 == XOR ? d_xor : fct3 == SRX ? d_srx : fct3 == OR ? d_or : d_and;

  assign result = __result_bits;
endmodule
