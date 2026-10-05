# ECG Analog Front-End Design & Simulation

A simulated ECG analog front-end (AFE) developed in LTspice and supported by Python-based analysis.

The project focuses on the analog signal-conditioning stages that precede digital ECG processing: differential amplification, common-mode rejection, band-limiting, final amplification, resistor-tolerance analysis, output headroom, realistic op-amp modeling, and validation with a real ECG waveform.

This project complements my digital ECG signal-processing project:

https://github.com/vhancajimal/ecg-signal-processing

---

## Project Overview

Electrocardiogram (ECG) signals have small differential amplitudes and may be affected by common-mode interference, baseline variations, and out-of-band noise.

The objective of this project was to design and simulate a single-supply analog front-end capable of:

- amplifying a small differential ECG signal,
- rejecting common-mode interference,
- limiting the signal bandwidth,
- centering the output around a 2.5 V reference,
- providing sufficient gain for subsequent digitization,
- evaluating the influence of resistor mismatch on CMRR,
- characterizing output headroom and clipping,
- comparing generic and realistic op-amp models,
- and processing a real ECG waveform from the MIT-BIH Arrhythmia Database.

The complete simulated signal chain is:

```text
Differential ECG input
        |
        v
3-op-amp instrumentation amplifier
        |
        v
High-pass filter
        |
        v
Low-pass filter
        |
        v
Post-gain stage
        |
        v
Conditioned analog ECG output
```

The circuit operates from a 0–5 V single supply and uses a 2.5 V reference voltage so that the ECG waveform is centered within the available output range.

---

## Design Summary

| Parameter | Value |
|---|---:|
| Supply voltage | 0–5 V |
| Reference voltage | 2.5 V |
| Initial sinusoidal test signal | 1 mVpp at 10 Hz |
| Instrumentation-amplifier gain | ~5 V/V |
| High-pass theoretical cutoff | ~0.482 Hz |
| Complete band-pass lower cutoff | ~0.452 Hz |
| Complete band-pass upper cutoff | ~43.57 Hz |
| Post-gain stage | 100 V/V |
| Nominal active-stage gain | 500 V/V |
| Simulated complete gain at 10 Hz | ~465 V/V |
| Common-mode test frequency | 50 Hz |
| Common-mode test amplitude | 200 mVpp |
| Real ECG validation | MIT-BIH Record 100 |

The nominal active-stage gain is approximately:

```text
5 × 100 = 500 V/V
```

The complete simulated gain is slightly lower because the passive filter network introduces attenuation.

---

# 1. Instrumentation Amplifier

The input stage uses a three-op-amp instrumentation-amplifier topology.

## First Stage

The first two amplifiers use:

```text
R1 = 10 kΩ
R3 = 10 kΩ
Rg = 5 kΩ
```

The theoretical differential gain is:

```text
G = 1 + 2R/Rg
```

Therefore:

```text
G = 1 + 2(10 kΩ)/(5 kΩ)
  = 5
```

For a 1 mVpp differential input, this stage produces approximately 5 mVpp before the subsequent filtering and post-amplification stages.

## Difference Amplifier

The third op-amp uses four nominally matched 20 kΩ resistors:

```text
R4 = 20 kΩ
R5 = 20 kΩ
R6 = 20 kΩ
R7 = 20 kΩ
```

This stage performs differential subtraction while referencing the output around:

```text
VREF = 2.5 V
```

The selected polarity in the difference-amplifier stage produces an inverted final ECG waveform relative to the defined differential input `V(in_plus,in_minus)`. This inversion does not affect the intended signal-conditioning behavior.

---

# 2. Common-Mode Rejection Analysis

To evaluate common-mode rejection, a 50 Hz common-mode signal was applied simultaneously to both input paths.

The test common-mode waveform was:

```text
VCM = 2.5 V + 0.1*sin(2*pi*50*t)
```

This corresponds to:

```text
200 mVpp common-mode interference
```

With matched resistors, the difference-amplifier stage strongly rejects this common-mode component.

To investigate resistor-tolerance sensitivity, one 20 kΩ resistor in the subtraction stage was varied according to:

```text
R = 20 kΩ * (1 + mismatch)
```

The simulated mismatch values were:

```text
0.1 %
0.5 %
1.0 %
2.0 %
```

## Differential Gain

The differential gain was measured independently for each mismatch value.

| Resistor mismatch | Differential gain Ad |
|---:|---:|
| 0.1 % | 5.0019 |
| 0.5 % | 5.0167 |
| 1.0 % | 5.0355 |
| 2.0 % | 5.0727 |

## Common-Mode Gain and CMRR

The common-mode gain was calculated as:

```text
Acm = Vout_CM_pp / Vin_CM_pp
```

CMRR was calculated using:

```text
CMRR = 20*log10(Ad/Acm)
```

The simulated results were:

| Resistor mismatch | Common-mode gain Acm | CMRR |
|---:|---:|---:|
| 0.1 % | 0.000502 | ~80.0 dB |
| 0.5 % | 0.002501 | ~66.0 dB |
| 1.0 % | 0.005001 | ~60.1 dB |
| 2.0 % | 0.010002 | ~54.1 dB |

The results show that common-mode rejection is strongly dependent on resistor matching in the difference-amplifier stage.

Even relatively small mismatch significantly increases common-mode gain and reduces CMRR.

### CMRR Result

![CMRR vs resistor mismatch](results/cmrr_vs_resistor_mismatch.png)

### Common-Mode Gain Result

![Common-mode gain vs resistor mismatch](results/common_mode_gain_vs_resistor_mismatch.png)

---

# 3. High-Pass Filter

A passive high-pass stage was added after the instrumentation amplifier.

Component values:

```text
C1 = 2.2 µF
R8 = 150 kΩ
```

Because the circuit uses a single supply, the resistor is referenced to `VREF = 2.5 V` rather than directly to ground.

The theoretical cutoff frequency is:

```text
fc = 1 / (2*pi*R*C)
```

which gives:

```text
fc ≈ 0.482 Hz
```

The LTspice AC-analysis measurement produced:

```text
HP_FC = 0.4823447 Hz
```

This closely matches the theoretical value.

---

# 4. Low-Pass Filter and Complete Band-Pass Response

The low-pass stage uses:

```text
R9 = 39 kΩ
C2 = 100 nF
```

Its isolated theoretical cutoff is approximately:

```text
fc ≈ 40.8 Hz
```

The high-pass and low-pass stages are cascaded without an active buffer between them.

Because passive RC stages load each other, the complete response does not exactly equal the cutoff frequencies calculated for each stage independently.

AC analysis of the complete passive filter network produced:

| Parameter | Simulated value |
|---|---:|
| Peak magnitude | -0.484 dB |
| Peak-response frequency | 4.47 Hz |
| Lower cutoff frequency | 0.452 Hz |
| Upper cutoff frequency | 43.57 Hz |

The -3 dB cutoff frequencies were determined relative to the actual pass-band peak rather than an absolute 0 dB level.

This demonstrates the loading interaction between cascaded passive filters.

---

# 5. Post-Gain Stage

After band-limiting, a non-inverting amplifier provides the final amplification.

Component values:

```text
R10 = 1 kΩ
R11 = 99 kΩ
```

The gain is:

```text
Gpost = 1 + R11/R10
      = 1 + 99 kΩ / 1 kΩ
      = 100
```

The non-inverting input receives the filtered ECG signal.

The feedback network is referenced to `VREF = 2.5 V`, giving:

```text
Vafe_out = VREF + 100 * (Vlp_out - VREF)
```

This preserves the 2.5 V DC operating point while amplifying the ECG component around it.

---

# 6. Complete Front-End Gain

Using a 1 mVpp differential sinusoidal input at 10 Hz, the complete front-end produces approximately:

```text
Vout ≈ 0.465 Vpp
```

The resulting overall gain is approximately:

```text
Atotal ≈ 0.465 Vpp / 0.001 Vpp
       ≈ 465 V/V
```

This is slightly below the nominal active-stage gain:

```text
5 × 100 = 500 V/V
```

because the passive band-pass network attenuates the signal slightly at 10 Hz.

---

# 7. Input Range and Output Headroom

The complete front-end was tested with different differential input amplitudes to evaluate output headroom and identify the onset of saturation.

The test signal was a 10 Hz differential sinusoid.

Measured results:

| Differential input | Output maximum | Output minimum | Output amplitude |
|---:|---:|---:|---:|
| 0.5 mVpp | 2.617 V | 2.384 V | 0.233 Vpp |
| 1.0 mVpp | 2.734 V | 2.268 V | 0.466 Vpp |
| 2.0 mVpp | 2.969 V | 2.037 V | 0.932 Vpp |
| 5.0 mVpp | 3.673 V | 1.342 V | 2.331 Vpp |
| 8.0 mVpp | 4.376 V | 0.647 V | 3.729 Vpp |
| 10.0 mVpp | 4.845 V | 0.184 V | 4.661 Vpp |
| 11.0 mVpp | 5.000 V | 0.0005 V | 4.999 Vpp |
| 12.0 mVpp | 5.000 V | 0.0003 V | 4.999 Vpp |

Within the linear operating region, the gain remains approximately:

```text
Atotal ≈ 466 V/V
```

For an ideal 0–5 V output range, the approximate maximum differential input before reaching the rails can be estimated as:

```text
Vin,max ≈ 5 Vpp / 466
        ≈ 10.7 mVpp
```

The simulation agrees with this estimate:

- 10 mVpp remains approximately linear.
- At 11 mVpp, the output reaches the supply rails and clipping begins.
- Increasing the input to 12 mVpp no longer produces a proportional increase in output amplitude.

The current configuration therefore has an approximate simulated linear differential input range up to about 10 mVpp.

![Input range and output saturation](results/headroom_saturation.png)

---

# 8. Realistic Op-Amp Model Validation

The initial front-end was developed using LTspice `UniversalOpamp2` models.

To evaluate whether the design remains valid with a more realistic device model, all four op-amps were replaced by LT1679 macromodels while keeping the circuit topology and component values unchanged.

The comparison used:

```text
Differential input = 1 mVpp
Frequency = 10 Hz
Measurement interval = 4 s to 5 s
```

The later measurement interval was selected to reduce the influence of the initial filter transient.

## Generic vs. LT1679 Comparison

| Parameter | UniversalOpamp2 | LT1679 |
|---|---:|---:|
| Output maximum | 2.732156 V | 2.732267 V |
| Output minimum | 2.267668 V | 2.267684 V |
| Output amplitude | 0.464488 Vpp | 0.464582 Vpp |
| Output average | 2.500000 V | 2.500032 V |
| INA output average | 2.500000 V | 2.500004 V |

The corresponding overall gains were:

```text
UniversalOpamp2 ≈ 464.49 V/V
LT1679          ≈ 464.58 V/V
```

The difference is approximately:

```text
0.02 %
```

At 10 Hz, replacing the generic op-amp models with LT1679 macromodels therefore produces almost no change in the simulated small-signal gain.

The LT1679-based instrumentation amplifier also remains closely centered around the 2.5 V reference:

```text
INA average offset from VREF ≈ 4 µV
Final output average offset from VREF ≈ 32 µV
```

These results indicate that the expected low-frequency gain and bias point are preserved when the generic models are replaced by LT1679 macromodels.

---

# 9. Real ECG Waveform Validation

As a final system-level test, the front-end was evaluated using a 10-second ECG segment from MIT-BIH Arrhythmia Database Record 100.

The same record is also used in the complementary digital ECG-processing project.

The ECG waveform was exported at:

```text
Sampling frequency = 360 Hz
Duration = 10 s
```

The DC component of the selected ECG segment was removed before export.

The waveform was then imported into LTspice as a piecewise-linear (PWL) voltage source and applied as a differential input centered around the 2.5 V common-mode voltage.

The differential input was generated as:

```text
Vin+ = VCM + ECG/2
Vin- = VCM - ECG/2
```

so that:

```text
Vin+ - Vin- = ECG
```

## Measured ECG Input and Output

Measurements from 1 s to 10 s produced:

| Parameter | Value |
|---|---:|
| ECG input maximum | +1.253 mV |
| ECG input minimum | -0.267 mV |
| ECG input amplitude | 1.520 mVpp |
| AFE output maximum | 2.617 V |
| AFE output minimum | 1.966 V |
| AFE output amplitude | 0.651 Vpp |

The conditioned output remains well inside the 0–5 V supply range.

No output clipping was observed.

The effective peak-to-peak input/output ratio for this ECG segment is:

```text
0.650936 Vpp / 0.00151968 Vpp ≈ 428 V/V
```

This value is lower than the approximately 465 V/V gain measured with a 10 Hz sinusoidal test signal.

This is expected because the ECG contains a broad range of frequency components that are affected differently by the front-end's band-pass response.

Therefore, the ECG peak-to-peak ratio should not be interpreted as the small-signal gain at a single frequency.

The simulation preserves the principal ECG morphology and timing, including the QRS complexes, while conditioning the waveform according to the analog front-end bandwidth.

Because of the polarity selected in the difference-amplifier stage, the final output waveform is inverted relative to the defined differential ECG input.

---

# 10. LTspice Measurements

Representative LTspice measurements used throughout the project include:

## Common-Mode Rejection

```spice
.meas tran VinCMpp PP V(VCM) FROM 0.2 TO 1
.meas tran VoutCMpp PP V(out) FROM 0.2 TO 1
.meas tran Acm PARAM VoutCMpp/VinCMpp
```

## Differential Gain

```spice
.meas tran VinDiffPP PP V(in_plus,in_minus) FROM 0.2 TO 1
.meas tran VoutDiffPP PP V(out) FROM 0.2 TO 1
.meas tran Ad PARAM VoutDiffPP/VinDiffPP
```

## High-Pass Cutoff

```spice
.meas ac HP_FC WHEN mag(V(hp_out)/V(hp_in))=0.70710678 CROSS=1
```

## Complete Band-Pass Response

```spice
.meas ac BP_MAX MAX mag(V(lp_out)/V(bp_in))
.meas ac BP_FPEAK WHEN mag(V(lp_out)/V(bp_in))=BP_MAX
.meas ac BP_FL WHEN mag(V(lp_out)/V(bp_in))=0.669 CROSS=1
.meas ac BP_FH WHEN mag(V(lp_out)/V(bp_in))=0.669 CROSS=2
```

## Output Headroom

```spice
.meas tran VoutMax MAX V(afe_out) FROM 0.5 TO 1
.meas tran VoutMin MIN V(afe_out) FROM 0.5 TO 1
.meas tran VoutPP PP V(afe_out) FROM 0.5 TO 1
```

## Real ECG Validation

```spice
.meas tran ECGinMax MAX V(in_plus,in_minus) FROM 1 TO 10
.meas tran ECGinMin MIN V(in_plus,in_minus) FROM 1 TO 10
.meas tran ECGinPP PP V(in_plus,in_minus) FROM 1 TO 10

.meas tran ECGoutMax MAX V(afe_out) FROM 1 TO 10
.meas tran ECGoutMin MIN V(afe_out) FROM 1 TO 10
.meas tran ECGoutPP PP V(afe_out) FROM 1 TO 10
```

---

# 11. Python Analysis

Python is used to generate test data and visualize selected simulation results.

The current analysis includes:

- CMRR versus resistor mismatch,
- common-mode gain versus resistor mismatch,
- input amplitude versus output amplitude,
- output saturation visualization,
- export of a real ECG waveform to an LTspice-compatible PWL file.

Main Python libraries:

- NumPy
- Matplotlib
- WFDB

---

# Repository Structure

```text
ecg-analog-front-end/
├── docs/
│   └── design_requirements.md
│
├── ltspice/
│   ├── inputs/
│   │   └── ecg_record100_10s.txt
│   │
│   ├── ina_common_mode_ideal.asc
│   ├── ina_common_mode_mismatch_1pct.asc
│   ├── ina_common_mode_mismatch_sweep.asc
│   ├── ina_differential_gain_sweep.asc
│   ├── ecg_front_end_highpass.asc
│   ├── ecg_front_end_highpass_ac.asc
│   ├── ecg_front_end_bandpass.asc
│   ├── ecg_front_end_bandpass_ac.asc
│   ├── ecg_front_end_complete.asc
│   ├── ecg_front_end_headroom_sweep.asc
│   ├── ecg_front_end_real_opamp.asc
│   └── ecg_front_end_ecg_input.asc
│
├── python/
│   ├── plot_cmrr_results.py
│   ├── plot_headroom_results.py
│   └── export_ecg_to_ltspice.py
│
├── results/
│   ├── cmrr_vs_resistor_mismatch.png
│   ├── common_mode_gain_vs_resistor_mismatch.png
│   └── headroom_saturation.png
│
└── README.md
```

File names may vary slightly depending on the final repository organization.

---

# Key Results

The main results of the project are:

- A three-op-amp instrumentation-amplifier stage with approximately 5 V/V differential gain was designed and simulated.
- The high-pass stage has a simulated cutoff of approximately 0.482 Hz.
- The complete passive band-pass network has simulated cutoff frequencies of approximately 0.452 Hz and 43.57 Hz.
- Resistor mismatch in the difference amplifier strongly affects common-mode rejection.
- CMRR decreases from approximately 80 dB at 0.1 % mismatch to approximately 54 dB at 2 % mismatch.
- The complete front-end provides approximately 465 V/V gain at 10 Hz.
- The circuit remains approximately linear up to a 10 mVpp differential sinusoidal input.
- Output clipping begins between 10 and 11 mVpp for the current 0–5 V supply configuration.
- Replacing `UniversalOpamp2` with LT1679 macromodels changes the simulated 10 Hz gain by only about 0.02 %.
- A real MIT-BIH ECG waveform was successfully passed through the complete LT1679-based front-end.
- A 1.520 mVpp ECG segment produced approximately 0.651 Vpp at the final output without clipping.
- The real ECG test preserved the main ECG timing and morphology while applying the intended analog band-limiting and amplification.

---

# Tools

- LTspice
- Python
- NumPy
- Matplotlib
- WFDB
- Visual Studio Code
- Git
- GitHub

---

# Engineering Scope and Limitations

This project is intended as an engineering simulation and portfolio project rather than a clinically validated ECG acquisition system.

Important limitations include:

- The design has not yet been built or validated with physical hardware.
- Real electrode impedance and electrode imbalance are not modeled in detail.
- A driven-right-leg circuit is not included.
- Power-supply noise and PCB/layout effects are not modeled.
- The passive high-pass and low-pass stages interact because they are cascaded without buffering.
- The LT1679 simulations rely on macromodel behavior rather than measurements from a physical device.
- The design has not been validated according to medical-device safety or performance standards.
- The system is not intended for diagnosis, patient monitoring, or clinical decision-making.

---

# Possible Future Work

Potential extensions include:

1. Build the analog front-end on a breadboard or PCB.
2. Compare simulated and measured gain and frequency response.
3. Measure real output noise and DC offset.
4. Model electrode-source impedance and imbalance.
5. Investigate a driven-right-leg circuit.
6. Interface the AFE with an ADC or microcontroller.
7. Connect the measured analog output to the digital ECG-processing pipeline.

For the current portfolio scope, the simulation work is considered complete.

---

# Related Project

A complementary digital ECG-processing project is available here:

https://github.com/vhancajimal/ecg-signal-processing

That project includes:

- MIT-BIH ECG data,
- digital band-pass filtering,
- R-peak detection,
- RR-interval estimation,
- heart-rate estimation,
- validation against reference annotations.

Together, both projects represent a simplified end-to-end ECG workflow:

```text
ECG source / electrodes
        |
        v
Analog front-end
        |
        v
Conditioned analog ECG
        |
        v
ADC / sampled ECG
        |
        v
Digital signal processing
        |
        v
R-peak detection
        |
        v
RR intervals / heart rate
```

---

# Author

Victor Hugo Ancajima Lozano  
B.Sc. Biomedical Engineering  
TU Ilmenau

GitHub:

https://github.com/vhancajimal

---

# Disclaimer

This project is intended for educational, engineering-development, and portfolio purposes only.

It is not a medical device and must not be used for diagnosis, patient monitoring, treatment decisions, or other clinical applications.
