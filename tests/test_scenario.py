"""Ma'lumotnoma qiymatlari bilan konvertatsiya va oyna ssenariylari."""
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from birlik_konvertori.units import CATEGORIES, convert  # noqa: E402


@pytest.mark.parametrize("cat,v,src,dst,ref", [
    ("length", 1, "mi", "km", 1.609344),
    ("length", 12, "in", "ft", 1.0),
    ("area", 1, "ha", "sotix", 100),
    ("area", 1, "acre", "m2", 4046.8564224),
    ("volume", 1, "gal", "l", 3.785411784),
    ("mass", 1, "t", "c", 10),
    ("mass", 1, "lb", "oz", 16),
    ("pressure", 1, "atm", "mmhg", 760),
    ("pressure", 1, "kgfcm2", "mpa", 0.0980665),
    ("pressure", 1, "psi", "kpa", 6.894757293),
    ("force", 1, "tf", "kn", 9.80665),
    ("speed", 100, "kmh", "ms", 27.7777778),
    ("speed", 1, "kn", "kmh", 1.852),
    ("angle", 3.14159265358979, "rad", "deg", 180),
    ("angle", 100, "grad", "deg", 90),
    ("angle", 45, "deg", "pct", 100),
    ("angle", 100, "pct", "deg", 45),
    ("angle", 8, "pct", "pct", 8),
    ("temperature", 100, "c", "f", 212),
    ("temperature", -40, "f", "c", -40),
    ("temperature", 0, "k", "c", -273.15),
    ("energy", 1, "kwh", "kcal", 859.845228),
    ("data", 1, "gb", "mb", 1024),
    ("density", 2.4, "tm3", "kgm3", 2400),
])
def test_reference_values(cat, v, src, dst, ref):
    assert convert(cat, v, src, dst) == pytest.approx(ref, rel=1e-6, abs=1e-9)


@pytest.mark.parametrize("cat", [c for c in CATEGORIES if c != "angle"])
def test_roundtrip_every_unit(cat):
    units = list(CATEGORIES[cat][1])
    for a in units:
        for b in units:
            assert convert(cat, convert(cat, 123.456, a, b), b, a) == pytest.approx(123.456, rel=1e-9)


@pytest.fixture
def win(tmp_path, monkeypatch):
    monkeypatch.setenv("APPDATA", str(tmp_path / "appdata"))
    from PySide6.QtWidgets import QApplication
    from uzkit import app as appmod, i18n
    from uzkit.settings import Settings
    QApplication.instance() or QApplication([])
    appmod.META = appmod.load_meta()
    sdir = tmp_path / "appdata" / "BahtiyorSoft" / "birlik_ui_test"
    sdir.mkdir(parents=True)
    (sdir / "settings.json").write_text(json.dumps({"precision": "abc", "history": "xyz", "category": 7}),
                                        encoding="utf-8")
    appmod.SETTINGS = Settings("birlik_ui_test")
    i18n.set_language("en")
    from birlik_konvertori import window as wmod
    errors = []
    monkeypatch.setattr(wmod, "error", lambda *a, **k: errors.append(a))
    w = wmod.MainWindow()
    yield w, wmod, tmp_path, errors
    w.close()


def test_ui_convert_and_history(win, monkeypatch):
    w, wmod, tmp, errors = win
    page = [p for p in w.findChildren(wmod.ConverterPage)][0]
    assert page.prec.value() == 6
    assert w.history.list.count() == 0 and not w.history.exp_btn.isEnabled()   # buzilgan tarix e'tiborsiz
    page.cat.setCurrentIndex(page.cat.findData("pressure"))
    page.src.setCurrentIndex(page.src.findData("atm"))
    page.dst.setCurrentIndex(page.dst.findData("mmhg"))
    page.value.setText("1,5")
    assert page.result.text().startswith("1 139.9998")      # 1 atm = 759.9999 mmHg (133.322387 Pa)
    page.value.setText("1e400")
    assert page.result.text() == wmod.tr("invalid_number")
    page._to_history()
    assert w.history.list.count() == 0          # noto'g'ri qiymat tarixga yozilmaydi
    page.value.setText("2")
    page._to_history()
    assert w.history.list.count() == 1
    page._swap()
    assert page.src.currentData() == "mmhg" and page.dst.currentData() == "atm"
    out = tmp / "Тарих o'quv"
    out.mkdir()
    p = str(out / "тарих.csv")
    monkeypatch.setattr(wmod.QFileDialog, "getSaveFileName", lambda *a, **k: (p, ""))
    w.history._export()
    assert "1 519.9997" in open(p, encoding="utf-8-sig").read()
    # fayl band bo'lsa (bu yerda: papka nomi bilan) dastur yiqilmaydi, xabar chiqaradi
    monkeypatch.setattr(wmod.QFileDialog, "getSaveFileName", lambda *a, **k: (str(out), ""))
    w.history._export()
    assert errors
    w.history._clear()
    assert w.history.list.count() == 0 and not w.history.exp_btn.isEnabled()
