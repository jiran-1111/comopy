module Vectorrev1(
  input  wire [7:0] in_,
  output wire [7:0] out
);

  // Variables for output ports
  logic [7:0] __out_bits;

  assign __out_bits = {in_[0], in_[1], in_[2], in_[3], in_[4], in_[5], in_[6], in_[7]};

  assign out = __out_bits;
endmodule
