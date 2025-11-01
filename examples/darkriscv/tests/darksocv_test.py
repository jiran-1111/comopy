from comopy import HDLStage, IRStage, JobPipeline, SimulatorStage

from ..config import MLEN, RESET_PC
from ..darksocv import DarkSocv
from .utils import translate_sv, write_sv


def print_regs(top: DarkSocv):
    print("PC:", top.core.pc_gen.pc.data_bits, end="  ")
    print("Insn:", top.core.insn.data_bits, end="  ")
    print("Debug:", top.core.debug.data_bits.bin())
    print("Registers:")
    for i in range(32):
        print(top.core.regs[i].data_bits, end="  ")
        if i % 8 == 7:
            print()
    print()


def test_I_R_U_insns():
    top = DarkSocv(name="darksocv")
    pipeline = JobPipeline(HDLStage(), IRStage(), SimulatorStage())
    pipeline(top)

    # addi x0, x0, 0 (nop)
    mem = [0x00000013 for k in range((1 << MLEN) // 4)]
    mem[0] = 0x00100093  # addi x1, x0, 1
    mem[1] = 0x00209113  # slli x2, x1, 2
    mem[2] = 0xFFF0A193  # slti x3, x1, -1
    mem[3] = 0xFFF13213  # sltiu x4, x2, -1
    mem[4] = 0xFFF24293  # xori x5, x4, -1
    mem[5] = 0x0DB26313  # ori x6, x4, 0xdb
    mem[6] = 0x0DB2F393  # andi x7, x5, 0xdb
    mem[7] = 0x0082D413  # srli x8, x5, 8
    mem[8] = 0x4082D493  # srai x9, x5, 8
    mem[9] = 0x00208533  # add x10, x1, x2
    mem[10] = 0x402085B3  # sub x11, x1, x2
    mem[11] = 0x00209633  # sll x12, x1, x2
    mem[12] = 0x0090A6B3  # slt x13, x1, x9
    mem[13] = 0x0090B733  # sltu x14, x1, x9
    mem[14] = 0x008347B3  # xor x15, x6, x8
    mem[15] = 0x00245833  # srl x16, x8, x2
    mem[16] = 0x4024D8B3  # sra x17, x9, x2
    mem[17] = 0x0020E933  # or x18, x1, x2
    mem[18] = 0x0083F9B3  # and x19, x7, x8
    mem[19] = 0x000DBA37  # lui x20, 0xdb
    mem[20] = 0x000DBA97  # auipc x21, 0xdb

    sim = top.simulator
    sim.start()
    top.memory.mem.read_mem(mem)
    top.reset /= 1
    for _ in range(3):
        sim.tick()
    assert top.core.pc_gen.pc == RESET_PC
    assert top.core.pc_gen.next_pc == RESET_PC
    assert top.core.insn_data == 0
    top.reset /= 0
    sim.tick()  # xreset <<= 0
    assert top.core.xreset == 0
    assert top.core.flush == 1
    assert top.core.pc == RESET_PC
    assert top.core.pc_gen.next_pc == RESET_PC
    assert top.core.insn_data == mem[0]
    # Instruction 0
    sim.tick()  # flush <<= 0
    print_regs(top)
    assert top.core.pc == RESET_PC
    assert top.core.pc_gen.next_pc == RESET_PC + 4
    # Instruction 1
    sim.tick()
    print_regs(top)
    assert top.core.regs[1] == 1
    # Instruction 2
    sim.tick()
    print_regs(top)
    assert top.core.regs[2] == 4
    # Instruction 3
    sim.tick()
    print_regs(top)
    assert top.core.regs[3] == 0
    # Instruction 4
    sim.tick()
    print_regs(top)
    assert top.core.regs[4] == 1
    # Instruction 5
    sim.tick()
    print_regs(top)
    assert top.core.regs[5] == 0xFFFFFFFE
    # Instruction 6
    sim.tick()
    print_regs(top)
    assert top.core.regs[6] == 0x000000DB
    # Instruction 7
    sim.tick()
    print_regs(top)
    assert top.core.regs[7] == 0x000000DA
    # Instruction 8
    sim.tick()
    print_regs(top)
    assert top.core.regs[8] == 0x00FFFFFF
    # Instruction 9
    sim.tick()
    print_regs(top)
    assert top.core.regs[9] == 0xFFFFFFFF
    # Instruction 10
    sim.tick()
    print_regs(top)
    assert top.core.regs[10] == 5
    # Instruction 11
    sim.tick()
    print_regs(top)
    assert top.core.regs[11].S == -3
    # Instruction 12
    sim.tick()
    print_regs(top)
    assert top.core.regs[12] == 0x10
    # Instruction 13
    sim.tick()
    print_regs(top)
    assert top.core.regs[13] == 0
    # Instruction 14
    sim.tick()
    print_regs(top)
    assert top.core.regs[14] == 1
    # Instruction 15
    sim.tick()
    print_regs(top)
    assert top.core.regs[15] == 0x00FFFF24
    # Instruction 16
    sim.tick()
    print_regs(top)
    assert top.core.regs[16] == 0x000FFFFF
    # Instruction 17
    sim.tick()
    print_regs(top)
    assert top.core.regs[17] == 0xFFFFFFFF
    # Instruction 18
    sim.tick()
    print_regs(top)
    assert top.core.regs[18] == 5
    # Instruction 19
    sim.tick()
    print_regs(top)
    assert top.core.regs[19] == 0xDA
    # Instruction 20
    sim.tick()
    print_regs(top)
    assert top.core.regs[20] == 0x000DB000
    # Instruction 21
    sim.tick()
    print_regs(top)
    assert top.core.regs[21] == 0x000DB050
    sim.stop()


def test_load_store():
    top = DarkSocv(name="darksocv")
    pipeline = JobPipeline(HDLStage(), IRStage(), SimulatorStage())
    pipeline(top)

    # addi x0, x0, 0 (nop)
    mem = [0x00000013 for k in range((1 << MLEN) // 4)]
    mem[0] = 0x0DB00093  # addi x1, x0, 0xdb
    mem[1] = 0x08102023  # sw x1, 128(x0)
    mem[2] = 0x08101323  # sh x1, 134(x0)
    mem[3] = 0x081002A3  # sb x1, 133(x0)
    mem[4] = 0x08002103  # lw x2, 128(x0)
    mem[5] = 0x08401183  # lh x3, 132(x0)
    mem[6] = 0x08405203  # lhu x4, 132(x0)
    mem[7] = 0x08500283  # lb x5, 133(x0)
    mem[8] = 0x08504303  # lbu x6, 133(x0)

    sim = top.simulator
    sim.start()
    top.memory.mem.read_mem(mem)
    top.reset /= 1
    for _ in range(3):
        sim.tick()
    assert top.core.pc_gen.pc == RESET_PC
    assert top.core.pc_gen.next_pc == RESET_PC
    assert top.core.insn_data == 0
    top.reset /= 0
    sim.tick()  # xreset <<= 0
    assert top.core.xreset == 0
    assert top.core.flush == 1
    assert top.core.pc == RESET_PC
    assert top.core.pc_gen.next_pc == RESET_PC
    assert top.core.insn_data == mem[0]
    # Instruction 0
    sim.tick()  # flush <<= 0
    print_regs(top)
    assert top.core.pc == RESET_PC
    assert top.core.pc_gen.next_pc == RESET_PC + 4
    # Instruction 1
    sim.tick()
    print_regs(top)
    assert top.core.regs[1] == 0xDB
    # Instruction 2
    sim.tick()
    print_regs(top)
    assert top.memory.mem_waddr == 128
    assert top.memory.mem[128 // 4] == 0xDB
    # Instruction 3
    sim.tick()
    print_regs(top)
    assert top.memory.mem_waddr == 134
    # Instruction 4
    sim.tick()
    print_regs(top)
    assert top.memory.mem_waddr == 133
    assert top.memory.mem[132 // 4] == 0x00DBDB13
    sim.tick()  # halt for load
    print_regs(top)
    assert top.core.insn == mem[4]
    assert top.core.halt2
    # Instruction 5
    sim.tick()
    print_regs(top)
    assert top.core.regs[2] == 0x000000DB
    sim.tick()  # halt for load
    print_regs(top)
    assert top.core.halt2
    # Instruction 6
    sim.tick()
    print_regs(top)
    assert top.core.regs[3] == 0xFFFFDB13
    sim.tick()  # halt for load
    print_regs(top)
    assert top.core.halt2
    # Instruction 7
    sim.tick()
    print_regs(top)
    assert top.core.regs[4] == 0x0000DB13
    sim.tick()  # halt for load
    print_regs(top)
    assert top.core.halt2
    # Instruction 8
    sim.tick()
    print_regs(top)
    assert top.core.regs[5] == 0xFFFFFFDB
    sim.tick()  # halt for load
    print_regs(top)
    assert top.core.halt2
    # Instruction 9
    sim.tick()
    print_regs(top)
    assert top.core.regs[6] == 0x000000DB
    sim.stop()


def test_loop_jal():
    top = DarkSocv(name="darksocv")
    pipeline = JobPipeline(HDLStage(), IRStage(), SimulatorStage())
    pipeline(top)

    # addi x0, x0, 0 (nop)
    mem = [0x00000013 for k in range((1 << MLEN) // 4)]
    mem[0] = 0x00200093  # addi x1, x0, 2
    mem[1] = 0x00410113  # addi x2, x2, 4
    mem[2] = 0xFFF08093  # addi x1, x1, -1
    mem[3] = 0xFE009CE3  # bne x1, x0, -8
    mem[4] = 0xFF1FF1EF  # jal x1, -16

    sim = top.simulator
    sim.start()
    top.memory.mem.read_mem(mem)
    top.reset /= 1
    for _ in range(3):
        sim.tick()
    assert top.core.pc_gen.pc == RESET_PC
    assert top.core.pc_gen.next_pc == RESET_PC
    assert top.core.insn_data == 0
    top.reset /= 0
    sim.tick()  # xreset <<= 0
    # Instruction 0
    sim.tick()  # flush <<= 0
    print_regs(top)
    assert top.core.insn == mem[0]
    # Loop #1
    # Instruction 1
    sim.tick()
    print_regs(top)
    assert top.core.regs[1] == 2
    # Instruction 2
    sim.tick()
    print_regs(top)
    assert top.core.regs[2] == 4
    # Instruction 3
    sim.tick()
    print_regs(top)
    assert top.core.regs[1] == 1
    sim.tick()  # flush
    print_regs(top)
    assert top.core.flush == 1
    # Loop #2
    # Instruction 1
    sim.tick()
    print_regs(top)
    assert top.core.pc == RESET_PC + 4
    assert top.core.insn == mem[1]
    # Instruction 2
    sim.tick()
    print_regs(top)
    assert top.core.regs[2] == 8
    # Instruction 3
    sim.tick()
    print_regs(top)
    assert top.core.flush == 0
    assert top.core.regs[1] == 0
    # Instruction 4
    sim.tick()
    print_regs(top)
    assert top.core.pc == RESET_PC + 4 * 4
    sim.tick()  # flush
    print_regs(top)
    assert top.core.flush == 1
    assert top.core.regs[3] == RESET_PC + 4 * 5
    # Instruction 0
    sim.tick()
    print_regs(top)
    assert top.core.pc == RESET_PC
    sim.stop


def read_mem_hex(path: str) -> list[int]:
    with open(path, "r") as f:
        lines = f.readlines()
    return [int(line.strip(), 16) for line in lines if line.strip()]


def test_boot_memcpy(project_path):
    memfile = f"{project_path}/examples/darkriscv/src/boot_memcpy.mem"
    mem = read_mem_hex(memfile)

    top = DarkSocv(name="darksocv")
    pipeline = JobPipeline(HDLStage(), IRStage(), SimulatorStage())
    pipeline(top)

    sim = top.simulator
    sim.start()
    top.memory.mem.read_mem(mem)
    top.reset /= 1
    for _ in range(3):
        sim.tick()
    assert top.core.pc_gen.pc == RESET_PC
    assert top.core.pc_gen.next_pc == RESET_PC
    assert top.core.insn_data == 0
    top.reset /= 0
    sim.tick()  # xreset <<= 0
    for _ in range(800):
        sim.tick()

    base = 512 // 4
    for i in range(8):
        for j in range(8):
            assert top.memory.mem[base + i * 8 + j] == ((i + 1) << 28) + j + 1
    sim.stop()


# Enable test_boot_app():
# - Make in darkriscv/src and generate darkriscv.mem
# - Debug test_boot_app(), check the output
# def test_boot_app(project_path):
def run_boot_app():
    project_path = "."
    memfile = f"{project_path}/examples/darkriscv/src/darkriscv.mem"
    mem = read_mem_hex(memfile)

    top = DarkSocv(name="darksocv")
    pipeline = JobPipeline(HDLStage(), IRStage(), SimulatorStage())
    pipeline(top)

    sim = top.simulator
    sim.start()
    top.memory.mem.read_mem(mem)
    top.reset /= 1
    for _ in range(3):
        sim.tick()
    assert top.core.pc_gen.pc == RESET_PC
    assert top.core.pc_gen.next_pc == RESET_PC
    assert top.core.insn_data == 0
    top.reset /= 0
    sim.tick()  # xreset <<= 0
    sim.tick()
    for _ in range(500):
        sim.tick()

    offset = 0x1000 // 4
    print("DBuffer:")
    while True:
        word = top.memory.mem[offset]
        if word == 0:
            break
        print(chr(word & 0xFF), end="")
        if (word := word >> 8) == 0:
            break
        print(chr(word & 0xFF), end="")
        if (word := word >> 8) == 0:
            break
        print(chr(word & 0xFF), end="")
        if (word := word >> 8) == 0:
            break
        print(chr(word & 0xFF), end="")
        offset += 1
    sim.stop()


def test_translate():
    top = DarkSocv(name="DarkSocv")
    sv = translate_sv(top)
    write_sv(sv, "darksocv.sv")
