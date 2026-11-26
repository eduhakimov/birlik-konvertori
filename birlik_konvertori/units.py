"""O'lchov birliklari va konvertatsiya mantig'i (interfeysdan mustaqil, test qilinadi).

Har bir kategoriya: birlik kodi -> (asosiy birlikka ko'paytuvchi, nomlar{uz,ru,en})
Harorat alohida (chiziqli emas, siljish bor).
"""
from typing import Dict, Tuple

N = Dict[str, str]


def _n(uz: str, ru: str, en: str) -> N:
    return {"uz": uz, "ru": ru, "en": en}


CATEGORIES: Dict[str, Tuple[N, Dict[str, Tuple[float, N]]]] = {
    "length": (_n("Uzunlik", "Длина", "Length"), {
        "mm": (0.001, _n("millimetr (mm)", "миллиметр (мм)", "millimetre (mm)")),
        "cm": (0.01, _n("santimetr (sm)", "сантиметр (см)", "centimetre (cm)")),
        "dm": (0.1, _n("detsimetr (dm)", "дециметр (дм)", "decimetre (dm)")),
        "m": (1.0, _n("metr (m)", "метр (м)", "metre (m)")),
        "km": (1000.0, _n("kilometr (km)", "километр (км)", "kilometre (km)")),
        "in": (0.0254, _n("dyuym (in)", "дюйм (in)", "inch (in)")),
        "ft": (0.3048, _n("fut (ft)", "фут (ft)", "foot (ft)")),
        "yd": (0.9144, _n("yard (yd)", "ярд (yd)", "yard (yd)")),
        "mi": (1609.344, _n("mil (mi)", "миля (mi)", "mile (mi)")),
    }),
    "area": (_n("Maydon", "Площадь", "Area"), {
        "mm2": (1e-6, _n("mm²", "мм²", "mm²")),
        "cm2": (1e-4, _n("sm²", "см²", "cm²")),
        "m2": (1.0, _n("m²", "м²", "m²")),
        "sotix": (100.0, _n("sotix (100 m²)", "сотка (100 м²)", "sotix / are (100 m²)")),
        "ha": (10000.0, _n("gektar (ga)", "гектар (га)", "hectare (ha)")),
        "km2": (1e6, _n("km²", "км²", "km²")),
        "ft2": (0.09290304, _n("ft²", "ft²", "ft²")),
        "acre": (4046.8564224, _n("akr", "акр", "acre")),
    }),
    "volume": (_n("Hajm", "Объём", "Volume"), {
        "ml": (1e-6, _n("millilitr (ml)", "миллилитр (мл)", "millilitre (ml)")),
        "l": (1e-3, _n("litr (l)", "литр (л)", "litre (l)")),
        "cm3": (1e-6, _n("sm³", "см³", "cm³")),
        "dm3": (1e-3, _n("dm³", "дм³", "dm³")),
        "m3": (1.0, _n("m³", "м³", "m³")),
        "gal": (0.003785411784, _n("gallon (AQSh)", "галлон (США)", "gallon (US)")),
        "ft3": (0.028316846592, _n("ft³", "ft³", "ft³")),
    }),
    "mass": (_n("Massa", "Масса", "Mass"), {
        "g": (0.001, _n("gramm (g)", "грамм (г)", "gram (g)")),
        "kg": (1.0, _n("kilogramm (kg)", "килограмм (кг)", "kilogram (kg)")),
        "c": (100.0, _n("sentner (s)", "центнер (ц)", "centner (q)")),
        "t": (1000.0, _n("tonna (t)", "тонна (т)", "tonne (t)")),
        "lb": (0.45359237, _n("funt (lb)", "фунт (lb)", "pound (lb)")),
        "oz": (0.028349523125, _n("unsiya (oz)", "унция (oz)", "ounce (oz)")),
    }),
    "density": (_n("Zichlik", "Плотность", "Density"), {
        "kgm3": (1.0, _n("kg/m³", "кг/м³", "kg/m³")),
        "tm3": (1000.0, _n("t/m³", "т/м³", "t/m³")),
        "gcm3": (1000.0, _n("g/sm³", "г/см³", "g/cm³")),
        "kgl": (1000.0, _n("kg/l", "кг/л", "kg/l")),
    }),
    "pressure": (_n("Bosim / kuchlanish", "Давление / напряжение", "Pressure / stress"), {
        "pa": (1.0, _n("paskal (Pa)", "паскаль (Па)", "pascal (Pa)")),
        "kpa": (1e3, _n("kPa", "кПа", "kPa")),
        "mpa": (1e6, _n("MPa (N/mm²)", "МПа (Н/мм²)", "MPa (N/mm²)")),
        "bar": (1e5, _n("bar", "бар", "bar")),
        "atm": (101325.0, _n("atmosfera (atm)", "атмосфера (атм)", "atmosphere (atm)")),
        "kgfcm2": (98066.5, _n("kgk/sm²", "кгс/см²", "kgf/cm²")),
        "tfm2": (9806.65, _n("tk/m²", "тс/м²", "tf/m²")),
        "psi": (6894.757293168, _n("psi", "psi", "psi")),
        "mmhg": (133.322387415, _n("mm sim. ust.", "мм рт. ст.", "mmHg")),
    }),
    "force": (_n("Kuch", "Сила", "Force"), {
        "n": (1.0, _n("nyuton (N)", "ньютон (Н)", "newton (N)")),
        "kn": (1e3, _n("kilonyuton (kN)", "килоньютон (кН)", "kilonewton (kN)")),
        "mn": (1e6, _n("meganyuton (MN)", "меганьютон (МН)", "meganewton (MN)")),
        "kgf": (9.80665, _n("kilogramm-kuch (kgk)", "килограмм-сила (кгс)", "kilogram-force (kgf)")),
        "tf": (9806.65, _n("tonna-kuch (tk)", "тонна-сила (тс)", "tonne-force (tf)")),
        "lbf": (4.4482216152605, _n("funt-kuch (lbf)", "фунт-сила (lbf)", "pound-force (lbf)")),
    }),
    "speed": (_n("Tezlik", "Скорость", "Speed"), {
        "ms": (1.0, _n("m/s", "м/с", "m/s")),
        "kmh": (1 / 3.6, _n("km/soat", "км/ч", "km/h")),
        "mph": (0.44704, _n("mil/soat", "миль/ч", "mph")),
        "kn": (1852 / 3600, _n("tugun", "узел", "knot")),
    }),
    "angle": (_n("Burchak", "Угол", "Angle"), {
        "deg": (1.0, _n("gradus (°)", "градус (°)", "degree (°)")),
        "rad": (57.29577951308232, _n("radian", "радиан", "radian")),
        "grad": (0.9, _n("grad (gon)", "град (гон)", "gradian (gon)")),
        "pct": (None, _n("nishablik (%)", "уклон (%)", "slope (%)")),
    }),
    "temperature": (_n("Harorat", "Температура", "Temperature"), {
        "c": (None, _n("Selsiy (°C)", "Цельсий (°C)", "Celsius (°C)")),
        "f": (None, _n("Farengeyt (°F)", "Фаренгейт (°F)", "Fahrenheit (°F)")),
        "k": (None, _n("Kelvin (K)", "Кельвин (K)", "Kelvin (K)")),
    }),
    "energy": (_n("Energiya / quvvat", "Энергия / мощность", "Energy / power"), {
        "j": (1.0, _n("joul (J)", "джоуль (Дж)", "joule (J)")),
        "kj": (1e3, _n("kJ", "кДж", "kJ")),
        "kwh": (3.6e6, _n("kVt·soat", "кВт·ч", "kWh")),
        "cal": (4.1868, _n("kaloriya (kal)", "калория (кал)", "calorie (cal)")),
        "kcal": (4186.8, _n("kkal", "ккал", "kcal")),
    }),
    "data": (_n("Ma'lumot hajmi", "Объём данных", "Data size"), {
        "b": (1.0, _n("bayt (B)", "байт (Б)", "byte (B)")),
        "kb": (1024.0, _n("KB", "КБ", "KB")),
        "mb": (1024.0 ** 2, _n("MB", "МБ", "MB")),
        "gb": (1024.0 ** 3, _n("GB", "ГБ", "GB")),
        "tb": (1024.0 ** 4, _n("TB", "ТБ", "TB")),
    }),
}


def _temp_to_c(v: float, u: str) -> float:
    if u == "c":
        return v
    if u == "f":
        return (v - 32) * 5 / 9
    if u == "k":
        return v - 273.15
    raise ValueError(u)


def _c_to_temp(c: float, u: str) -> float:
    if u == "c":
        return c
    if u == "f":
        return c * 9 / 5 + 32
    if u == "k":
        return c + 273.15
    raise ValueError(u)


def convert(category: str, value: float, src: str, dst: str) -> float:
    """value ni src birlikdan dst birlikka o'tkazadi."""
    if category == "temperature":
        return _c_to_temp(_temp_to_c(value, src), dst)
    units = CATEGORIES[category][1]
    if category == "angle" and "pct" in (src, dst):
        import math
        deg = math.degrees(math.atan(value / 100)) if src == "pct" else value * units[src][0]
        if dst == "pct":
            return math.tan(math.radians(deg)) * 100
        return deg / units[dst][0]
    base = value * units[src][0]
    return base / units[dst][0]


# ------------------------------------------------------------------ armatura
REBAR_DIAMETERS = [6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40]
STEEL_DENSITY = 7850.0  # kg/m³


def rebar_mass_per_m(d_mm: float) -> float:
    """Armatura 1 metrining massasi (kg/m): π·d²/4 · 7850."""
    import math
    return math.pi * (d_mm / 1000) ** 2 / 4 * STEEL_DENSITY


def rebar_area_mm2(d_mm: float) -> float:
    import math
    return math.pi * d_mm ** 2 / 4


def fmt(x: float, digits: int = 6) -> str:
    """Chiroyli son ko'rinishi: ortiqcha nollarsiz, katta/kichik sonlar uchun ilmiy yozuv."""
    if x == 0:
        return "0"
    ax = abs(x)
    if ax >= 1e12 or ax < 1e-6:
        return f"{x:.{digits}e}"
    s = f"{x:,.{digits}f}".rstrip("0").rstrip(".")
    return s.replace(",", " ")
