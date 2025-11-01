module Wire4(
  input  wire a,
              b,
              c,
  output wire w,
              x,
              y,
              z
);

  // Variables for output ports
  logic __w_bits;
  logic __x_bits;
  logic __y_bits;
  logic __z_bits;

  // @comb update():
  always_comb begin
    __w_bits = a;
    __x_bits = b;
    __y_bits = b;
    __z_bits = c;
  end // always_comb

  assign w = __w_bits;
  assign x = __x_bits;
  assign y = __y_bits;
  assign z = __z_bits;
endmodule
