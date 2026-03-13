import asyncio

class ComopyDUT:
    def __init__(self, runner):
        self._runner = runner
        self.top = runner.top
        self.io = runner.io
        self.sim = runner.top.simulator
        self.signal_list = [0] * len(self.io._part_names)
        self.port_names = self.io._part_names
        print("🔥 你的真实端口列表：", self.port_names)

    def __getattr__(self, port_name):
        return ComopySignal(self, port_name)

    def set_signal(self, port_name, value):
        idx = self.port_names.index(port_name)
        self.signal_list[idx] = value

    def run_comb(self):
        self.io.assign_inputs(self.top, self.signal_list)
        self.sim.evaluate()

    def get_signal_value(self, port_name):
        self.run_comb()
        # ✅ 修复：Wire 直接返回，不加 .value！
        return self.top.X


class ComopySignal:
    def __init__(self, dut, port_name):
        self.dut = dut
        self.port_name = port_name

    @property
    def value(self):
        return self.dut.get_signal_value(self.port_name)

    @value.setter
    def value(self, v):
        self.dut.set_signal(self.port_name, v)


async def RisingEdge(signal):
    signal.dut.run_comb()
    await asyncio.sleep(0)