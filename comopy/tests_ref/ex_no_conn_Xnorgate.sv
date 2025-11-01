module Xnorgate(
  input  wire a,
              b,
  output wire out
);

  // Variables for output ports
  logic __out_bits;

  // @comb update():
  always_comb
    __out_bits = ~(a ^ b);

  assign out = __out_bits;
endmodule
