module Alwaysblock1(
  input  wire a,
              b,
  output wire out_assign,
              out_alwaysblock
);

  // Variables for output ports
  logic __out_assign_bits;
  logic __out_alwaysblock_bits;

  assign __out_assign_bits = a & b;

  // @comb update():
  always_comb
    __out_alwaysblock_bits = a & b;

  assign out_assign = __out_assign_bits;
  assign out_alwaysblock = __out_alwaysblock_bits;
endmodule
