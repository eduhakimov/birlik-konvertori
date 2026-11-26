"""Asosiy oyna: konvertor, armatura jadvali, tarix."""
import csv
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (QAbstractItemView, QComboBox, QDoubleSpinBox, QFileDialog, QFormLayout,
                               QGridLayout, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QListWidget,
                               QPushButton, QSpinBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from uzkit.i18n import language, register, tr
from uzkit.widgets import Card, header, primary_button
from uzkit.window import BaseMainWindow

from .strings import STRINGS
from .units import (CATEGORIES, REBAR_DIAMETERS, convert, fmt, rebar_area_mm2, rebar_mass_per_m)

register(STRINGS)


def _parse(text: str) -> float:
    return float(text.replace(" ", "").replace(",", "."))


class ConverterPage(QWidget):
    def __init__(self, win):
        super().__init__()
        self.win = win
        lay = QVBoxLayout(self)
        lay.setSpacing(14)
        lay.addWidget(header(tr("conv_title"), tr("conv_sub")))

        top = Card()
        g = QGridLayout()
        g.setHorizontalSpacing(12)
        self.cat = QComboBox()
        for key, (names, _) in CATEGORIES.items():
            self.cat.addItem(names[language()], key)
        self.value = QLineEdit("1")
        self.value.setPlaceholderText("0")
        self.value.setMinimumHeight(34)
        f = self.value.font()
        f.setPointSize(13)
        self.value.setFont(f)
        self.src = QComboBox()
        self.dst = QComboBox()
        self.swap = QPushButton(tr("swap"))
        self.prec = QSpinBox()
        self.prec.setRange(0, 12)
        self.prec.setValue(win.settings.get("precision", 6))
        g.addWidget(QLabel(tr("category")), 0, 0)
        g.addWidget(self.cat, 1, 0)
        g.addWidget(QLabel(tr("value")), 0, 1)
        g.addWidget(self.value, 1, 1)
        g.addWidget(QLabel(tr("precision")), 0, 2)
        g.addWidget(self.prec, 1, 2)
        g.addWidget(QLabel(tr("from_unit")), 2, 0)
        g.addWidget(self.src, 3, 0)
        g.addWidget(self.swap, 3, 1)
        g.addWidget(QLabel(tr("to_unit")), 2, 2)
        g.addWidget(self.dst, 3, 2)
        g.setColumnStretch(0, 2)
        g.setColumnStretch(1, 2)
        g.setColumnStretch(2, 2)
        top.add(g)

        res_row = QHBoxLayout()
        self.result = QLabel("—")
        self.result.setObjectName("Title")
        self.result.setTextInteractionFlags(Qt.TextSelectableByMouse)
        res_row.addWidget(self.result, 1)
        self.copy_btn = QPushButton(tr("copy_result"))
        self.hist_btn = primary_button(tr("save_history"))
        res_row.addWidget(self.copy_btn)
        res_row.addWidget(self.hist_btn)
        top.add(res_row)
        lay.addWidget(top)

        allc = Card(tr("all_units"))
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels([tr("unit"), tr("result")])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        allc.add(self.table)
        lay.addWidget(allc, 1)

        self.cat.currentIndexChanged.connect(self._fill_units)
        for w in (self.src, self.dst):
            w.currentIndexChanged.connect(self.recalc)
        self.value.textChanged.connect(self.recalc)
        self.prec.valueChanged.connect(self._prec_changed)
        self.swap.clicked.connect(self._swap)
        self.copy_btn.clicked.connect(self._copy)
        self.hist_btn.clicked.connect(self._to_history)
        last = win.settings.get("category")
        idx = self.cat.findData(last) if last else 0
        self.cat.setCurrentIndex(max(idx, 0))
        self._fill_units()

    def _fill_units(self):
        key = self.cat.currentData()
        units = CATEGORIES[key][1]
        for box in (self.src, self.dst):
            box.blockSignals(True)
            box.clear()
            for code, (_, names) in units.items():
                box.addItem(names[language()], code)
            box.blockSignals(False)
        self.dst.setCurrentIndex(1 if self.dst.count() > 1 else 0)
        self.win.settings.set("category", key)
        self.recalc()

    def _prec_changed(self, v):
        self.win.settings.set("precision", v)
        self.recalc()

    def _swap(self):
        a, b = self.src.currentIndex(), self.dst.currentIndex()
        self.src.blockSignals(True)
        self.src.setCurrentIndex(b)
        self.src.blockSignals(False)
        self.dst.setCurrentIndex(a)

    def recalc(self):
        key = self.cat.currentData()
        if key is None or self.src.currentData() is None:
            return
        try:
            v = _parse(self.value.text())
        except ValueError:
            self.result.setText(tr("invalid_number"))
            self.table.setRowCount(0)
            return
        p = self.prec.value()
        src = self.src.currentData()
        r = convert(key, v, src, self.dst.currentData())
        self.result.setText(f"{fmt(r, p)}  {self.dst.currentText()}")
        units = CATEGORIES[key][1]
        self.table.setRowCount(len(units))
        for i, (code, (_, names)) in enumerate(units.items()):
            self.table.setItem(i, 0, QTableWidgetItem(names[language()]))
            it = QTableWidgetItem(fmt(convert(key, v, src, code), p))
            it.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(i, 1, it)

    def _copy(self):
        QGuiApplication.clipboard().setText(self.result.text().split("  ")[0])
        self.win.status(tr("copied"))

    def _to_history(self):
        line = f"{self.value.text()} {self.src.currentText()} = {self.result.text()}"
        self.win.history.add(line)


class RebarPage(QWidget):
    def __init__(self, win):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setSpacing(14)
        lay.addWidget(header(tr("rebar_title"), tr("rebar_sub")))
        calc = Card()
        form = QFormLayout()
        self.d = QComboBox()
        for d in REBAR_DIAMETERS:
            self.d.addItem(f"Ø {d}", d)
        self.d.setCurrentIndex(REBAR_DIAMETERS.index(12))
        self.l = QDoubleSpinBox()
        self.l.setRange(0, 1e6)
        self.l.setDecimals(2)
        self.l.setValue(11.7)
        self.n = QSpinBox()
        self.n.setRange(1, 1_000_000)
        self.n.setValue(1)
        form.addRow(tr("diameter"), self.d)
        form.addRow(tr("length_m"), self.l)
        form.addRow(tr("count"), self.n)
        calc.add(form)
        self.out = QLabel()
        self.out.setObjectName("Title")
        calc.add(self.out)
        lay.addWidget(calc)

        ref = Card(tr("ref_table"))
        t = QTableWidget(len(REBAR_DIAMETERS), 3)
        t.setHorizontalHeaderLabels([tr("diameter"), tr("area_mm2"), tr("mass_per_m")])
        t.verticalHeader().setVisible(False)
        t.setEditTriggers(QAbstractItemView.NoEditTriggers)
        t.setAlternatingRowColors(True)
        t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i, d in enumerate(REBAR_DIAMETERS):
            for j, txt in enumerate((f"Ø {d}", f"{rebar_area_mm2(d):.1f}", f"{rebar_mass_per_m(d):.3f}")):
                it = QTableWidgetItem(txt)
                it.setTextAlignment(Qt.AlignCenter)
                t.setItem(i, j, it)
        ref.add(t)
        lay.addWidget(ref, 1)
        for w in (self.d, self.l, self.n):
            sig = w.currentIndexChanged if isinstance(w, QComboBox) else w.valueChanged
            sig.connect(self.recalc)
        self.recalc()

    def recalc(self):
        d = self.d.currentData()
        m = rebar_mass_per_m(d) * self.l.value() * self.n.value()
        self.out.setText(f"{tr('total_mass')}: {fmt(m, 3)} kg  ({fmt(m / 1000, 4)} t)")


class HistoryPage(QWidget):
    def __init__(self, win):
        super().__init__()
        self.win = win
        lay = QVBoxLayout(self)
        lay.addWidget(header(tr("page_history")))
        self.list = QListWidget()
        self.list.setAlternatingRowColors(True)
        lay.addWidget(self.list, 1)
        row = QHBoxLayout()
        row.addStretch(1)
        exp = QPushButton(tr("export_csv"))
        clr = QPushButton(tr("clear"))
        row.addWidget(exp)
        row.addWidget(clr)
        lay.addLayout(row)
        exp.clicked.connect(self._export)
        clr.clicked.connect(self._clear)
        for line in win.settings.get("history", []):
            self.list.addItem(line)

    def add(self, line: str):
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.list.insertItem(0, f"{stamp}   {line}")
        items = [self.list.item(i).text() for i in range(min(self.list.count(), 500))]
        self.win.settings.set("history", items)
        self.win.status(tr("done"))

    def _clear(self):
        self.list.clear()
        self.win.settings.set("history", [])

    def _export(self):
        p, _ = QFileDialog.getSaveFileName(self, tr("export_csv"), "tarix.csv", "CSV (*.csv)")
        if not p:
            return
        with open(p, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            for i in range(self.list.count()):
                w.writerow([self.list.item(i).text()])
        self.win.status(tr("done"))


class MainWindow(BaseMainWindow):
    def __init__(self):
        super().__init__()
        self.history = HistoryPage(self)
        self.add_page(tr("page_convert"), ConverterPage(self))
        self.add_page(tr("page_rebar"), RebarPage(self))
        self.add_page(tr("page_history"), self.history)
