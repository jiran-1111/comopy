module Vector100r(
  input  wire [99:0] in_,
  output wire [99:0] out
);

  // Variables for output ports
  logic [99:0] __out_bits;

  // @comb update():
  always_comb begin
    for (logic [31:0] i = 32'h0; i < 32'h64; i += 32'h1) begin
      // s.out[i] /= s.in_[100 - i - 1]
      __out_bits[i +: 1] = in_[32'h64 - i - 32'h1 +: 1];
    end
  end // always_comb

  assign out = __out_bits;
endmodule
