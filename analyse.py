import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft, fftfreq
import scipy
import os
from os.path import isfile, join
import numpy as np
# rate, data = wav.read('opsix/normed_opsix-ratio1-1-output-5.wav')
# print(max(data))
# data = [x/32577 for x in data]
# print(max(data))
# time_period = 1 / rate
# print(data[:20])
# N = len(data)
# fft_out = fft(data)
# yf = fft(data) / len(data)
# xf = fftfreq(N, 1/rate)[:N//2]
# print(max(abs(yf)))
# ## put this out and do it for each sideband
# print(xf[100:1000])
# i = 0
# while xf[i] < 130.8 * 2:
#     i += 1
# # what if this comes from a negative amplitude?
# second_harmonic_amp = abs(yf[i] * 2)
# f = lambda a : scipy.special.jv(1.0, a) - second_harmonic_amp
# print(scipy.optimize.brentq(f, 0, 2))

# x = [0.43, 0.65, 0.83, 0.97]
# y = [2.40, 5.52, 8.65, 11.79]

# # %matplotlib inline
# # plt.plot(xf[:10000], 2 * np.abs(yf[0:10000]))
# plt.plot(x, y)
# plt.show()

## This function assumes 16bit signed integer format!
def read_wav_normalised(wav_path):
    rate, data = wav.read(wav_path)
    data = [x/32767 for x in data]
    return rate, data

def get_file_list(path):
    files = [join(path, f) for f in os.listdir(path) if isfile(join(path, f)) and f.endswith(".wav")]
    print(files)
    return files

def get_ffts(wav_path):
    rate, data = read_wav_normalised(wav_path)
    # Assumes s16 format
    time_period = 1 / rate
    N = len(data)
    yf = fft(data) / N
    xf = fftfreq(N, time_period)[:N//2]
    return xf, yf

def get_harominic_index(fundamental, harmonic, xf):
    i = 0
    while xf[i] < (fundamental * harmonic):
        i += 1
    return i

def get_fundamental_amplitude(fundamental, xf, yf):
    i = get_harominic_index(fundamental, 1, xf)
    return abs(yf[i] * 2)

## Need to consider negative amplitudes, so need to be able to select the intervals
def reverse_bessel_function(fundamental_amp):
    f = lambda a : scipy.special.jv(0.0, a) - fundamental_amp
    result = scipy.optimize.brentq(f, 0, 2.4)
    return result

def estimate_modulation_index(wav_path):
    xf, yf = get_ffts(wav_path)
    fundamental_amp = get_fundamental_amplitude(130.8, xf, yf)
    print(fundamental_amp)
    modulation_index_estimate = reverse_bessel_function(fundamental_amp)
    return modulation_index_estimate
    
if __name__ == "__main__":
    path = "opsix"
    files = get_file_list(path)
    for f in files:
        print(f)
        result = estimate_modulation_index(f)
        print(result)