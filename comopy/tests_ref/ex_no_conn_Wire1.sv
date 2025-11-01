module Wire1(
  input  wire in_,
  output wire out
);

  // Variables for output ports
  logic __out_bits;

  // @comb update():
  always_comb
    __out_bits = in_;

  assign out = __out_bits;
endmodule
