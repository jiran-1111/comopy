module Module_fadd1(
  input  wire a,
              b,
              cin,
  output wire sum,
              cout
);

  // Variables for output ports
  logic __sum_bits;
  logic __cout_bits;

  assign __sum_bits = a ^ b ^ cin;
  assign __cout_bits = a & b | a & cin | b & cin;

  assign sum = __sum_bits;
  assign cout = __cout_bits;
endmodule
