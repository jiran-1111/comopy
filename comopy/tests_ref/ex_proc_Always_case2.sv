module Always_case2(
  input  wire [3:0] in_,
  output wire [1:0] pos
);

  // Variables for output ports
  logic [1:0] __pos_bits;

  // @comb update():
  always_comb begin
    unique case (in_)
      4'b0000:
        __pos_bits = 2'h0;
      4'b0001:
        __pos_bits = 2'h0;
      4'b0010:
        __pos_bits = 2'h1;
      4'b0011:
        __pos_bits = 2'h0;
      4'b0100:
        __pos_bits = 2'h2;
      4'b0101:
        __pos_bits = 2'h0;
      4'b0110:
        __pos_bits = 2'h1;
      4'b0111:
        __pos_bits = 2'h0;
      4'b1000:
        __pos_bits = 2'h3;
      4'b1001:
        __pos_bits = 2'h0;
      4'b1010:
        __pos_bits = 2'h1;
      4'b1011:
        __pos_bits = 2'h0;
      4'b1100:
        __pos_bits = 2'h2;
      4'b1101:
        __pos_bits = 2'h0;
      4'b1110:
        __pos_bits = 2'h1;
      4'b1111:
        __pos_bits = 2'h0;
    endcase
  end // always_comb

  assign pos = __pos_bits;
endmodule
