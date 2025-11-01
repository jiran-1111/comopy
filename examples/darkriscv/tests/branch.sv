module Branch(
  input  wire [2:0]  fct3,
  input  wire [31:0] rs1,
                     rs2,
                     simm,
                     data_addr,
                     pc,
  input  wire        jal,
                     jalr,
                     bcc,
  output wire [31:0] pc_simm,
  output wire        jreq,
  output wire [31:0] jval
);

  // Variables for output ports
  logic      [31:0] __pc_simm_bits;
  logic             __jreq_bits;
  logic      [31:0] __jval_bits;

  // Local parameters
  localparam [2:0]  GEU = 7;
  localparam [2:0]  LTU = 6;
  localparam [2:0]  GE = 5;
  localparam [2:0]  LT = 4;
  localparam [2:0]  NE = 1;
  localparam [2:0]  EQ = 0;

  logic             bmux;
  assign bmux =
    fct3 == GEU & rs1 >= rs2 | fct3 == LTU & rs1 < rs2 | fct3 == GE
    & $signed(rs1) >= $signed(rs2) | fct3 == LT & $signed(rs1) < $signed(rs2) | fct3 == NE
    & rs1 != rs2 | fct3 == EQ & rs1 == rs2;
  assign __pc_simm_bits = pc + simm;
  assign __jreq_bits = jal | jalr | bcc & bmux;
  assign __jval_bits = jalr ? data_addr : __pc_simm_bits;

  assign pc_simm = __pc_simm_bits;
  assign jreq = __jreq_bits;
  assign jval = __jval_bits;
endmodule
