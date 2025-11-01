module Always_if(
  input  wire a,
              b,
              sel_b1,
              sel_b2,
  output wire out_assign,
              out_always
);

  // Variables for output ports
  logic __out_assign_bits;
  logic __out_always_bits;

  assign __out_assign_bits = sel_b1 & sel_b2 ? b : a;

  // @comb update():
  always_comb begin
    if (sel_b1 & sel_b2)
      __out_always_bits = b;
    else
      __out_always_bits = a;
  end // always_comb

  assign out_assign = __out_assign_bits;
  assign out_always = __out_always_bits;
endmodule
