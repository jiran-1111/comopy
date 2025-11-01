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
