module Vector3(
  input  wire [4:0] a,
                    b,
                    c,
                    d,
                    e,
                    f,
  output wire [7:0] w,
                    x,
                    y,
                    z
);

  // Variables for output ports
  logic [7:0] __w_bits;
  logic [7:0] __x_bits;
  logic [7:0] __y_bits;
  logic [7:0] __z_bits;

  // @comb update():
  always_comb begin
    automatic logic [31:0] _GEN = {a, b, c, d, e, f, 2'h3};
    // cat(s.w, s.x, s.y, s.z)[:] /= cat(
    //     s.a, s.b, s.c, s.d, s.e, s.f, b2(0b11)
    // )
    __w_bits = _GEN[31:24];
    __x_bits = _GEN[23:16];
    __y_bits = _GEN[15:8];
    __z_bits = _GEN[7:0];
  end // always_comb

  assign w = __w_bits;
  assign x = __x_bits;
  assign y = __y_bits;
  assign z = __z_bits;
endmodule
