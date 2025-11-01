module add16(
  input  wire [15:0] a,
                     b,
  input  wire        cin,
  output wire [15:0] sum,
  output wire        cout
);

  // Variables for output ports
  logic [15:0] __sum_bits;
  logic        __cout_bits;

  // cat(s.cout, s.sum)[:] @= s.a.ext(17) + s.b.ext(17) + s.cin.ext(17)
  wire  [16:0] _GEN = {1'h0, a} + {1'h0, b} + {16'h0, cin};
  assign __cout_bits = _GEN[16];
  assign __sum_bits = _GEN[15:0];

  assign sum = __sum_bits;
  assign cout = __cout_bits;
endmodule

module Module_cseladd(
  input  wire [31:0] a,
                     b,
  output wire [31:0] sum
);

  wire  [15:0] _hi1_sum;
  wire  [15:0] _hi0_sum;
  wire         _lo_cout;
  // Variables for output ports
  logic [31:0] __sum_bits;

  // s.lo = add16(s.a[:16], s.b[:16], 0, s.sum[:16])
  add16 lo (
    .a    (a[15:0]),
    .b    (b[15:0]),
    .cin  (1'h0),
    .sum  (__sum_bits[32'h0 +: 16]),
    .cout (_lo_cout)
  );

  // s.hi0 = add16(s.a[16:], s.b[16:], 0)
  add16 hi0 (
    .a    (a[31:16]),
    .b    (b[31:16]),
    .cin  (1'h0),
    .sum  (_hi0_sum),
    .cout (/* unused */)
  );

  // s.hi1 = add16(s.a[16:], s.b[16:], 1)
  add16 hi1 (
    .a    (a[31:16]),
    .b    (b[31:16]),
    .cin  (1'h1),
    .sum  (_hi1_sum),
    .cout (/* unused */)
  );

  // s.sum[16:] @= s.hi1.sum if s.lo.cout else s.hi0.sum
  assign __sum_bits[32'h10 +: 16] = _lo_cout ? _hi1_sum : _hi0_sum;

  assign sum = __sum_bits;
endmodule
