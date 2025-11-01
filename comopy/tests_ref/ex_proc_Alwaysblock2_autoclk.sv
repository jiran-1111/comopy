module Alwaysblock2_autoclk(
  input  wire clk,
              a,
              b,
  output wire out_assign,
              out_always_comb,
              out_always_ff
);

  // Variables for output ports
  logic __out_assign_bits;
  logic __out_always_comb_bits;
  logic __out_always_ff_bits;

  assign __out_assign_bits = a ^ b;

  // @comb update():
  always_comb
    __out_always_comb_bits = a ^ b;

  // @seq update_ff():
  always @(posedge clk)
    __out_always_ff_bits <= a ^ b;

  assign out_assign = __out_assign_bits;
  assign out_always_comb = __out_always_comb_bits;
  assign out_always_ff = __out_always_ff_bits;
endmodule
