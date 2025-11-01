module Always_case(
  input  wire [2:0] sel,
  input  wire [3:0] data0,
                    data1,
                    data2,
                    data3,
                    data4,
                    data5,
  output wire [3:0] out
);

  // Variables for output ports
  logic [3:0] __out_bits;

  // @comb update():
  always_comb begin
    unique case (sel)
      3'b000:
        __out_bits = data0;
      3'b001:
        __out_bits = data1;
      3'b010:
        __out_bits = data2;
      3'b011:
        __out_bits = data3;
      3'b100:
        __out_bits = data4;
      3'b101:
        __out_bits = data5;
      default:
        __out_bits = 4'h0;
    endcase
  end // always_comb

  assign out = __out_bits;
endmodule
