module Gates4(
  input  wire [3:0] in_,
  output wire       out_and,
                    out_or,
                    out_xor
);

  // Variables for output ports
  logic __out_and_bits;
  logic __out_or_bits;
  logic __out_xor_bits;

  // @comb update():
  always_comb begin
    __out_and_bits = &in_;
    __out_or_bits = |in_;
    __out_xor_bits = ^in_;
  end // always_comb

  assign out_and = __out_and_bits;
  assign out_or = __out_or_bits;
  assign out_xor = __out_xor_bits;
endmodule
