module Vector1(
  input  wire [15:0] in_,
  output wire [7:0]  out_hi,
                     out_lo
);

  // Variables for output ports
  logic [7:0] __out_hi_bits;
  logic [7:0] __out_lo_bits;

  // @comb update():
  always_comb begin
    __out_hi_bits = in_[15:8];
    __out_lo_bits = in_[7:0];
  end // always_comb

  assign out_hi = __out_hi_bits;
  assign out_lo = __out_lo_bits;
endmodule
