module Memory(
  input  wire        clk,
                     reset,
  input  wire [31:0] insn_addr,
                     data_addr,
                     data_in,
  input  wire        write,
                     read,
  input  wire [3:0]  byte_en,
  output wire [31:0] mem_waddr,
                     insn_data,
                     data_out,
  output wire        halt
);

  // Variables for output ports
  logic      [31:0] __mem_waddr_bits;
  logic      [31:0] __insn_data_bits;
  logic      [31:0] __data_out_bits;
  logic             __halt_bits;

  // Local parameters
  localparam [31:0] MLEN = 13;

  logic      [31:0] mem[0:2047];
  logic             d_ack;
  logic             d_hit;
  logic             w_hit;
  assign d_hit = ~(read & d_ack != 1'h1);
  assign w_hit = 1'h1;
  assign __halt_bits = ~d_hit | ~w_hit;

  // @seq insn_bus():
  always @(posedge clk)
    __insn_data_bits <= reset ? 32'h0 : mem[insn_addr[12:2]];

  // @seq update_dack():
  always @(posedge clk)
    d_ack <= reset ? 1'h0 : read ? 1'h1 : 1'h0;

  // @seq read_data():
  always @(posedge clk)
    __data_out_bits <= reset ? 32'h0 : mem[data_addr[12:2]];

  // @seq write_data():
  always @(posedge clk) begin
    for (logic [31:0] i = 32'h0; i < 32'h4; i += 32'h1) begin
      if (~__halt_bits & write & data_addr[31] == 1'h0 & byte_en[i +: 1])
        mem[data_addr[12:2]][i * 32'h8 +: 8] <= data_in[i * 32'h8 +: 8];
    end
    __mem_waddr_bits <= reset ? 32'h0 : data_addr;
  end // always @(posedge)

  assign mem_waddr = __mem_waddr_bits;
  assign insn_data = __insn_data_bits;
  assign data_out = __data_out_bits;
  assign halt = __halt_bits;
endmodule
