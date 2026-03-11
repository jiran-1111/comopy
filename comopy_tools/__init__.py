# get_runner的更新

import cocotb_tools.runner as runner_module
from .runner import ComoPy


_original_get_runner = runner_module.get_runner

def get_runner(simulator_name: str):
    if simulator_name.lower() == "comopy":
        return ComoPy()
    return _original_get_runner(simulator_name)

# 覆盖注册
runner_module.get_runner = get_runner
