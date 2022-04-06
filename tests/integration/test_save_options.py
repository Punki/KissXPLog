from unittest import TestCase
from unittest.mock import patch

from PyQt5.QtWidgets import QApplication

from KissXPLog import MainWindow


class TestSaveOptions(TestCase):
    app = QApplication([])

    def setUp(self):
        self.window = MainWindow()
        self.window.ui.le_call.setText("HB9")
        self.window.new_dxcc_lookup_thread()
        self.window.ui.cb_mode.setCurrentIndex(self.window.ui.cb_mode.findText("CW"))
        self.window.ui.cb_band.setCurrentIndex(self.window.ui.cb_band.findText("80m"))
        self.window.ui.cbo_sent_options.setCurrentIndex(self.window.ui.cbo_sent_options.findText("Yes"))
        self.window.save_or_edit_handler()

    @patch('KissXPLog.kiss_xp_log.QMessageBox')
    def test_unsaved_changes_dialog(self, mock):
        self.assertTrue(self.window._do_we_have_unsaved_changes)
        self.window.close()
        mock.question.assert_called_once()


