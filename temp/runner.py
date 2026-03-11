import os
import sys
import logging
from pathlib import Path
from typing import Any, Mapping, Sequence
from pathlib import Path
import importlib
import os
import comopy.hdl as HDL
from comopy.hdl import HDLStage
from comopy.ir import IRStage
from comopy.simulator import BaseSimulator, SimulatorStage
from comopy.translator import BaseTranslator, TranslatorStage
from comopy.utils import JobPipeline, match_lines
from cocotb_tools.runner import Runner, get_abs_path
from comopy_tools.Runner_base_test_case import RunnerBaseTestCase
import comopy.testcases.ex_HDLBits_features as ex
from comopy_tools.signal import ComoPySignal
from comopy_tools.dut import ComoPyDUT
from comopy_tools.trigger import ComoPyTimer
import asyncio
from cocotb.regression import RegressionManager

class ComoPy(Runner,RunnerBaseTestCase):
    def build(self, **kwargs: Any) -> None:

        sources = kwargs.get("sources", [])

        # 1 分离 python source
        py_sources = [s for s in sources if str(s).endswith(".py")]

        kwargs["sources"] = [s for s in sources if not str(s).endswith(".py")]

        # 2 先调用 cocotb build
        super().build(**kwargs)

        if not py_sources:
            raise ValueError("Need Python model source")

        model_path = Path(py_sources[0]).resolve()

        # 3 动态加载 python module
        module_name = model_path.stem

        spec = importlib.util.spec_from_file_location(module_name, model_path)

        module = importlib.util.module_from_spec(spec)

        sys.modules[module_name] = module

        spec.loader.exec_module(module)

        # 4 获取 top
        hdl_toplevel = kwargs.get("hdl_toplevel")

        model_cls = getattr(ex, hdl_toplevel)

        self.top = model_cls()

        # 5 获取 TV
        test_cls = getattr(module, f"Test{hdl_toplevel}")

        tv = test_cls.TV

        # 6 IO
        io = self._get_tv_io(tv)

        # 7 pipeline
        pipeline = JobPipeline(HDLStage(), IRStage(), SimulatorStage())
        pipeline(self.top)

        # 8 check
        self._check_module_io(self.top, io)

        # 9 init
        self._init_data(self.top, {})

        # 10 保存
        self.io = io
        self.simulator = self.top.simulator

        with open(os.path.join(self.build_dir, "comopy_debug.log"), "w") as f:
            f.write(f"Build success! Top: {self.top}, Simulator: {self.simulator}")
        
        # 检查
        if hasattr(self.top, 'simulator'):
            print(f"✅ [DEBUG] Found simulator instance: {type(self.top.simulator)}")
            
            if hasattr(self.top, 'simulator'):
                self.log.info(f"✅ ComoPy: {type(self.top.simulator).__name__} is ready.")
        else:
            self.log.error("❌ ComoPy: self.top has NO simulator attribute!")
            self.log.debug(f"Available attributes: {dir(self.top)}")
            
    # self.simulator 就是仿真器实例了，后续 cocotb 会调用它的接口进行仿真
    """
    hdl_toplevel="Gates100",
        hdl_toplevel_lang="verilog",
        test_module="cocotb_Gates100"

    """
    def test(self, **kwargs):
        # 1. 包装 DUT 并开启电源
        dut = ComoPyDUT(self.simulator)
        dut.start()
        
        # 2. 加载你刚写的脚本
        test_module = importlib.import_module("cocotb_Gates100")
        test_func = getattr(test_module, "test_gates100_logic")
        
        # 3. 运行协程
        print("🚀 正在通过 Cocotb 驱动 ComoPy 仿真...")
        asyncio.run(test_func(dut))
        
        dut.stop()
        

    
    
    # --- 必须实现的抽象方法 (Abstract Methods) ---


    def _check_hdl_toplevel_lang(self, hdl_toplevel_lang):
        return "python"
    
    def _simulator_in_path(self) -> str:
        # 这个方法通常检查仿真器可执行文件是否存在。
        # 对于 ComoPy，我们直接返回一个虚拟路径或库名
        return "comopy"

    def _build_command(self) -> list[str]:
        # ComoPy 是在 Python 内部 build 的，不需要外部 shell 命令
        return []

    def _test_command(self) -> list[str]:
        # 同理，测试也不需要外部命令行驱动
        return []

    def _get_include_options(self, includes: Sequence[Path]) -> list[str]:
        return []

    def _get_define_options(self, defines: Mapping[str, Any]) -> list[str]:
        return []

    def _get_parameter_options(self, parameters: Mapping[str, Any]) -> list[str]:
        return []

    # 另外建议重写这个方法，防止父类去执行空的命令导致报错
    def _execute(self, command: list[str], **kwargs: Any) -> None:
        if not command:
            return 
        super()._execute(command, **kwargs)