from unittest import TestCase
from unittest.mock import patch

import keyboard
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QDialogButtonBox, QDialog

from KissXPLog import MainWindow, UserConfig
from KissXPLog.dialog.config_dialog import ConfigDialog
from KissXPLog.dialog.filter_dialog import FilterDialog


class TestShowUserSettingsInConfigDialog(TestCase):
    app = QApplication([])

    def setUp(self):
        self.window = MainWindow()
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

    def test_autosave(self):
        self.window.autosave = True
        self.window.cdw.load_config()
        self.assertEqual(True, self.window.cdw.ui2.cb_autosave.isChecked())

    def test_autosave_intervall(self):
        self.window.autosave_interval = 42
        self.window.cdw.load_config()
        self.assertEqual(42, self.window.cdw.ui2.cb_autosave_interval.value())

    # def test_custom_bands(self):
    #     self.window.bands = {'': [0, 0], '40m': [7.0, 7.3], '20m': [14.0, 14.35]}
    #     self.window.cdw.load_config()
    #     self.window.cdw.show_bands_filter_dialog()
    #     print("test")




