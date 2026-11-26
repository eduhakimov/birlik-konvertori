import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from birlik_konvertori.units import CATEGORIES, convert, fmt, rebar_mass_per_m


def close(a, b, eps=1e-9):
    return abs(a - b) <= eps * max(1, abs(a), abs(b))


def test_length():
    assert close(convert("length", 1, "m", "mm"), 1000)
    assert close(convert("length", 1, "in", "cm"), 2.54)


def test_area_sotix():
    assert close(convert("area", 1, "ha", "sotix"), 100)


def test_temperature():
    assert close(convert("temperature", 100, "c", "f"), 212)
    assert close(convert("temperature", 0, "c", "k"), 273.15)
    assert close(convert("temperature", 32, "f", "c"), 0)


def test_pressure():
    assert close(convert("pressure", 1, "mpa", "kgfcm2"), 10.197162129779283)


def test_slope():
    assert close(convert("angle", 100, "pct", "deg"), 45)
    assert close(convert("angle", 45, "deg", "pct"), 100)


def test_roundtrip_all():
    for cat, (_, units) in CATEGORIES.items():
        codes = list(units)
        x = 0.5 if cat == "angle" else 12.5   # nishablik faqat (-90°; 90°) oralig'ida qaytariladi
        for a in codes:
            for b in codes:
                v = convert(cat, convert(cat, x, a, b), b, a)
                assert close(v, x, 1e-7), (cat, a, b, v)


def test_rebar():
    assert abs(rebar_mass_per_m(12) - 0.888) < 0.001
    assert abs(rebar_mass_per_m(10) - 0.617) < 0.001


def test_fmt():
    assert fmt(1000.5, 2) == "1 000.5"
    assert fmt(0) == "0"
