"""Monitoring loop that ingests IQ frames, runs analysis, and logs alerts."""
import time
import numpy as np
from .signal_sim import generate_multi_tone
from .analysis import compute_spectrum, detect_peaks, compute_spectrogram, save_spectrogram_image


def run_monitor(sample_rate=48000, frame_duration=0.5, threshold_db=-40, save_every=10):
    frame_len = int(sample_rate * frame_duration)
    iteration = 0
    try:
        while True:
            # In real use, replace with SDR read. Here we simulate:
            tones = [(1000, 1.0), (5000 + 100*iteration, 0.6 if iteration % 5 else 1.0)]
            iq = generate_multi_tone(tones, sample_rate, frame_duration)
            freqs, psd_db = compute_spectrum(iq, sample_rate)
            peaks = detect_peaks(freqs, psd_db, height_db=threshold_db, distance_hz=200)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            if peaks:
                for p in peaks:
                    print(f"{timestamp} ALERT: Detected signal at {p['freq_hz']:.0f} Hz, {p['power_db']:.1f} dB")
            else:
                print(f"{timestamp} OK: no signals above {threshold_db} dB")
            # Save spectrogram occasionally
            if iteration % save_every == 0:
                freqs_spec, times_spec, Sxx_db = compute_spectrogram(iq, sample_rate)
                out = f'spec_{iteration:04d}.png'
                save_spectrogram_image(freqs_spec, times_spec, Sxx_db, out)
                print(f"Saved {out}")
            iteration += 1
            time.sleep(frame_duration)
    except KeyboardInterrupt:
        print('Monitor stopped by user')


if __name__ == "__main__":
    run_monitor()
