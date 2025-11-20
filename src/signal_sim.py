"""Signal simulator for complex baseband IQ samples.

Provides simple AM and FM modulators and a multi-tone generator useful for testing analysis/monitoring code
without SDR hardware.
"""
import numpy as np


def generate_tone(freq_hz, sample_rate, duration_s, amplitude=1.0, phase=0.0):
    t = np.arange(0, int(duration_s * sample_rate)) / sample_rate
    return amplitude * np.exp(1j * (2 * np.pi * freq_hz * t + phase))


def generate_am(carrier_hz, mod_freq_hz, sample_rate, duration_s, mod_index=0.5, carrier_amp=1.0):
    t = np.arange(0, int(duration_s * sample_rate)) / sample_rate
    mod = 1.0 + mod_index * np.cos(2 * np.pi * mod_freq_hz * t)
    carrier = carrier_amp * np.cos(2 * np.pi * carrier_hz * t)
    # Represent as real passband-like; convert to complex baseband by shifting (simulate)
    # For testing it's fine to return complex representation using analytic signal
    analytic = np.real(carrier * mod)
    return analytic + 0j


def generate_fm(carrier_hz, mod_freq_hz, sample_rate, duration_s, freq_dev_hz=5000, carrier_amp=1.0):
    t = np.arange(0, int(duration_s * sample_rate)) / sample_rate
    # integrate modulating signal to produce phase deviation
    mod = np.sin(2 * np.pi * mod_freq_hz * t)
    phase = 2 * np.pi * carrier_hz * t + 2 * np.pi * freq_dev_hz * np.cumsum(mod) / sample_rate
    return carrier_amp * np.exp(1j * phase)


def generate_multi_tone(tones, sample_rate, duration_s):
    """tones: list of (freq_hz, amplitude)
    Returns complex IQ samples (sum of tones)
    """
    t = np.arange(0, int(duration_s * sample_rate)) / sample_rate
    out = np.zeros_like(t, dtype=np.complex128)
    for f, a in tones:
        out += a * np.exp(1j * 2 * np.pi * f * t)
    # normalize
    max_a = np.max(np.abs(out))
    if max_a > 0:
        out /= max_a
    return out


if __name__ == "__main__":
    # Quick local demo generator
    import matplotlib.pyplot as plt
    sr = 48000
    dur = 0.05
    sig = generate_multi_tone([(1000, 1.0), (4000, 0.7), (8000, 0.5)], sr, dur)
    plt.plot(np.real(sig)[:1024])
    plt.title('Demo multi-tone (real part)')
    plt.show()
