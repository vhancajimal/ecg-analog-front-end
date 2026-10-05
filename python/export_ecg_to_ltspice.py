from pathlib import Path

import numpy as np
import wfdb


# ---------------------------------------------------------
# Settings
# ---------------------------------------------------------

record_name = "100"
fs = 360

start_sec = 5
duration_sec = 10

start_sample = start_sec * fs
end_sample = (start_sec + duration_sec) * fs


# ---------------------------------------------------------
# Load ECG from MIT-BIH
# ---------------------------------------------------------

record = wfdb.rdrecord(
    record_name,
    pn_dir="mitdb",
    sampfrom=start_sample,
    sampto=end_sample,
    channels=[0]
)

ecg_mV = record.p_signal[:, 0]


# ---------------------------------------------------------
# Remove DC component
# ---------------------------------------------------------

ecg_mV = ecg_mV - np.mean(ecg_mV)

# Convert mV -> V for LTspice
ecg_V = ecg_mV * 1e-3


# ---------------------------------------------------------
# Time vector
# ---------------------------------------------------------

time = np.arange(len(ecg_V)) / fs


# ---------------------------------------------------------
# Output directory
# ---------------------------------------------------------

repo_root = Path(__file__).resolve().parents[1]

output_dir = repo_root / "ltspice" / "inputs"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "ecg_record100_10s.txt"


# ---------------------------------------------------------
# Export LTspice PWL file
# ---------------------------------------------------------

with open(output_file, "w") as f:
    for t, v in zip(time, ecg_V):
        f.write(f"{t:.6f} {v:.9f}\n")


# ---------------------------------------------------------
# Information
# ---------------------------------------------------------

vpp_mV = (np.max(ecg_V) - np.min(ecg_V)) * 1000

print("ECG waveform exported successfully.")
print(f"Record: MIT-BIH {record_name}")
print(f"Duration: {duration_sec} s")
print(f"Samples: {len(ecg_V)}")
print(f"Sampling frequency: {fs} Hz")
print(f"ECG amplitude: {vpp_mV:.3f} mVpp")
print(f"Output file: {output_file}")