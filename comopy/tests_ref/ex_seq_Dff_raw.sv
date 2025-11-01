module Dff_raw(
  input  wire clk,
              d,
  output wire q
);

  // Variables for output ports
  logic __q_bits;

  // @seq update_ff():
  always @(posedge clk)
    __q_bits <= d;

  assign q = __q_bits;
endmodule
