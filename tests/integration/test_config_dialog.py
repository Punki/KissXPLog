from unittest import TestCase

from PyQt5.QtWidgets import QApplication

from KissXPLog import MainWindow


class TestShowUserSettingsInConfigDialog(TestCase):
    app = QApplication([])

    def setUp(self):
        self.window = MainWindow(load_user_settings=False)
        self.window.show_config_window()

    def test_station_callsign(self):
        self.window.user_config.user_settings['STATION_CALLSIGN'] = "AAAAA"
        self.window.cdw.load_config()
        self.assertEqual("AAAAA", self.window.cdw.ui2.le_my_call.text())

    def test_cq_zone(self):
        self.window.user_config.user_settings['MY_CQ_ZONE'] = "BBBBB"
        self.window.cdw.load_config()
        self.assertEqual("BBBBB", self.window.cdw.ui2.le_my_cqzone.text())

    def test_itu_zone(self):
        self.window.user_config.user_settings['MY_ITU_ZONE'] = "CCCCC"
        self.window.cdw.load_config()
        self.assertEqual("CCCCC", self.window.cdw.ui2.le_my_ituzone.text())

    def test_log_level_critical(self):
        self.window.user_config.user_settings['LogLevel'] = "CRITICAL"
        self.window.cdw.load_config()
        self.assertEqual("CRITICAL", self.window.cdw.ui2.cb_loglevel.currentText())

    def test_autosave(self):
        self.window.autosave = True
        self.window.cdw.load_config()
        self.assertEqual(True, self.window.cdw.ui2.cb_autosave.isChecked())

    def test_autosave_intervall(self):
        self.window.autosave_interval = 42
        self.window.cdw.load_config()
        self.assertEqual(42, self.window.cdw.ui2.cb_autosave_interval.value())
