"""
Base class for cocotb test cases.
"""
import comopy.hdl as HDL
import os
from typing import Any
import textwrap
from comopy.ir import IRStage
from comopy.simulator import BaseSimulator, SimulatorStage
from comopy.translator import BaseTranslator, TranslatorStage
from comopy.utils import JobPipeline, match_lines
from comopy.hdl import HDLStage
from comopy.ir import IRStage
from typing import List, Tuple
from comopy.hdl.signal import Signal
class CocotbBaseTestCase():
    
    # 主流程：仿真 & 验证
    def simulate(
        self,
        top: HDL.RawModule,
        tv: list,
        init: dict[str, Any] = {}
    ):
        if not tv:
            raise RuntimeError(f"No TV for DUT module {top}.")

        io = self.__get_tv_io(tv)

        pipeline = JobPipeline(
            HDLStage(),
            IRStage(),
            TranslatorStage(),
            SimulatorStage(),
        )
        pipeline(top)

        # 生成 SV 供 cocotb 使用
     
        trans = top.translator
        assert isinstance(trans, BaseTranslator)
        sv = trans.emit()
        assert isinstance(sv, str)

        out_dir = os.path.join(
            os.path.dirname(__file__),
            "cocotb_tests",
            top.__class__.__name__
        )
        os.makedirs(out_dir, exist_ok=True)

        sv_path = os.path.join(out_dir, f"{top.__class__.__name__}.sv")
        with open(sv_path, "w", encoding="utf-8") as f:
            f.write(sv)

        print("Generated SV at:", sv_path)

        # 后续流程 同base_test_case.py
        self.__check_module_io(top, io)
        self.__init_data(top, init)
        self.__run_ticks(top, io, tv)

        # 生成 cocotb 测试文件 & Makefile
        self.cocotb_simulate(top.__class__.__name__, tv)

    # 提取测试向量中的 IOStruct
    def __get_tv_io(self, tv: list) -> HDL.IOStruct:
            io = tv[0]
            if not isinstance(io, HDL.IOStruct):
                raise RuntimeError("No IOStruct at TV[0].")
            for i, data in enumerate(tv[1:], 1):
                # 检查输入数量与类型一致性
                if not io.match_data(data):
                    io_cls = io.__class__.__name__
                    raise RuntimeError(f"TV[{i}] doesn't match {io_cls}: {data}")
            return io
    
    # 比较电路端口 测试端口一致
    def __check_module_io(self, top: HDL.RawModule, io: HDL.IOStruct):
        if not io.match_module_io(top):
            io_cls = io.__class__.__name__
            raise RuntimeError(
                f"{io_cls}() at TV[0] doesn't match module {top}."
            )

    # 初始化寄存器
    def __init_data(self, top: HDL.RawModule, init: dict[str, Any]):
        root = top.node
        assert isinstance(root, HDL.CircuitNode)
        assert root.is_root
        for name, value in init.items():
            node = root.get_element(name)
            assert isinstance(node, HDL.CircuitNode)
            obj = node.obj
            assert isinstance(obj, HDL.SignalArray)
            # 把初始数据写入
            obj.read_mem(value)

    # 推进时钟周期 & 验证输出
    def __run_ticks(self, top: HDL.RawModule, io: HDL.IOStruct, tv: list):
        sim = top.simulator
        # isinstance是检查某个东西是不是某个类型的
        assert isinstance(sim, BaseSimulator)
        # 启动仿真 推进时钟周期 组合逻辑重新计算 结束仿真 这里等价于timer readonlu nexttimestep
        sim.start()
        # 每一行测试向量 把输入信号送进电路
        for i, data in enumerate(tv[1:], 1):
            io.assign_inputs(top, data)
            # 等价于 dut.in,_value = data[0] GPI写信号
            assert isinstance(top, HDL.RawModule)
            if isinstance(top, HDL.Module):
                sim.tick()
            else:
                sim.evaluate()
            try:
                # 比对
                io.verify_outputs(top, data)
                # 等价于 assert dut.out_and.value == expected  GPI读信号
            except Exception as e:
                raise RuntimeError(f"{e} : TV[{i}] {data}")
        sim.stop()

    # 验证生成的verilgo是否符合预期
    def translate(self, top: HDL.RawModule, match: str):
        pipeline = JobPipeline(HDLStage(), IRStage(), TranslatorStage())
        pipeline(top)

        trans = top.translator
        assert isinstance(trans, BaseTranslator)
        sv = trans.emit()
        assert isinstance(sv, str)
        match_lines(sv, match)


    # 生成 cocotb 测试文件 & Makefile
    def cocotb_simulate(
        self, top_module_name:str, tv:list
    ):
        
        io = self.__get_tv_io(tv)
        vectors = tv[1:]

        # 提取端口信息（顺序 + 方向）
        ports = self._extract_ports(io)
         # 校验测试向量长度
        for i, vec in enumerate(vectors):
            if len(vec) != len(ports):
                raise RuntimeError(
                    f"TV[{i}] length {len(vec)} != IO ports {len(ports)}"
                )

        # 生成 cocotb 测试 & Makefile
        self._generate_cocotb_test(top_module_name, ports, vectors)

    # 从 IOStruct 中提取端口信息
    # 返回类似 [('in_', 'In'), ('parity', 'Out')]
    def _extract_ports(self, io: HDL.IOStruct) -> list[tuple[str, str]]:
        ports: list[tuple[str, str]] = []
        io_cls = type(io)
        
        for name, attr in vars(io_cls).items():
            if not isinstance(attr, Signal):
                continue
            direction = attr.direction
            ports.append((name, direction.name))


        if not ports:
            raise RuntimeError("No Input/Output ports found in IOStruct")

        #print("Extracted ports:", ports)
        return ports
 
    # 生成 cocotb 测试文件      
    def _generate_cocotb_test(self, top: str, ports: list, vectors: list):
        out_dir = os.path.join(
            os.path.dirname(__file__),
            "cocotb_tests",top
        )
        os.makedirs(out_dir, exist_ok=True)

        out_file = os.path.join(out_dir, f"test_{top}_auto.py")
        print("Generating cocotb test at:", out_file)

        lines = []
        lines.append("# auto-generated by comopy")
        lines.append("import cocotb")
        lines.append("from cocotb.triggers import Timer")
        lines.append("")
        lines.append("@cocotb.test()")
        lines.append(f"async def test_{top}(dut):")
        lines.append("    await Timer(1, units='ns')")
        lines.append("")
        lines.append("    vectors = [")

        for vec in vectors:
            lines.append(f"        {vec},")

        lines.append("    ]")
        lines.append("")
        lines.append("    for vec in vectors:")


        # 输入赋值
        for idx, (name, direction) in enumerate(ports):
            if direction == "In":
                lines.append(
                    f"        dut.{name}.value = vec[{idx}]"
                )

        lines.append("        await Timer(1, units='ns')")

        # 输出检查
        for idx, (name, direction) in enumerate(ports):
            if direction == "Out":
                lines.append(
                    f"        assert dut.{name}.value == vec[{idx}]"
                )

        with open(out_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        self._generate_makefile(out_dir, top)

    # 生成 Makefile
    def _generate_makefile(self, out_dir: str, top_module_name: str) -> None:
        makefile = textwrap.dedent(f"""\
            TOPLEVEL_LANG = verilog
            SIM = icarus
            TOPLEVEL = {top_module_name}
            MODULE = test_{top_module_name}_auto
            VERILOG_SOURCES = $(PWD)/{top_module_name}.sv
            include $(shell cocotb-config --makefiles)/Makefile.sim
            .PHONY: clean_all

            clean_all: clean
            \trm -f {top_module_name}.sv test_{top_module_name}_auto.py
        """).rstrip() + "\n"

        path = os.path.join(out_dir, "Makefile")
        with open(path, "w", encoding="utf-8") as f:
            f.write(makefile)

        print("Generating Makefile at:", path)



