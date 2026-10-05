import numpy as np
import matplotlib.pyplot as plt

# Differential input amplitude from LTspice (mVpp)
vin_mVpp = np.array([
    0.5,
    1.0,
    2.0,
    5.0,
    8.0,
    10.0,
    11.0,
    12.0
])

# Measured final output amplitude from LTspice (Vpp)
vout_Vpp = np.array([
    0.233066,
    0.466125,
    0.932231,
    2.330540,
    3.728852,
    4.661060,
    4.999089,
    4.999388
])

# Overall gain measured in the linear region
gain = 466.1

# Ideal linear response without supply limitation
vin_ideal = np.linspace(0, 12, 200)
vout_ideal = gain * (vin_ideal / 1000)

print("Input (mVpp) | Output (Vpp)")
print("----------------------------")

for vin, vout in zip(vin_mVpp, vout_Vpp):
    print(f"{vin:12.1f} | {vout:.4f}")

# Plot
plt.figure(figsize=(7, 4.5))

plt.plot(
    vin_mVpp,
    vout_Vpp,
    marker="o",
    label="LTspice simulation"
)

plt.plot(
    vin_ideal,
    vout_ideal,
    linestyle="--",
    label="Ideal linear response"
)

plt.axhline(
    5.0,
    linestyle=":",
    label="5 Vpp supply-limited maximum"
)

plt.xlabel("Differential input amplitude (mVpp)")
plt.ylabel("Output amplitude (Vpp)")
plt.title("ECG Front-End Input Range and Output Saturation")

plt.xlim(0, 12.5)
plt.ylim(0, 5.5)

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    "../results/headroom_saturation.png",
    dpi=300
)

plt.show()