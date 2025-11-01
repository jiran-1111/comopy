module Vectorgates(
  input  wire [2:0] a,
                    b,
  output wire [2:0] out_or_bitwise,
  output wire       out_or_logical,
  output wire [5:0] out_not
);

  // Variables for output ports
  logic [2:0] __out_or_bitwise_bits;
  logic       __out_or_logical_bits;
  logic [5:0] __out_not_bits;

  // @comb update():
  always_comb begin
    __out_or_bitwise_bits = a | b;
    __out_or_logical_bits = (|a) | (|b);
    // s.out_not[:3] /= ~s.a
    __out_not_bits[32'h0 +: 3] = ~a;
    // s.out_not[3:] /= ~s.b
    __out_not_bits[32'h3 +: 3] = ~b;
  end // always_comb

  assign out_or_bitwise = __out_or_bitwise_bits;
  assign out_or_logical = __out_or_logical_bits;
  assign out_not = __out_not_bits;
endmodule
