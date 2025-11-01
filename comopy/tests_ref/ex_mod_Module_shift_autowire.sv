module my_dff(
  input  wire clk,
              d,
  output wire q
);

  // Variables for output ports
  logic __q_bits;

  assign __q_bits = d;

  assign q = __q_bits;
endmodule

module Module_shift_autowire(
  input  wire clk,
              d,
  output wire q
);

  wire  _dff1_q;
  wire  _dff0_q;
  // Variables for output ports
  logic __q_bits;

  // s.dff0 = my_dff(clk=s.clk, d=s.d)
  my_dff dff0 (
    .clk (clk),
    .d   (d),
    .q   (_dff0_q)
  );

  // s.dff1 = my_dff(s.clk, s.dff0.q)
  my_dff dff1 (
    .clk (clk),
    .d   (_dff0_q),
    .q   (_dff1_q)
  );

  // s.dff2 = my_dff(s.clk, s.dff1.q, s.q)
  my_dff dff2 (
    .clk (clk),
    .d   (_dff1_q),
    .q   (__q_bits)
  );

  assign q = __q_bits;
endmodule
