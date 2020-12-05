import numpy as np
import warnings


class RNG:
    A = 843314861
    B = 453816693
    def __init__(self, seed = 0):
        self.xn = seed
    def __xn_to_int(self):
        warnings.filterwarnings('ignore')
        return np.int32(self.xn & 0xffffffff)
    def rng(self):
        self.xn = LRNG.A*self.xn + LRNG.B
        return self.__xn_to_int()
    def fast_forward(self, t):
        self.xn = self.xn * RNG.A ** (t - 1) + RNG.B * (RNG.A ** t - 1) // (RNG.A - 1)
'''
class RNG:
    A = np.int32(843314861)
    B = np.int32(453816693)
    def __init__(self, xn = 0):
        self.xn = np.int32(xn)
    
    def rng(self):
        #warnings.filterwarnings('ignore')
        self.xn = np.int32(RNG.A*self.xn + RNG.B)
        return self.xn
''' 
rng = RNG()