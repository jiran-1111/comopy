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

module Module_shift(
  input  wire clk,
              d,
  output wire q
);

  // Variables for output ports
  logic __q_bits;

  logic a;
  logic b;

  // s.dff0 = my_dff(s.clk, s.d, s.a)
  my_dff dff0 (
    .clk (clk),
    .d   (d),
    .q   (a)
  );

  // s.dff1 = my_dff(s.clk, s.a, s.b)
  my_dff dff1 (
    .clk (clk),
    .d   (a),
    .q   (b)
  );

  // s.dff2 = my_dff(s.clk, s.b, s.q)
  my_dff dff2 (
    .clk (clk),
    .d   (b),
    .q   (__q_bits)
  );


  assign q = __q_bits;
endmodule
