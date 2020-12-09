import numpy as np
from numpy.random import default_rng, PCG64
import warnings

class RNG_PCG:
    def __init__(self, seed = 0):
        self.state = PCG64(seed)
        self.r = default_rng(self.state)
    def rng(self, high = 2**32, low = 0, numbers = 1):
        #return np.random.randint(low, high, numbers)
        return self.r.integers(low, high, numbers)
    def fast_forward(self, t):
        self.state.advance(t)

class RNG_URAND:
    A = np.int32(843314861)
    B = np.int32(453816693)
    def __init__(self, xn = 0):
        self.xn = np.int32(xn)
    
    def rng(self, high = 2**32, low = None, numbers = None):
        warnings.filterwarnings('ignore')
        self.xn = np.int32(RNG_URAND.A*self.xn + RNG_URAND.B)
        return self.xn