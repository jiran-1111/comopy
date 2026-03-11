"""
Cocotb-style signal wrapper for ComoPy.
Supports dut.sig.value read/write.
"""

class ComoPySignal:

    def __init__(self, sim, signal):
        self._sim = sim
        self._signal = signal

    @property
    def value(self):
        return int(self._signal._data)

    @value.setter
    def value(self, v):
        self._signal /= v
        self._sim.evaluate()

    def __repr__(self):
        return f"<ComoPySignal value={int(self._signal._data)}>"