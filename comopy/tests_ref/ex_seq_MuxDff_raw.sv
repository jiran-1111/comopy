module MuxDff_raw(
  input  wire clk,
              L,
              r_in,
              q_in,
  output wire Q
);

  // Variables for output ports
  logic __Q_bits;

  // @seq update_q():
  always @(posedge clk)
    __Q_bits <= L ? r_in : q_in;

  assign Q = __Q_bits;
endmodule
