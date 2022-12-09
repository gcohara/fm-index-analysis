import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft, fftfreq
import scipy
import os
from math import exp
from os.path import isfile, join
import numpy as np

## This function assumes 16bit signed integer format!
def read_wav_normalised(wav_path):
    rate, data = wav.read(wav_path)
    data = [x/32767 for x in data]
    return rate, data

def get_file_list(path):
    files = [join(path, f) for f in os.listdir(path) if isfile(join(path, f)) and f.endswith(".wav")]
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
## Would be good to store some state
def reverse_bessel_function(fundamental_amp, output_level):
    f = get_reverse_bessel(fundamental_amp, output_level)
    (a,b) = get_solver_range(output_level)
    result = scipy.optimize.brentq(f, a, b)
    return result

## Get the function we want to solve, using prior knowledge of the output levels that
## correspond to zeros of the bessel function
## If it's x axis, subtract amp off, if below we add it
def get_reverse_bessel(fundamental_amp, output_level):
    opsix_zero_levels = [43, 65, 81, 95]
    is_above_x_axis = output_level < opsix_zero_levels[0] or \
    output_level in range(opsix_zero_levels[1], opsix_zero_levels[2]) or \
    output_level > opsix_zero_levels[3]
    
    if is_above_x_axis:
        f = lambda a : scipy.special.jv(0.0, a) - fundamental_amp
    else:
        f = lambda a : scipy.special.jv(0.0, a) + fundamental_amp
    return f

## ranges should be between two inflection points of the bessel function
## they were obtained from here https://mathworld.wolfram.com/BesselFunctionZeros.html
def get_solver_range(output_level):
    inflection_points = [54, 73, 88]
    if output_level < inflection_points[0]:
        return (0,3.8317)
    elif output_level in range(inflection_points[0],inflection_points[1]):
        return (3.8317, 7.0156)
    elif output_level in range(inflection_points[1],inflection_points[2]):
        return (7.0156, 10.1735)
    elif output_level > inflection_points[2]:
        return (10.1735, 13.3237)
        

def estimate_modulation_index(wav_path,output_level):
    xf, yf = get_ffts(wav_path)
    fundamental_amp = get_fundamental_amplitude(130.8, xf, yf)
    modulation_index_estimate = reverse_bessel_function(fundamental_amp,output_level)
    return modulation_index_estimate
    
if __name__ == "__main__":
    path = "opsix"
    files = sorted(get_file_list(path))
    results = []
    for (i, f) in enumerate(files):
        output_level = i * 5
        result = estimate_modulation_index(f, output_level)
        results.append(result)
    x = [i * 5 for i in range(len(results))]
    f = lambda xs, b : [exp(x * b) - (1.0 - results[0]) for x in xs]
    curve_results = scipy.optimize.curve_fit(f, x, results)
    b = curve_results[0][0]    
    curve_xs = [x for x in range(100)]
    curve_ys = f(curve_xs, b)
    
    plt.plot(x, results)
    plt.plot(curve_xs, curve_ys)
    plt.show()
