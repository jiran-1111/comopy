module Vector2(
  input  wire [31:0] in_,
  output wire [31:0] out
);

  // Variables for output ports
  logic [31:0] __out_bits;

  // @comb update():
  always_comb begin
    // s.out[24:] /= s.in_[:8]
    __out_bits[32'h18 +: 8] = in_[7:0];
    // s.out[16:24] /= s.in_[8:16]
    __out_bits[32'h10 +: 8] = in_[15:8];
    // s.out[8:16] /= s.in_[16:24]
    __out_bits[32'h8 +: 8] = in_[23:16];
    // s.out[:8] /= s.in_[24:]
    __out_bits[32'h0 +: 8] = in_[31:24];
  end // always_comb

  assign out = __out_bits;
endmodule
