# copilot-cli-main

**Radio Signal Analysis & Monitoring (Python demo)**

- **Description**: Small demo that simulates complex IQ signals, computes spectra and spectrograms, detects strong carriers, and runs a monitoring loop that prints alerts and saves spectrogram images.

- **Files created**:
	- `requirements.txt`: Python deps
	- `src/signal_sim.py`: signal generator (AM/FM/multi-tone)
	- `src/analysis.py`: FFT, spectrogram, peak detection, image saving
	- `src/monitor.py`: simulated continuous monitor with alerts
	- `src/main.py`: CLI entrypoint (`--demo` or `--monitor`)

- **Install** (PowerShell):

```powershell
cd C:\Users\Taylor\Downloads\copilot-cli-main
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

- **Run demo** (generates `demo_spec.png`):

```powershell
python -m src.main --demo
```

- **Run simulated monitor** (prints alerts and saves spectrograms):

```powershell
python -m src.main --monitor
```

- **Using real RTL-SDR**: Install `pyrtlsdr` and modify `src/monitor.py` to read frames from the device instead of `generate_multi_tone`. I can help adapt the code once you confirm you have an RTL-SDR.

- **Next steps I can do**:
	- Hook up `pyrtlsdr` and streaming input
	- Add FM/AM demodulation utilities
	- Add logging to file and alerting (email/HTTP)
	- Add configuration via YAML/JSON

If you'd like, I can now attach RTL-SDR capture support or run the demo here and show sample outputs. Which would you prefer?
