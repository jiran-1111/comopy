from comopy import *  # 导入库

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

