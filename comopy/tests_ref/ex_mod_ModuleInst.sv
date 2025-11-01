module mod_a1(
  input  wire in1,
              in2,
  output wire out
);

  // Variables for output ports
  logic __out_bits;

  assign __out_bits = in1 & in2;

  assign out = __out_bits;
endmodule

module ModuleInst(
  input  wire a,
              b,
  output wire out
);

  // Variables for output ports
  logic __out_bits;

  // s.inst = mod_a1()
  logic _inst_in1;
  logic _inst_in2;
  mod_a1 inst (
    .in1 (_inst_in1),
    .in2 (_inst_in2),
    .out (__out_bits)
  );

  assign _inst_in1 = a;
  assign _inst_in2 = b;

  assign out = __out_bits;
endmodule
