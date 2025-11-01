module Dff8ar(
  input  wire       clk,
                    areset,
  input  wire [7:0] d,
  output wire [7:0] q
);

  // Variables for output ports
  logic [7:0] __q_bits;

  // @seq update_ff():
  always @(posedge clk or posedge areset) begin
    if (areset)
      __q_bits <= 8'h0;
    else
      __q_bits <= d;
  end // always @(posedge, posedge)

  assign q = __q_bits;
endmodule
