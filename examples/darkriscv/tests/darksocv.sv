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

module LSU(
  input  wire [2:0]  fct3,
  input  wire [31:0] data_addr,
                     data_in,
                     rs2_reg,
  output wire [31:0] ld_data,
                     st_data,
  output wire [3:0]  byte_en
);

  // Variables for output ports
  logic [31:0] __ld_data_bits;
  logic [31:0] __st_data_bits;
  logic [3:0]  __byte_en_bits;

  logic [31:0] ld_b;
  logic [31:0] ld_bu;
  logic [31:0] ld_h;
  logic [31:0] ld_hu;
  logic [31:0] ld_w;
  logic [31:0] st_b;
  logic [31:0] st_h;
  logic [31:0] st_w;
  logic [3:0]  be_b;
  logic [3:0]  be_h;
  logic [3:0]  be_w;
  wire  [7:0]  _data_in_31to24 = data_in[31:24];
  wire  [7:0]  _data_in_23to16 = data_in[23:16];
  wire  [7:0]  _data_in_15to8 = data_in[15:8];
  wire  [7:0]  _data_in_7to0 = data_in[7:0];
  assign ld_b =
    (&(data_addr[1:0]))
      ? {{24{_data_in_31to24[7]}}, _data_in_31to24}
      : data_addr[1:0] == 2'h2
          ? {{24{_data_in_23to16[7]}}, _data_in_23to16}
          : data_addr[1:0] == 2'h1
              ? {{24{_data_in_15to8[7]}}, _data_in_15to8}
              : {{24{_data_in_7to0[7]}}, _data_in_7to0};
  assign ld_bu =
    (&(data_addr[1:0]))
      ? {24'h0, data_in[31:24]}
      : data_addr[1:0] == 2'h2
          ? {24'h0, data_in[23:16]}
          : data_addr[1:0] == 2'h1 ? {24'h0, data_in[15:8]} : {24'h0, data_in[7:0]};
  wire  [15:0] _data_in_31to16 = data_in[31:16];
  wire  [15:0] _data_in_15to0 = data_in[15:0];
  assign ld_h =
    (&(data_addr[1]))
      ? {{16{_data_in_31to16[15]}}, _data_in_31to16}
      : {{16{_data_in_15to0[15]}}, _data_in_15to0};
  assign ld_hu = (&(data_addr[1])) ? {16'h0, data_in[31:16]} : {16'h0, data_in[15:0]};
  assign ld_w = data_in;
  assign __ld_data_bits =
    fct3 == 3'h0
      ? ld_b
      : fct3 == 3'h1 ? ld_h : fct3 == 3'h4 ? ld_bu : fct3 == 3'h5 ? ld_hu : ld_w;
  assign st_b =
    (&(data_addr[1:0]))
      ? {rs2_reg[7:0], 24'h0}
      : data_addr[1:0] == 2'h2
          ? {8'h0, rs2_reg[7:0], 16'h0}
          : data_addr[1:0] == 2'h1 ? {16'h0, rs2_reg[7:0], 8'h0} : {24'h0, rs2_reg[7:0]};
  assign st_h = (&(data_addr[1])) ? {rs2_reg[15:0], 16'h0} : {16'h0, rs2_reg[15:0]};
  assign st_w = rs2_reg;
  assign __st_data_bits = fct3 == 3'h0 ? st_b : fct3 == 3'h1 ? st_h : st_w;
  assign be_b =
    (&(data_addr[1:0]))
      ? 4'h8
      : data_addr[1:0] == 2'h2 ? 4'h4 : data_addr[1:0] == 2'h1 ? 4'h2 : 4'h1;
  assign be_h = data_addr[1] ? 4'hC : 4'h3;
  assign be_w = 4'hF;
  assign __byte_en_bits =
    fct3 == 3'h0 | fct3 == 3'h4 ? be_b : fct3 == 3'h1 | fct3 == 3'h5 ? be_h : be_w;

  assign ld_data = __ld_data_bits;
  assign st_data = __st_data_bits;
  assign byte_en = __byte_en_bits;
endmodule

module PC(
  input  wire        clk,
                     xreset,
                     halt,
                     jreq,
  input  wire [31:0] jval,
  output wire [31:0] pc,
                     next_pc
);

  // Variables for output ports
  logic      [31:0] __pc_bits;
  logic      [31:0] __next_pc_bits;

  // Local parameters
  localparam [31:0] RESET_PC = 0;

  // @seq update_pc():
  always @(posedge clk) begin
    if (xreset) begin
      __next_pc_bits <= RESET_PC;
      __pc_bits <= RESET_PC;
    end
    else begin
      __next_pc_bits <= halt ? __next_pc_bits : jreq ? jval : __next_pc_bits + 32'h4;
      __pc_bits <= halt ? __pc_bits : __next_pc_bits;
    end
  end // always @(posedge)

  assign pc = __pc_bits;
  assign next_pc = __next_pc_bits;
endmodule

module DarkRiscv(
  input  wire        clk,
                     reset,
  input  wire [31:0] insn_data,
  output wire [31:0] insn_addr,
  input  wire [31:0] data_in,
  output wire [31:0] data_out,
                     data_addr,
  output wire        write,
                     read,
  output wire [3:0]  byte_en,
  output wire        idle,
  output wire [3:0]  debug
);

  wire  [31:0] _lsu_ld_data;
  wire  [31:0] _branch_pc_simm;
  wire  [31:0] _branch_jval;
  wire  [31:0] _alu_result;
  wire  [31:0] _imm_simm;
  wire  [31:0] _imm_uimm;
  wire         _dec_lui;
  wire         _dec_auipc;
  wire         _dec_jal;
  wire         _dec_jalr;
  wire         _dec_bcc;
  wire         _dec_lcc;
  wire         _dec_scc;
  wire         _dec_mcc;
  wire         _dec_rcc;
  wire  [2:0]  _dec_fct3;
  wire  [6:0]  _dec_fct7;
  // Variables for output ports
  logic [31:0] __insn_addr_bits;
  logic [31:0] __data_out_bits;
  logic [31:0] __data_addr_bits;
  logic        __write_bits;
  logic        __read_bits;
  logic [3:0]  __byte_en_bits;
  logic        __idle_bits;
  logic [3:0]  __debug_bits;

  logic        xreset;
  logic        flush;
  logic        dack;
  logic        halt;
  logic        halt2;
  logic [31:0] insn2;
  logic [31:0] insn;
  logic [31:0] pc;
  logic        jreq;
  logic [31:0] regs[0:31];
  logic [4:0]  rd_ptr;
  logic [4:0]  rs1_ptr;
  logic [4:0]  rs2_ptr;
  logic [31:0] rd_reg;
  logic [31:0] rd_data;
  logic [31:0] rs1_reg;
  logic [31:0] rs2_reg;

  Decoder dec (
    .xreset  (xreset),
    .flush   (flush),
    .insn    (insn),
    .lui     (_dec_lui),
    .auipc   (_dec_auipc),
    .jal     (_dec_jal),
    .jalr    (_dec_jalr),
    .bcc     (_dec_bcc),
    .lcc     (_dec_lcc),
    .scc     (_dec_scc),
    .mcc     (_dec_mcc),
    .rcc     (_dec_rcc),
    .ccc     (/* unused */),
    .rd_ptr  (rd_ptr),
    .rs1_ptr (rs1_ptr),
    .rs2_ptr (rs2_ptr),
    .opcode  (/* unused */),
    .fct3    (_dec_fct3),
    .fct7    (_dec_fct7)
  );

  logic [31:0] s2_regx;
  logic [31:0] u2_regx;

  Immediate imm (
    .xreset (xreset),
    .insn   (insn),
    .simm   (_imm_simm),
    .uimm   (_imm_uimm)
  );

  ALU alu (
    .rcc     (_dec_rcc),
    .fct3    (_dec_fct3),
    .fct7    (_dec_fct7),
    .rs1     (rs1_reg),
    .s2_regx (s2_regx),
    .u2_regx (u2_regx),
    .result  (_alu_result)
  );

  Branch branch (
    .fct3      (_dec_fct3),
    .rs1       (rs1_reg),
    .rs2       (rs2_reg),
    .simm      (_imm_simm),
    .data_addr (__data_addr_bits),
    .pc        (pc),
    .jal       (_dec_jal),
    .jalr      (_dec_jalr),
    .bcc       (_dec_bcc),
    .pc_simm   (_branch_pc_simm),
    .jreq      (jreq),
    .jval      (_branch_jval)
  );

  LSU lsu (
    .fct3      (_dec_fct3),
    .data_addr (__data_addr_bits),
    .data_in   (data_in),
    .rs2_reg   (rs2_reg),
    .ld_data   (_lsu_ld_data),
    .st_data   (__data_out_bits),
    .byte_en   (__byte_en_bits)
  );

  PC pc_gen (
    .clk     (clk),
    .xreset  (xreset),
    .halt    (halt),
    .jreq    (jreq),
    .jval    (_branch_jval),
    .pc      (pc),
    .next_pc (__insn_addr_bits)
  );

  assign insn = halt2 ? insn2 : insn_data;
  assign __idle_bits = flush;
  assign rd_reg = regs[rd_ptr];
  assign rs1_reg = regs[rs1_ptr];
  assign rs2_reg = regs[rs2_ptr];
  assign s2_regx = _dec_mcc ? _imm_simm : rs2_reg;
  assign u2_regx = _dec_mcc ? _imm_uimm : rs2_reg;
  assign __read_bits = _dec_lcc;
  assign __write_bits = _dec_scc;
  assign halt = __read_bits & ~dack;
  assign __data_addr_bits = rs1_reg + _imm_simm;
  assign rd_data =
    _dec_lcc
      ? _lsu_ld_data
      : _dec_auipc
          ? _branch_pc_simm
          : _dec_jal | _dec_jalr
              ? __insn_addr_bits
              : _dec_lui ? _imm_simm : _dec_mcc | _dec_rcc ? _alu_result : rd_reg;
  assign __debug_bits = {xreset, __idle_bits, _dec_scc, _dec_lcc};

  // @seq update_states():
  always @(posedge clk) begin
    xreset <= reset;
    if (xreset)
      dack <= 1'h0;
    else
      dack <= dack ? 1'h0 : __read_bits ? 1'h1 : 1'h0;
    if (halt ^ halt2)
      insn2 <= insn_data;
    halt2 <= halt;
    flush <= xreset ? 1'h1 : halt ? flush : jreq;
  end // always @(posedge)

  // @seq update_regs():
  always @(posedge clk) begin
    if (xreset) begin
      for (logic [31:0] i = 32'h0; i < 32'h20; i += 32'h1) begin
        regs[i] <= 32'h0;
      end
    end
    else
      regs[rd_ptr] <= (xreset | (|rd_ptr)) == 1'h0 ? 32'h0 : halt ? rd_reg : rd_data;
  end // always @(posedge)

  assign insn_addr = __insn_addr_bits;
  assign data_out = __data_out_bits;
  assign data_addr = __data_addr_bits;
  assign write = __write_bits;
  assign read = __read_bits;
  assign byte_en = __byte_en_bits;
  assign idle = __idle_bits;
  assign debug = __debug_bits;
endmodule

module Memory(
  input  wire        clk,
                     reset,
  input  wire [31:0] insn_addr,
                     data_addr,
                     data_in,
  input  wire        write,
                     read,
  input  wire [3:0]  byte_en,
  output wire [31:0] mem_waddr,
                     insn_data,
                     data_out,
  output wire        halt
);

  // Variables for output ports
  logic      [31:0] __mem_waddr_bits;
  logic      [31:0] __insn_data_bits;
  logic      [31:0] __data_out_bits;
  logic             __halt_bits;

  // Local parameters
  localparam [31:0] MLEN = 13;

  logic      [31:0] mem[0:2047];
  logic             d_ack;
  logic             d_hit;
  logic             w_hit;
  assign d_hit = ~(read & d_ack != 1'h1);
  assign w_hit = 1'h1;
  assign __halt_bits = ~d_hit | ~w_hit;

  // @seq insn_bus():
  always @(posedge clk)
    __insn_data_bits <= reset ? 32'h0 : mem[insn_addr[12:2]];

  // @seq update_dack():
  always @(posedge clk)
    d_ack <= reset ? 1'h0 : read ? 1'h1 : 1'h0;

  // @seq read_data():
  always @(posedge clk)
    __data_out_bits <= reset ? 32'h0 : mem[data_addr[12:2]];

  // @seq write_data():
  always @(posedge clk) begin
    for (logic [31:0] i = 32'h0; i < 32'h4; i += 32'h1) begin
      if (~__halt_bits & write & data_addr[31] == 1'h0 & byte_en[i +: 1])
        mem[data_addr[12:2]][i * 32'h8 +: 8] <= data_in[i * 32'h8 +: 8];
    end
    __mem_waddr_bits <= reset ? 32'h0 : data_addr;
  end // always @(posedge)

  assign mem_waddr = __mem_waddr_bits;
  assign insn_data = __insn_data_bits;
  assign data_out = __data_out_bits;
  assign halt = __halt_bits;
endmodule

module DarkSocv(
  input  wire       clk,
                    reset,
  output wire [3:0] debug
);

  wire  [31:0] _core_insn_addr;
  wire  [31:0] _core_data_out;
  wire  [31:0] _core_data_addr;
  wire         _core_write;
  wire         _core_read;
  wire  [3:0]  _core_byte_en;
  wire  [3:0]  _core_debug;
  // Variables for output ports
  logic [3:0]  __debug_bits;

  logic [31:0] xaddr;
  logic [31:0] xdata_in;

  logic [31:0] _core_insn_data;
  logic [31:0] _core_data_in;
  DarkRiscv core (
    .clk       (clk),
    .reset     (reset),
    .insn_data (_core_insn_data),
    .insn_addr (_core_insn_addr),
    .data_in   (_core_data_in),
    .data_out  (_core_data_out),
    .data_addr (_core_data_addr),
    .write     (_core_write),
    .read      (_core_read),
    .byte_en   (_core_byte_en),
    .idle      (/* unused */),
    .debug     (_core_debug)
  );

  Memory memory (
    .clk       (clk),
    .reset     (reset),
    .insn_addr (_core_insn_addr),
    .data_addr (_core_data_addr),
    .data_in   (_core_data_out),
    .write     (_core_write),
    .read      (_core_read),
    .byte_en   (_core_byte_en),
    .mem_waddr (xaddr),
    .insn_data (_core_insn_data),
    .data_out  (xdata_in),
    .halt      (/* unused */)
  );

  assign _core_data_in = xdata_in;
  assign __debug_bits = {1'h0, _core_debug[2:0]};

  assign debug = __debug_bits;
endmodule
