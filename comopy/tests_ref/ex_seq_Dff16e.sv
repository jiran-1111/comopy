module Dff16e(
  input  wire        clk,
                     resetn,
  input  wire [1:0]  byteena,
  input  wire [15:0] d,
  output wire [15:0] q
);

  // Variables for output ports
  logic [15:0] __q_bits;

  // @seq update_ff():
  always @(posedge clk) begin
    if (~resetn)
      __q_bits <= 16'h0;
    else begin
      if (byteena[0]) begin
        // s.q[:8] <<= s.d[:8]
        __q_bits[32'h0 +: 8] <= d[7:0];
      end
      if (byteena[1]) begin
        // s.q[8:] <<= s.d[8:]
        __q_bits[32'h8 +: 8] <= d[15:8];
      end
    end
  end // always @(posedge)

  assign q = __q_bits;
endmodule
