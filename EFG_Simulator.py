'''
Date: 2022.12.23
Title: 어구자동식별모니터링 데이터 시뮬레이터(Phase)
By: Kang Jin Seong
'''

import numpy as np
from pylfsr import LFSR
import matplotlib.pyplot as plt
from scipy.signal import upfirdn
from scipy.fftpack import fft, ifft, fftshift, ifftshift
from scipy import signal
from matplotlib import font_manager, rc
import ICAT_Simulator as ICAT

font_path = "C:/Windows/Fonts/gulim.ttc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)



class Simulator(ICAT.Analytic):
    def __init__(self):
        super().__init__()
        self.Rc = 32e3
        self.Tc = 1/self.Rc
        self.Fs = self.Rc * 4
        self.taps = [8,7,6,1]
    def SIG_GEN_EFG(self):
        pass

    def main(self):
       coef, y = self.SIG_GEN(2,1,8,0)
       self.Demod(coef= coef, y = y,window_size=1, cut_f= 32e3)

if __name__ == "__main__":
    print('SSS')
    A = Simulator()
    A.main()
    plt.show()