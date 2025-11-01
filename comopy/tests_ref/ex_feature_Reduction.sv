module Reduction(
  input  wire [7:0] in_,
  output wire       parity
);

  // Variables for output ports
  logic __parity_bits;

  assign __parity_bits = ^in_;

  assign parity = __parity_bits;
endmodule
