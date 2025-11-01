module Vector2(
  input  wire [31:0] in_,
  output wire [31:0] out
);

  // Variables for output ports
  logic [31:0] __out_bits;

  // s.out[24:] @= s.in_[:8]
  assign __out_bits[32'h18 +: 8] = in_[7:0];
  // s.out[16:24] @= s.in_[8:16]
  assign __out_bits[32'h10 +: 8] = in_[15:8];
  // s.out[8:16] @= s.in_[16:24]
  assign __out_bits[32'h8 +: 8] = in_[23:16];
  // s.out[:8] @= s.in_[24:]
  assign __out_bits[32'h0 +: 8] = in_[31:24];

  assign out = __out_bits;
endmodule
