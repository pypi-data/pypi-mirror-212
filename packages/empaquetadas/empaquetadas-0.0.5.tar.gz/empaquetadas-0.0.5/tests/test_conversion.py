import empaquetadas
import pytest


def test_change_factor():
    test_data = {"2023-01": 1500, "2023-02": 2000}
    conv = empaquetadas.Converter(test_data)
    assert 1.333333 == pytest.approx(conv.change_factor("2023-01", "2023-02"))
