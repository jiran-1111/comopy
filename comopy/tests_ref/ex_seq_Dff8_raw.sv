module Dff8_raw(
  input  wire       clk,
  input  wire [7:0] d,
  output wire [7:0] q
);

  // Variables for output ports
  logic [7:0] __q_bits;

  // @seq update_ff():
  always @(posedge clk)
    __q_bits <= d;

  assign q = __q_bits;
endmodule
