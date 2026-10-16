"""Receiver sensitivity calculations and configuration comparisons."""
import math

BOLTZMANN_CONSTANT_J_K = 1.380649e-23


def watts_to_dbm(power_watts: float) -> float:
    if power_watts <= 0:
        raise ValueError("Power must be greater than zero.")
    return 10 * math.log10(power_watts / 1e-3)


def calculate_noise_density_dbm_hz(temperature_k: float = 290.0) -> float:
    if temperature_k <= 0:
        raise ValueError("Temperature must be greater than zero kelvin.")
    return watts_to_dbm(BOLTZMANN_CONSTANT_J_K * temperature_k)


def calculate_thermal_noise_dbm(bandwidth_hz: float, temperature_k: float = 290.0) -> float:
    if bandwidth_hz <= 0:
        raise ValueError("Bandwidth must be greater than zero.")
    return calculate_noise_density_dbm_hz(temperature_k) + 10 * math.log10(bandwidth_hz)


def calculate_receiver_sensitivity_dbm(
    bandwidth_hz: float,
    noise_figure_db: float,
    required_snr_db: float,
    implementation_margin_db: float = 0.0,
    temperature_k: float = 290.0,
) -> float:
    return (calculate_thermal_noise_dbm(bandwidth_hz, temperature_k)
            + noise_figure_db + required_snr_db + implementation_margin_db)


RECEIVER_CONFIGURATIONS = [
    {"name": "Narrowband Receiver", "bandwidth_hz": 25_000, "noise_figure_db": 5.0, "required_snr_db": 10.0, "implementation_margin_db": 2.0, "temperature_k": 290.0},
    {"name": "Wideband Receiver", "bandwidth_hz": 200_000, "noise_figure_db": 4.5, "required_snr_db": 12.0, "implementation_margin_db": 3.0, "temperature_k": 290.0},
    {"name": "Low-Noise Receiver", "bandwidth_hz": 100_000, "noise_figure_db": 2.5, "required_snr_db": 9.0, "implementation_margin_db": 2.0, "temperature_k": 290.0},
    {"name": "Satellite Receiver", "bandwidth_hz": 1_000_000, "noise_figure_db": 2.0, "required_snr_db": 6.0, "implementation_margin_db": 2.0, "temperature_k": 290.0},
]


def evaluate_receivers(configurations=RECEIVER_CONFIGURATIONS, received_signal_dbm=-100.0, minimum_required_margin_db=3.0):
    results = []
    for receiver in configurations:
        sensitivity_dbm = calculate_receiver_sensitivity_dbm(
            bandwidth_hz=receiver["bandwidth_hz"],
            noise_figure_db=receiver["noise_figure_db"],
            required_snr_db=receiver["required_snr_db"],
            implementation_margin_db=receiver["implementation_margin_db"],
            temperature_k=receiver["temperature_k"],
        )
        margin_db = received_signal_dbm - sensitivity_dbm
        results.append({"name": receiver["name"], "sensitivity_dbm": sensitivity_dbm,
                        "margin_db": margin_db, "result": "PASS" if margin_db >= minimum_required_margin_db else "FAIL"})
    return results


def main():
    results = evaluate_receivers()
    print("Receiver Configuration Comparison")
    print("=" * 78)
    for result in results:
        print(f'{result["name"]:24} Sensitivity: {result["sensitivity_dbm"]:8.2f} dBm  '
              f'Margin: {result["margin_db"]:6.2f} dB  {result["result"]}')
    print("\nSensitivity Ranking (best to worst)")
    for rank, result in enumerate(sorted(results, key=lambda item: item["sensitivity_dbm"]), start=1):
        print(f'{rank}. {result["name"]}: {result["sensitivity_dbm"]:.2f} dBm')


if __name__ == "__main__":
    main()
