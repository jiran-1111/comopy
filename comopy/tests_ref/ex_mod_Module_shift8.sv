module my_dff8(
  input  wire       clk,
  input  wire [7:0] d,
  output wire [7:0] q
);

  // Variables for output ports
  logic [7:0] __q_bits;

  // @seq update_ff():
  always @(posedge clk)
    __q_bits <= d;

  assign q = __q_bits;
endmodule

module Module_shift8(
  input  wire       clk,
  input  wire [7:0] d,
  input  wire [1:0] sel,
  output wire [7:0] q
);

  wire  [7:0] _dff2_q;
  wire  [7:0] _dff1_q;
  wire  [7:0] _dff0_q;
  // Variables for output ports
  logic [7:0] __q_bits;

  // s.dff0 = my_dff8(s.d)
  my_dff8 dff0 (
    .clk (clk),
    .d   (d),
    .q   (_dff0_q)
  );

  // s.dff1 = my_dff8(s.dff0.q)
  my_dff8 dff1 (
    .clk (clk),
    .d   (_dff0_q),
    .q   (_dff1_q)
  );

  // s.dff2 = my_dff8(s.dff1.q)
  my_dff8 dff2 (
    .clk (clk),
    .d   (_dff1_q),
    .q   (_dff2_q)
  );

  // @comb update():
  always_comb begin
    unique case (sel)
      2'b00:
        __q_bits = d;
      2'b01:
        __q_bits = _dff0_q;
      2'b10:
        __q_bits = _dff1_q;
      2'b11:
        __q_bits = _dff2_q;
    endcase
  end // always_comb

  assign q = __q_bits;
endmodule
