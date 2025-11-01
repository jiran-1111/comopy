module Vector5(
  input  wire        a,
                     b,
                     c,
                     d,
                     e,
  output wire [24:0] out
);

  // Variables for output ports
  logic [24:0] __out_bits;

  logic [24:0] top;
  logic [24:0] bottom;
  assign top = {{5{a}}, {5{b}}, {5{c}}, {5{d}}, {5{e}}};
  assign bottom = {5{a, b, c, d, e}};
  assign __out_bits = ~top ^ bottom;

  assign out = __out_bits;
endmodule
