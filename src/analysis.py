"""Signal analysis utilities: FFT, spectrogram, peak detection."""
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def compute_spectrum(iq_samples, sample_rate, nfft=4096, window='hann'):
    # iq_samples: complex or real numpy array
    if np.iscomplexobj(iq_samples):
        x = iq_samples
    else:
        x = iq_samples.astype(np.float64)
    window_vals = signal.get_window(window, nfft)
    freqs, Pxx = signal.welch(x, fs=sample_rate, window=window_vals, nperseg=nfft, return_onesided=False)
    # Shift zero frequency to center
    Pxx = np.fft.fftshift(Pxx)
    freqs = np.fft.fftshift(freqs) - sample_rate/2
    return freqs, 10 * np.log10(Pxx + 1e-12)


def detect_peaks(freqs, psd_db, height_db=-60, distance_hz=1000, sample_rate=48000):
    # Convert distance_hz to samples for peak finder based on freq spacing
    if len(freqs) < 2:
        return []
    df = abs(freqs[1] - freqs[0])
    distance_bins = max(1, int(distance_hz / df))
    peaks, props = signal.find_peaks(psd_db, height=height_db, distance=distance_bins)
    results = []
    for p in peaks:
        results.append({'freq_hz': freqs[p], 'power_db': psd_db[p]})
    return results


def compute_spectrogram(iq_samples, sample_rate, nperseg=1024, noverlap=512, cmap='viridis'):
    if np.iscomplexobj(iq_samples):
        x = iq_samples
    else:
        x = iq_samples.astype(np.float64)
    freqs, times, Sxx = signal.spectrogram(x, fs=sample_rate, nperseg=nperseg, noverlap=noverlap, mode='magnitude')
    # convert to dB
    Sxx_db = 20 * np.log10(Sxx + 1e-12)
    return freqs, times, Sxx_db


def save_spectrogram_image(freqs, times, Sxx_db, out_path, vmax=None, vmin=None):
    plt.figure(figsize=(8,4))
    plt.pcolormesh(times, freqs, Sxx_db, shading='gouraud', cmap='viridis', vmin=vmin, vmax=vmax)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar(label='Magnitude (dB)')
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


if __name__ == "__main__":
    # Quick test
    from signal_sim import generate_multi_tone
    sr = 48000
    sig = generate_multi_tone([(1000, 1.0), (4000, 0.7), (8000, 0.5)], sr, 0.5)
    f, p = compute_spectrum(sig, sr)
    peaks = detect_peaks(f, p, height_db=-50)
    print('Peaks:', peaks)
    freqs, times, Sxx_db = compute_spectrogram(sig, sr)
    save_spectrogram_image(freqs, times, Sxx_db, 'demo_spec.png')
    print('Saved demo_spec.png')
