module Vectorrev1_cat_lhs(
  input  wire [7:0] in_,
  output wire [7:0] out
);

  // Variables for output ports
  logic [7:0] __out_bits;

  // @comb update():
  always_comb begin
    /*
      cat(
          s.out[0],
          s.out[1],
          s.out[2],
          s.out[3],
          s.out[4],
          s.out[5],
          s.out[6],
          s.out[7],
      )[:] /= s.in_
     */
    __out_bits[32'h0 +: 1] = in_[7];
    __out_bits[32'h1 +: 1] = in_[6];
    __out_bits[32'h2 +: 1] = in_[5];
    __out_bits[32'h3 +: 1] = in_[4];
    __out_bits[32'h4 +: 1] = in_[3];
    __out_bits[32'h5 +: 1] = in_[2];
    __out_bits[32'h6 +: 1] = in_[1];
    __out_bits[32'h7 +: 1] = in_[0];
  end // always_comb

  assign out = __out_bits;
endmodule
