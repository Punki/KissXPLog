from unittest import TestCase

from PyQt5.QtWidgets import QApplication

from KissXPLog import MainWindow


class TestGuiStuff(TestCase):
    app = QApplication([])

    def setUp(self):
        self.window = MainWindow()

    def test_lowcase_unit_match_band(self):
        band_low_case = {"BAND": "80m"}
        self.window.fill_values_to_edit_form(band_low_case)
        expect = "80m"
        self.assertEqual(expect, self.window.ui.cb_band.currentText())

    def test_uppercase_unit_match_band(self):
        band_low_case = {"BAND": "40M"}
        self.window.fill_values_to_edit_form(band_low_case)
        expect = "40m"
        self.assertEqual(expect, self.window.ui.cb_band.currentText())
