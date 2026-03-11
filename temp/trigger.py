"""
Minimal trigger adapter for ComoPy.
Maps cocotb-style time advance (Timer)
to the ComoPy simulator clock tick.
"""

class ComoPyTimer:

    def __init__(self, sim):
        self._sim = sim

    async def wait(self):
        # Advance one simulation cycle
        self._sim.tick()