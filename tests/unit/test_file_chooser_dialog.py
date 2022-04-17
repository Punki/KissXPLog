import os
from unittest import TestCase
from unittest.mock import MagicMock

import keyboard as keyboard
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from KissXPLog.kiss_xp_log import MainWindow
from KissXPLog.config import *


class FileChooserTests(TestCase):

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Check if Saving is working with Choose Dialog
    def test_int_json_save_file_chooser(self):
        import KissXPLog
        app = QApplication([])

        filename = "some_testfile.json"
        expected_path_with_filename = (os.path.join(data_dir, filename)).replace(os.sep, '/')

        QtCore.QTimer.singleShot(1, lambda: keyboard.write(filename))
        QtCore.QTimer.singleShot(10, lambda: keyboard.press('enter'))

        window = MainWindow()
        gsfc = KissXPLog.kiss_xp_log.generic_save_data_to_file = MagicMock()
        window.json_save_file_chooser()

        # Search if inputfile is in the call-list
        self.assertEqual(expected_path_with_filename, str(gsfc.call_args[0][0]))

    # Check if Saving is working with Choose Dialog
    def test_int_adif_save_file_chooser(self):
        import KissXPLog
        app = QApplication([])

        filename = "some_testfile.adi"
        expected_path_with_filename = (os.path.join(data_dir, filename)).replace(os.sep, '/')

        QtCore.QTimer.singleShot(1, lambda: keyboard.write(filename))
        QtCore.QTimer.singleShot(10, lambda: keyboard.press('enter'))

        window = MainWindow()
        gsfc = KissXPLog.kiss_xp_log.generic_save_data_to_file = MagicMock()
        window.adif_save_file_chooser()

        # Search if inputfile is in the call-list
        self.assertEqual(expected_path_with_filename, str(gsfc.call_args[0][0]))
