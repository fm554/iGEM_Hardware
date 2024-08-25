import numpy as np
import matplotlib.pyplot as plt

def sine_wave(samples, amplitude):
    #generate a wavelength of sinewave
    x = np.arange(samples)
    y = amplitude * np.sin(2 * np.pi * x / samples)

    return y


def square_wave(samples, amplitude):
    #generate a wavelength of squarewave
    x = np.arange(samples)
    y = amplitude * np.sign(np.sin(2 * np.pi * x / samples))

    return y

def triangle_wave(samples, amplitude):
    #generate a wavelength of triangle wave
    x = np.arange(samples)
    y = amplitude * np.arcsin(np.sin(2 * np.pi * x / samples))

    return y

def wave_to_string(wave):
    #convert wave to string
    wave_str = ""
    for i in range(len(wave)):
        wave_str += str(wave[i]) + ","
    return wave_str

def wave_gen(samples, amplitude, wave_type):
    #generate wave
    if wave_type == "sine":
        wave = sine_wave(samples, amplitude)
    elif wave_type == "square":
        wave = square_wave(samples, amplitude)
    elif wave_type == "triangle":
        wave = triangle_wave(samples, amplitude)
    else:
        wave = np.zeros(samples)

    return np.round(wave,0).astype(int)


if __name__ == "__main__":
    samples = 64
    amplitude = 100
    wave_type = "sine"
    wave = wave_gen(samples, amplitude, wave_type)
    wave_str = wave_to_string(wave)
    print(wave_str)
    plt.step(range(len(wave)), wave)
    plt.show()
    #print(wave)