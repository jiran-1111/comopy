import os
import re
import importlib
from pathlib import Path
from typing import Any
import comopy.hdl as HDL
from comopy.hdl import IOStruct, Input, Output
from comopy_tools.Runner_base_test_case import RunnerBaseTestCase


class ComoPy(RunnerBaseTestCase):
    def build(self, file_path: str, top_module_name: str, init: dict[str, Any] = {}):
        """
        构建待测试模块的RawModule实例，纯文本解析生成IO类
        
        Args:
            file_path: 模块文件绝对/相对路径
            top_module_name: 顶层模块类名
            init: 初始化参数
        
        Returns:
            构建好的RawModule实例
        """
        # 检查文件存在性
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"HDL文件 {file_path} 未找到。")
        
        # 读取文件内容并解析端口定义
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        port_defs = self._parse_ports_from_text(file_content)
        if not port_defs:
            raise RuntimeError(f"在文件 {file_path} 中未解析到任何端口定义！")
        
        # 生成IO类代码并动态创建IO类
        io_class_code = self._generate_io_class_code(port_defs)
        loc = {}
        exec(io_class_code, globals(), loc)
        IO = loc['IO']

        # 动态导入模块并实例化顶层模块
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        top_cls = getattr(module, top_module_name, None)
        if top_cls is None:
            raise RuntimeError(f"在文件 {file_path} 中找不到模块 {top_module_name}。")
        top_inst = top_cls()

        # 构建测试向量并执行仿真
        io_instance = IO()
        tv = [io_instance]
        result = self.simulate(top_inst, tv, init)
        
        # 输出仿真结果
        print(f"simulate returned: {result}")
        print(f"simulate returned type: {type(result)}")
        print(result.simulator)
        return result
    
    def _parse_ports_from_text(self, file_content: str) -> dict:
        """
        正则匹配解析端口定义
        
        Args:
            file_content: 模块文件文本内容
        
        Returns:
            端口定义字典，格式: {"端口名": ("类型", 位宽)}
        """
        pattern = r's\.(\w+)\s*=\s*(Input|Output)\((\d+)\)'
        matches = re.findall(pattern, file_content)
        
        port_defs = {}
        for port_name, port_type, width in matches:
            port_defs[port_name] = (port_type, int(width))
        return port_defs

    def _generate_io_class_code(self, port_defs: dict) -> str:
        """
        根据端口定义生成IO类代码字符串
        
        Args:
            port_defs: 端口定义字典
        
        Returns:
            IO类代码字符串
        """
        code_lines = [
            "from comopy.hdl import IOStruct, Input, Output",
            "",
            "class IO(IOStruct):",
            "    \"\"\"自动生成的IOStruct类\"\"\""
        ]
        for port_name, (port_type, width) in port_defs.items():
            code_lines.append(f"    {port_name} = {port_type}({width})")
        
        return '\n'.join(code_lines)

# 废弃方案：因ports方法被assemble和HDLStage重复执行导致冲突
# def generate_io_class(top: HDL.RawModule) -> type:
#     class DynamicIOStruct(IOStruct):
#         pass
#     for name, port in vars(top).items():
#         if isinstance(port, HDL.Signal):
#             if port.direction == HDL.IODirection.In:
#                 setattr(DynamicIOStruct, name, Input(port.nbits))
#             elif port.direction == HDL.IODirection.Out:
#                 setattr(DynamicIOStruct, name, Output(port.nbits))
#     return DynamicIOStruct


def test_adder_runner():
    """测试Adder模块构建与仿真"""
    runner = ComoPy()
    adder_path = str(Path(__file__).parent.parent / "debug"/"model" / "adder.py")
    
    runner.build(
        file_path=adder_path, 
        top_module_name="Adder",
    )

if __name__ == "__main__":
    test_adder_runner()