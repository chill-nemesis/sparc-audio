import numpy as np
import sounddevice as sd


def sine_tone(frequency, duration, sample_rate):
    # Generate a sine wave
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(frequency * 2 * np.pi * t)

    sd.play(wave, sample_rate)
    sd.wait()
