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

  // @comb update():
  always_comb begin
    w1 = a & b;
    w2 = c & d;
    __out_bits = w1 | w2;
    __out_n_bits = ~__out_bits;
  end // always_comb

  assign out = __out_bits;
  assign out_n = __out_n_bits;
endmodule
