module Dff8r_raw(
  input  wire       clk,
                    reset,
  input  wire [7:0] d,
  output wire [7:0] q
);

  // Variables for output ports
  logic [7:0] __q_bits;

  // @seq update_ff():
  always @(posedge clk) begin
    if (reset)
      __q_bits <= 8'h0;
    else
      __q_bits <= d;
  end // always @(posedge)

  assign q = __q_bits;
endmodule
