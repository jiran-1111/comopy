module Gates100(
  input  wire [99:0] in_,
  output wire        out_and,
                     out_or,
                     out_xor
);

  // Variables for output ports
  logic __out_and_bits;
  logic __out_or_bits;
  logic __out_xor_bits;

  assign __out_and_bits = in_ == {100{1'h1}};
  assign __out_or_bits = |in_;
  assign __out_xor_bits = ^in_;

  assign out_and = __out_and_bits;
  assign out_or = __out_or_bits;
  assign out_xor = __out_xor_bits;
endmodule
