module Always_nolatches(
  input  wire [15:0] scancode,
  output wire        left,
                     down,
                     right,
                     up
);

  // Variables for output ports
  logic __left_bits;
  logic __down_bits;
  logic __right_bits;
  logic __up_bits;

  // @comb update():
  always_comb begin
    __left_bits = 1'h0;
    __down_bits = 1'h0;
    __right_bits = 1'h0;
    __up_bits = 1'h0;
    unique case (scancode)
      16'b1110000001101011:
        __left_bits = 1'h1;
      16'b1110000001110010:
        __down_bits = 1'h1;
      16'b1110000001110100:
        __right_bits = 1'h1;
      16'b1110000001110101:
        __up_bits = 1'h1;
      default: begin
        // Empty default for unique case completeness
      end
    endcase
  end // always_comb

  assign left = __left_bits;
  assign down = __down_bits;
  assign right = __right_bits;
  assign up = __up_bits;
endmodule
