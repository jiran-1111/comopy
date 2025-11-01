module Popcount255(
  input  wire [254:0] in_,
  output wire [7:0]   out
);

  // Variables for output ports
  logic [7:0] __out_bits;

  // @comb update():
  always_comb begin
    __out_bits = 8'h0;
    for (logic [31:0] i = 32'h0; i < 32'hFF; i += 32'h1) begin
      __out_bits = __out_bits + {7'h0, in_[i +: 1]};
    end
  end // always_comb

  assign out = __out_bits;
endmodule
