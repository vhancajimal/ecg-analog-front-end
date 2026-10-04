import numpy as np
import matplotlib.pyplot as plt

mismatch_percent = np.array([0.1, 0.5, 1.0, 2.0])

Ad = np.array([
    5.00190657769,
    5.01668255481,
    5.03551000953,
    5.07268827455
])

Acm = np.array([
    0.000501871587631,
    0.00250101327993,
    0.00500083446582,
    0.0100016689316
])

cmrr_db = 20 * np.log10(np.abs(Ad / Acm))

print("Mismatch (%) | Ad | Acm | CMRR (dB)")
print("--------------------------------------")

for mismatch, ad, acm, cmrr in zip(
    mismatch_percent, Ad, Acm, cmrr_db
):
    print(
        f"{mismatch:10.1f} | "
        f"{ad:.6f} | "
        f"{acm:.8f} | "
        f"{cmrr:.2f}"
    )

plt.figure(figsize=(7, 4.5))

plt.plot(
    mismatch_percent,
    cmrr_db,
    marker="o"
)
plt.ylim(52, 82)
plt.xlim(0, 2.1)
for x, y in zip(mismatch_percent, cmrr_db):
    plt.annotate(
        f"{y:.1f} dB",
        (x, y),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center"
    )
plt.xlabel("Resistor mismatch (%)")
plt.ylabel("CMRR (dB)")
plt.title("Effect of Resistor Mismatch on CMRR")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "../results/cmrr_vs_resistor_mismatch.png",
    dpi=300
)

plt.show()

plt.figure(figsize=(7, 4.5))

plt.plot(
    mismatch_percent,
    Acm,
    marker="o"
)

for x, y in zip(mismatch_percent, Acm):
    plt.annotate(
        f"{y:.4f}",
        (x, y),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center"
    )

plt.xlabel("Resistor mismatch (%)")
plt.ylabel("Common-mode gain")
plt.title("Effect of Resistor Mismatch on Common-Mode Gain")

plt.xlim(0, 2.1)

plt.grid(True)
plt.tight_layout()

plt.savefig(
    "../results/common_mode_gain_vs_resistor_mismatch.png",
    dpi=300
)

plt.show()