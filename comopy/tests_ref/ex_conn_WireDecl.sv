module WireDecl(
  input  wire a,
              b,
              c,
              d,
  output wire out,
              out_n
);

  // Variables for output ports
  logic __out_bits;
  logic __out_n_bits;

  logic w1;
  logic w2;
  assign w1 = a & b;
  assign w2 = c & d;
  assign __out_bits = w1 | w2;
  assign __out_n_bits = ~__out_bits;

  assign out = __out_bits;
  assign out_n = __out_n_bits;
endmodule
