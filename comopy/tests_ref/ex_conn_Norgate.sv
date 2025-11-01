module Norgate(
  input  wire a,
              b,
  output wire out
);

  // Variables for output ports
  logic __out_bits;

  assign __out_bits = ~(a | b);

  assign out = __out_bits;
endmodule
