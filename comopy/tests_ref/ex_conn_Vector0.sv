module Vector0(
  input  wire [2:0] vec,
  output wire [2:0] outv,
  output wire       o0,
                    o1,
                    o2
);

  // Variables for output ports
  logic [2:0] __outv_bits;
  logic       __o0_bits;
  logic       __o1_bits;
  logic       __o2_bits;

  assign __outv_bits = vec;
  assign __o0_bits = vec[0];
  assign __o1_bits = vec[1];
  assign __o2_bits = vec[2];

  assign outv = __outv_bits;
  assign o0 = __o0_bits;
  assign o1 = __o1_bits;
  assign o2 = __o2_bits;
endmodule
