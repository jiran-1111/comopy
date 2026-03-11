import comopy.hdl as HDL
from comopy_tools.signal import ComoPySignal

class ComoPyDUT:

    def __init__(self, top):
        self._top = top
        self._sim = top.simulator

        for name, obj in vars(top).items():
            if isinstance(obj, HDL.Signal):
                setattr(self, name, ComoPySignal(self._sim, obj))