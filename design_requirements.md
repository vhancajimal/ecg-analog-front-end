# Design Requirements

## Objective

Design and simulate an analog front-end for ECG signal acquisition and conditioning.

The system should amplify a low-amplitude differential ECG signal while reducing baseline drift, high-frequency noise, and common-mode interference.

The design is intended for simulation and educational analysis only and is not a clinically validated medical device.

## Input Signal

- Nominal ECG differential amplitude: 1 mVpp
- Test range: 0.5–5 mVpp
- Relevant ECG frequency range: approximately 0.5–40 Hz
- Power-line common-mode interference: 50 Hz
- Electrode DC offset: tested up to ±300 mV
- Electrode impedance mismatch will be considered

## Signal Conditioning

Target signal chain:

ECG input  
→ instrumentation amplifier  
→ high-pass filter  
→ low-pass filter  
→ additional gain  
→ conditioned output

## Target Specifications

| Parameter | Target |
|---|---:|
| Overall differential gain | ~1000 V/V |
| First-stage gain | 10–20 V/V |
| High-pass cutoff | ~0.5 Hz |
| Low-pass cutoff | ~40 Hz |
| CMRR | > 80 dB |
| Supply voltage | 5 V |
| Reference voltage | 2.5 V |

## Analyses

The design will be evaluated using:

- transient analysis
- AC frequency response
- common-mode rejection analysis
- resistor tolerance analysis
- electrode impedance imbalance
- input offset analysis
- noise analysis
- output saturation/headroom analysis
