module Vector4(
  input  wire [7:0]  in_,
  output wire [31:0] out
);

  // Variables for output ports
  logic [31:0] __out_bits;

  assign __out_bits = {{24{in_[7]}}, in_};

  assign out = __out_bits;
endmodule
