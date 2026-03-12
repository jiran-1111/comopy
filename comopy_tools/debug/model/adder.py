from comopy import *
class Adder(RawModule):
    """一个简单的加法器：X = A + B"""

    @build
    def ports(myport):
        myport.A = Input(8)   # 8位输入
        myport.B = Input(8)
        myport.X = Output(8)  # 8位输出

    @comb
    def update(myport):
        myport.X /= myport.A + myport.B  # 加法运算


class IO(IOStruct):
        A = Input(8)
        B = Input(8)
        X = Output(8)