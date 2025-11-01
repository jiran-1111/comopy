module Conditional(
  input  wire [7:0] a,
                    b,
                    c,
                    d,
  output wire [7:0] min
);

  // Variables for output ports
  logic [7:0] __min_bits;

  logic [7:0] m1;
  logic [7:0] m2;
  assign m1 = a < b ? a : b;
  assign m2 = c < d ? c : d;
  assign __min_bits = m1 < m2 ? m1 : m2;

  assign min = __min_bits;
endmodule
