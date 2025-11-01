module Always_if2(
  input  wire cpu_overheated,
  output wire shut_off_computer,
  input  wire arrived,
              gas_tank_empty,
  output wire keep_driving
);

  // Variables for output ports
  logic __shut_off_computer_bits;
  logic __keep_driving_bits;

  // @comb computer():
  always_comb begin
    if (cpu_overheated)
      __shut_off_computer_bits = 1'h1;
    else
      __shut_off_computer_bits = 1'h0;
  end // always_comb

  // @comb car():
  always_comb begin
    if (~arrived)
      __keep_driving_bits = ~gas_tank_empty;
    else
      __keep_driving_bits = 1'h0;
  end // always_comb

  assign shut_off_computer = __shut_off_computer_bits;
  assign keep_driving = __keep_driving_bits;
endmodule
