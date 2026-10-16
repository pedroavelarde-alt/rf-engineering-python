import pytest
import math

from receiver_sensitivity import (
    calculate_thermal_noise_dbm,
    calculate_receiver_sensitivity_dbm,
)


def test_thermal_noise():
    noise = calculate_thermal_noise_dbm(
        bandwidth_hz=100_000,
        temperature_k=290.0,
    )

    assert noise == pytest.approx(-123.98, abs=0.05)


def test_receiver_sensitivity():
    sensitivity = calculate_receiver_sensitivity_dbm(
        bandwidth_hz=100_000,
        noise_figure_db=5.0,
        required_snr_db=10.0,
        implementation_margin_db=2.0,
        temperature_k=290.0,
    )

    assert sensitivity == pytest.approx(-106.98, abs=0.05)


def test_invalid_bandwidth():
    with pytest.raises(ValueError):
        calculate_thermal_noise_dbm(
            bandwidth_hz=0,
            temperature_k=290.0,
        )

def test_noise_figure_impact():

    sensitivity_nf5 = calculate_receiver_sensitivity_dbm(
        bandwidth_hz=100_000,
        noise_figure_db=5.0,
        required_snr_db=10.0,
        implementation_margin_db=2.0,
        temperature_k=290.0,
    )

    sensitivity_nf8 = calculate_receiver_sensitivity_dbm(
        bandwidth_hz=100_000,
        noise_figure_db=8.0,
        required_snr_db=10.0,
        implementation_margin_db=2.0,
        temperature_k=290.0,
    )

    sensitivity_difference = sensitivity_nf8 - sensitivity_nf5

    assert sensitivity_difference == pytest.approx(3.0, abs=0.01)

def test_bandwidth_impact():

    noise_100khz = calculate_thermal_noise_dbm(
        bandwidth_hz=100_000,
        temperature_k=290.0,
    )

    noise_1mhz = calculate_thermal_noise_dbm(
        bandwidth_hz=1_000_000,
        temperature_k=290.0,
    )

    noise_difference = noise_1mhz - noise_100khz

    expected_difference = 10 * math.log10(10)

    assert noise_difference == pytest.approx(
        expected_difference,
        abs=0.01
    )