from sources.distance_entre_mots import CalculDistanceMots
import pytest

def test_CalculDistanceMots():
    assert CalculDistanceMots("avec", "abec") == 1
    assert CalculDistanceMots("avec", "avec") == 0
    assert CalculDistanceMots("", "") == 0
    assert CalculDistanceMots("", "avec") == 4
    assert CalculDistanceMots("aevc", "avec") == 1
    assert CalculDistanceMots("aec", "avec") == 1