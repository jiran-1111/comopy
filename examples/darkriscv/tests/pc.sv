module PC(
  input  wire        clk,
                     xreset,
                     halt,
                     jreq,
  input  wire [31:0] jval,
  output wire [31:0] pc,
                     next_pc
);

  // Variables for output ports
  logic      [31:0] __pc_bits;
  logic      [31:0] __next_pc_bits;

  // Local parameters
  localparam [31:0] RESET_PC = 0;

  // @seq update_pc():
  always @(posedge clk) begin
    if (xreset) begin
      __next_pc_bits <= RESET_PC;
      __pc_bits <= RESET_PC;
    end
    else begin
      __next_pc_bits <= halt ? __next_pc_bits : jreq ? jval : __next_pc_bits + 32'h4;
      __pc_bits <= halt ? __pc_bits : __next_pc_bits;
    end
  end // always @(posedge)

  assign pc = __pc_bits;
  assign next_pc = __next_pc_bits;
endmodule
