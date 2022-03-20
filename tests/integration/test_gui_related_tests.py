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


class TestSetFrequencyFromBand(TestCase):
    app = QApplication([])

    def setUp(self):
        self.window = MainWindow()
        self.window.ui.cb_band.setCurrentText("80m")

    def test_freq_not_set(self):
        # Should set the Freq
        self.window.set_frequency_from_band()
        self.assertEqual("3.5", self.window.ui.le_freq.text())

    def test_freq_already_set(self):
        # Frequency allready set >> do nothing..
        self.window.ui.le_freq.setText("666")
        self.window.set_frequency_from_band()
        self.assertEqual("666", self.window.ui.le_freq.text())


class TestSetBandFromFrequency(TestCase):
    app = QApplication([])

    def setUp(self):
        self.window = MainWindow()
        self.window.ui.le_freq.setText("3.5")

    def test_band_not_set(self):
        self.window.set_band_from_frequency()
        self.assertEqual("80m", self.window.ui.cb_band.currentText())

    def test_band_already_set(self):
        # Should do Nothing
        self.window.ui.cb_band.setCurrentText("20m")
        self.window.set_band_from_frequency()
        self.assertEqual("20m", self.window.ui.cb_band.currentText())


class TestAutoEnterDxccInfosFromCallsign(TestCase):
    app = QApplication([])

    # FixMe check for Key Errors!
    def setUp(self):
        self.window = MainWindow()
        self.window.all_dxcc['Country'] = "AAAAAA"
        self.window.all_dxcc['Continent'] = "BBBBBB"
        self.window.all_dxcc['ITUZone'] = "CC"
        self.window.all_dxcc['CQZone'] = "DD"

    def test_country_not_set(self):
        self.window.auto_enter_dxcc_infos_from_callsign()
        self.assertEqual("AAAAAA", self.window.ui.le_country.text())

    def test_country_set_in_gui(self):
        self.window.ui.le_country.setText("ZZZ")
        self.window.auto_enter_dxcc_infos_from_callsign()
        self.assertEqual("ZZZ", self.window.ui.le_country.text())

    def test_continent_not_set(self):
        self.window.auto_enter_dxcc_infos_from_callsign()
        self.assertEqual("BBBBBB", self.window.ui.le_continent.text())

    def test_continent_set_in_gui(self):
        self.window.ui.le_continent.setText("YYY")
        self.window.auto_enter_dxcc_infos_from_callsign()
        self.assertEqual("YYY", self.window.ui.le_continent.text())

    def test_ituzone_not_set(self):
        self.window.auto_enter_dxcc_infos_from_callsign()
        self.assertEqual("CC", self.window.ui.le_itu.text())

    def test_ituzone_set_in_gui(self):
        self.window.ui.le_itu.setText("XXX")
        self.window.auto_enter_dxcc_infos_from_callsign()
        self.assertEqual("XXX", self.window.ui.le_itu.text())

    def test_cqzone_not_set(self):
        self.window.auto_enter_dxcc_infos_from_callsign()
        self.assertEqual("DD", self.window.ui.le_cq.text())

    def test_cqzone_set_in_gui(self):
        self.window.ui.le_cq.setText("WW")
        self.window.auto_enter_dxcc_infos_from_callsign()
        self.assertEqual("WW", self.window.ui.le_cq.text())

    def test_none_values(self):
        self.window.all_dxcc = {}
        self.window.auto_enter_dxcc_infos_from_callsign()
        self.assertEqual("", self.window.ui.le_country.text())
        self.assertEqual("", self.window.ui.le_continent.text())
        self.assertEqual("", self.window.ui.le_itu.text())
        self.assertEqual("", self.window.ui.le_cq.text())
