'''
Date: 2022.12.28
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
        self.decimaterate = 16
        self.dFs = int(self.Fs / self.decimaterate)
        self.taps = [8,7,6,1]
    def analog(self):
        S_BB, y =self.mod_IQ(q = 2,r = 1,order = 8, index = 0)
        t1 = np.arange(0,len(y)/self.Fs, 1/self.Fs)
        Demode_carrier_I = np.cos(2*np.pi*self.Rc*t1)
        Demode_carrier_Q = -np.sin(2*np.pi*self.Rc*t1)
        rx_Q = y * Demode_carrier_Q
        rx_I = y * Demode_carrier_I
        fir = signal.firwin(512, cutoff=10000,fs=self.Fs, pass_zero='lowpass')
        result_r_I = signal.lfilter(fir, [1.0],rx_I)
        result_r_Q = signal.lfilter(fir, [1.0],rx_Q)
        result = result_r_I.real + 1j*result_r_Q.imag
        NFFT = len(result)
        RESULT = fftshift(fft(result,NFFT)*(1/NFFT))
        f = np.arange(start = -NFFT/2, stop = NFFT/2)*(self.Fs/NFFT)      
        # plt.figure()
        # plt.subplot(2,1,1)
        # plt.plot(t1,result)
        # plt.subplot(2,1,2)
        # plt.plot(f,abs(RESULT))
        return S_BB, result, t1, f

    def ADC(self):
        S_BB , result,t,f = self.analog()
        d_result = signal.decimate(result, self.decimaterate)
        d_S_BB = signal.decimate(S_BB, self.decimaterate)
        t1 = np.arange(0, len(d_result)/self.dFs, 1/self.dFs)

        plt.figure()
        plt.subplot(3,1,1)
        plt.plot(t,result)
        plt.subplot(3,1,2)
        plt.plot(t1,d_result)
        plt.subplot(3,1,3)
        plt.plot(-S_BB) 

        filtered_y = signal.correlate(d_S_BB.real, d_result.real, method = 'fft')
        en_filtered_y = abs(signal.hilbert(np.diff(filtered_y))) 
        plt.figure()
        plt.plot(en_filtered_y)
    def main(self):
        self.ADC()
    #    self.Demod(coef= coef, y = y,window_size=1, cut_f= 32e3)

if __name__ == "__main__":
    print('SSS')
    A = Simulator()
    A.main()
    plt.show()