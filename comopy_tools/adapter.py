import asyncio

"""
DUT: 包装被测的DUT模块，给测试脚本提供统一接口
"""
class ComopyDUT:
    # 接收runner作为参数
    def __init__(self, runner):
        self._runner = runner
        self.top = runner.top
        self.io = runner.io
        self.sim = runner.top.simulator
        # 信号值缓存列表：与端口一一对应，存储输入信号的值
        self.signal_list = [0] * len(self.io._part_names)
        # 保存模块所有端口名称（例如 ["A", "B", "X"]）
        self.port_names = self.io._part_names
        print("🔥 你的真实端口列表：", self.port_names)

    def __getattr__(self, port_name):
        # 返回一个信号包装对象，绑定当前DUT和端口名
        return ComopySignal(self, port_name)

    # 设置信号值
    def set_signal(self, port_name, value):
        idx = self.port_names.index(port_name)
        self.signal_list[idx] = value

    # 运行组合逻辑：立即更新输入并让仿真器计算一次输出
    def run_comb(self):
        # 将缓存的输入值复制给HDL模块的输入端口
        self.io.assign_inputs(self.top, self.signal_list)
        # 计算
        self.sim.evaluate()

    # 获取指定端口的值
    def get_signal_value(self, port_name):
        # 更新
        self.run_comb()
        # 获取输出端口的值
        return getattr(self.top, port_name)


"""
信号包装
"""
class ComopySignal:
    def __init__(self, dut, port_name):
        self.dut = dut
        self.port_name = port_name

    @property
    def value(self):
        # 调用dut的方法获取信号值
        return self.dut.get_signal_value(self.port_name)

    @value.setter
    def value(self, v):
        # 调用dut的方法设置信号值
        self.dut.set_signal(self.port_name, v)


# TODO: 各类触发器？暂时只是刷新了一下
async def RisingEdge(signal):
    signal.dut.run_comb()
    await asyncio.sleep(0)