module Always_casez(
  input  wire [7:0] in_,
  output wire [2:0] pos
);

  // Variables for output ports
  logic [2:0] __pos_bits;

  // @comb update():
  always_comb begin
    casez (in_)
      8'bzzzzzzz1:
        __pos_bits = 3'h0;
      8'bzzzzzz10:
        __pos_bits = 3'h1;
      8'bzzzzz100:
        __pos_bits = 3'h2;
      8'bzzzz1000:
        __pos_bits = 3'h3;
      8'bzzz10000:
        __pos_bits = 3'h4;
      8'bzz100000:
        __pos_bits = 3'h5;
      8'bz1000000:
        __pos_bits = 3'h6;
      8'b10000000:
        __pos_bits = 3'h7;
      default:
        __pos_bits = 3'h0;
    endcase
  end // always_comb

  assign pos = __pos_bits;
endmodule
