from comopy import *  # 导入库
import comopy.hdl as HDL

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

from comopy import *

def generate_io_class(top: HDL.RawModule) -> type:
    """生成IOStruct类"""
    
    # 动态创建一个新的类，继承自IOStruct
    class DynamicIOStruct(IOStruct):
        pass
    
    # 遍历并动态地为DynamicIOStruct添加端口
    for name, port in vars(top).items():
        if isinstance(port, HDL.Signal):
            if port.direction == HDL.IODirection.In:
                setattr(DynamicIOStruct, name, Input(port.nbits))
            elif port.direction == HDL.IODirection.Out:
                setattr(DynamicIOStruct, name, Output(port.nbits))

    # 返回生成的IOStruct类
    return DynamicIOStruct


# 创建 Adder 模块的实例 
if __name__ == '__main__': 
    adder = Adder()  # 创建Adder模块的实例
    adder.assemble()  # assemble端口，并初始化 
    
    # 列举所有信号及其名称
    for name, port in vars(adder).items():
        if isinstance(port, HDL.Signal):  # 判断是否是Signal类型（Wire, Logic等）
            print(f"Signal name: {name}, Direction: {port.direction}")
    
    print(adder.X.nbits)  # 8位输出信号的位宽应该是8
    print({type(adder)})
    # 生成对应的IOStruct类
    IOClass = generate_io_class(adder)
    print({type(IOClass)})
    # 创建DynamicIOStruct实例
    io_instance = IOClass()  # 创建实例
    print({type(IOClass)})
    print(io_instance.A.nbits)  # 8位输入信号的位宽应该是8
    print(io_instance.B.nbits)  # 8位输入信号的位宽应该是8
    print(io_instance.X.nbits)  # 8位输出信号的位宽应该是8
    print(io_instance._has_input)  # 应该有输入信号
    print(io_instance._has_output)  # 应该有输出信号
