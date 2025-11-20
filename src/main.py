"""CLI entrypoint for demo monitor and quick analysis."""
import argparse
from . import monitor
from . import analysis
from .signal_sim import generate_multi_tone


def main():
    parser = argparse.ArgumentParser(description='Radio Signal Analysis & Monitoring Demo')
    parser.add_argument('--demo', action='store_true', help='Run a short demo: generate signal, compute spectrum')
    parser.add_argument('--monitor', action='store_true', help='Run continuous monitor (simulated)')
    parser.add_argument('--sr', type=int, default=48000, help='Sample rate')
    args = parser.parse_args()

    if args.demo:
        sr = args.sr
        sig = generate_multi_tone([(1000, 1.0), (4000, 0.7), (8000, 0.5)], sr, 0.5)
        freqs, p = analysis.compute_spectrum(sig, sr)
        peaks = analysis.detect_peaks(freqs, p, height_db=-50)
        print('Detected peaks:', peaks)
        freqs_spec, times_spec, Sxx_db = analysis.compute_spectrogram(sig, sr)
        analysis.save_spectrogram_image(freqs_spec, times_spec, Sxx_db, 'demo_spec.png')
        print('Wrote demo_spec.png')
    elif args.monitor:
        monitor.run_monitor(sample_rate=args.sr)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
