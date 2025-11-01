module mod_a2(
  output wire out1,
              out2,
  input  wire in1,
              in2,
              in3,
              in4
);

  // Variables for output ports
  logic __out1_bits;
  logic __out2_bits;

  assign __out1_bits = in1 & in2;
  assign __out2_bits = in3 | in4;

  assign out1 = __out1_bits;
  assign out2 = __out2_bits;
endmodule

module Module_name(
  input  wire a,
              b,
              c,
              d,
  output wire out1,
              out2
);

  // Variables for output ports
  logic __out1_bits;
  logic __out2_bits;

  // s.inst = mod_a2(
  mod_a2 inst (
    .out1 (__out1_bits),
    .out2 (__out2_bits),
    .in1  (a),
    .in2  (b),
    .in3  (c),
    .in4  (d)
  );

  assign out1 = __out1_bits;
  assign out2 = __out2_bits;
endmodule
