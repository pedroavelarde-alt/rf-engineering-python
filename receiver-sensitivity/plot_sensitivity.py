"""Plot receiver sensitivity versus bandwidth for several noise figures."""
import numpy as np
import matplotlib.pyplot as plt
from receiver_sensitivity import calculate_receiver_sensitivity_dbm


def main():
    bandwidth_hz = np.logspace(3, 6, 100)
    required_snr_db = 10.0
    implementation_margin_db = 2.0
    plt.figure(figsize=(9, 5))
    for noise_figure_db in [2.0, 5.0, 8.0]:
        sensitivity_dbm = [
            calculate_receiver_sensitivity_dbm(float(b), noise_figure_db, required_snr_db, implementation_margin_db)
            for b in bandwidth_hz
        ]
        plt.semilogx(bandwidth_hz, sensitivity_dbm, linewidth=2, label=f"NF = {noise_figure_db:g} dB")
    plt.xlabel("Receiver Bandwidth (Hz)")
    plt.ylabel("Receiver Sensitivity (dBm)")
    plt.title("Receiver Sensitivity vs. Bandwidth and Noise Figure")
    plt.grid(True, which="both", linestyle="--")
    plt.legend()
    plt.tight_layout()
    plt.savefig("receiver_sensitivity_plot.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
