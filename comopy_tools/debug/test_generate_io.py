import comopy.hdl as HDL
from comopy.hdl import IOStruct, Input, Output
from comopy import *

class Adder(RawModule):
    """一个简单的加法器：X = A + B"""

    @build
    def ports(s):
        s.A = Input(8)   # 8位输入
        s.B = Input(8)
        s.X = Output(8)  # 8位输出

    @comb
    def update(s):
        s.X /= s.A + s.B  # 加法运算

def generate_io_class(top: HDL.RawModule) -> type:
    """
    动态生成一个类，继承自 IOStruct，并根据模块端口生成成员。
    """
    # 获取该模块类的所有端口（通过build方法定义的端口）
    port_definitions = top.get_builders()
    
    # 动态创建一个新的类，用于存储端口
    class DynamicIOStruct(IOStruct):
        pass
    
    # 创建 _part_names 列表，存储所有端口的名称
    part_names = []
    
    # 遍历所有 build 方法，提取端口信息
    for builder in port_definitions:
        if builder.__name__ == "ports":  # 只关心 ports 方法
            # 获取端口定义（例如 Input(8), Output(8)）
            for param_name, param in builder.__annotations__.items():
                if isinstance(param, Input):
                    # 动态添加端口
                    setattr(DynamicIOStruct, param_name, Input(param.nbits))
                    part_names.append(param_name)  # 记录端口名称
                elif isinstance(param, Output):
                    # 动态添加端口
                    setattr(DynamicIOStruct, param_name, Output(param.nbits))
                    part_names.append(param_name)  # 记录端口名称

    # 确保 _part_names 属性存在
    DynamicIOStruct._part_names = part_names
    
    # 检查生成的类是否包含端口
    print(f"Generated class {DynamicIOStruct.__name__} with ports: {dir(DynamicIOStruct)}")
    
    return DynamicIOStruct

if __name__ == '__main__':
    # 创建 Adder 类的实例
    top = Adder()

    # 生成对应的 IO 类
    io_class = generate_io_class(top)
    print(f"Generated IO class: {io_class}")
    
    # 创建 IO 类实例
    io_instance = io_class()

    # 检查生成的类是否包含端口
    print(f"Has port A: {'A' in dir(io_instance)}")
    print(f"Has port B: {'B' in dir(io_instance)}")
    print(f"Has port X: {'X' in dir(io_instance)}")