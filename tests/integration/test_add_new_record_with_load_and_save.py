import os
import sys
import unittest
from contextlib import suppress

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, QTime

from KissXPLog import adif
from KissXPLog.adif import parse_adif_for_data
from KissXPLog.file_operations import generic_save_data_to_file, write_file_as_json
from KissXPLog.kiss_xp_log import read_data_from_json_file, MainWindow


class TestJsonFileHandling(unittest.TestCase):
    app = QtWidgets.QApplication(sys.argv)

    def setUp(self):
        self.window = MainWindow()
        self.json_outputfile_name = "testfile.json"
        self.json_outputfile_name2 = "testfile2.json"
        self.adif_outputfile_name = "testfile.adi"
        self.adif_outputfile_name2 = "testfile2.adi"

        self.data_to_write = [
            {"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"},
            {"CALL": "BBB", "QSO_DATE": "000000", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"},
            {"CALL": "CCC", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"}]
        self.json_expect = [
            {"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"},
            {"CALL": "BBB", "QSO_DATE": "000000", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"},
            {"CALL": "CCC", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"},
            {"CALL": "DDD", "QSO_DATE": "20220104", "TIME_ON": "113653", "MODE": "FT8", "RST_SENT": "15",
             "RST_RCVD": "10", "FREQ": "182500"}]

        # Same as above but with Frequency..
        self.adi_expect = [
            {"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28", "FREQ": "7.0"},
            {"CALL": "BBB", "QSO_DATE": "000000", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28", "FREQ": "7.0"},
            {"CALL": "CCC", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28", "FREQ": "7.0"},
            {"CALL": "DDD", "QSO_DATE": "20220104", "TIME_ON": "113653", "MODE": "FT8", "RST_SENT": "15",
             "RST_RCVD": "10", "FREQ": "182500"}]

    def tearDown(self):
        with suppress(OSError):
            os.remove(self.json_outputfile_name)
            os.remove(self.json_outputfile_name2)
            os.remove(self.adif_outputfile_name)
            os.remove(self.adif_outputfile_name2)

    def add_some_new_data_to_table(self):
        self.window.ui.le_call.setText("DDD")
        self.window.ui.dateEdit.setDate(QDate.fromString("20220104", "yyyyMMdd"))
        self.window.ui.timeEdit.setTime(QTime.fromString("113653", "HHmmss"))
        self.window.ui.le_freq.setText("182500")
        self.window.ui.cb_mode.setCurrentIndex(self.window.ui.cb_mode.findText("FT8"))
        self.window.ui.le_rst_sent.setText("15")
        self.window.ui.le_rst_rcvd.setText("10")

    def test_add_new_record_with_json_export(self):
        # Create JSON for the test:
        write_file_as_json(self.json_outputfile_name, self.data_to_write)

        # Load File in Table
        self.window.generic_load_file_to_table(self.json_outputfile_name)

        # Fill Input Form
        self.add_some_new_data_to_table()

        # Save InputForm
        self.window.save_new_log_entry()

        # Save Table to file
        generic_save_data_to_file(self.json_outputfile_name2, self.window.model.get_data_from_table())

        # Read File in for check
        result = read_data_from_json_file(self.json_outputfile_name2)

        self.assertEqual(self.json_expect, result)

    def test_add_new_record_with_adif_export(self):
        # Write input File
        adif.export_to_adif(self.adif_outputfile_name, self.data_to_write, self.window.custom_fields_list)

        # Load File in Table
        self.window.generic_load_file_to_table(self.adif_outputfile_name)

        # Fill Input Form
        self.add_some_new_data_to_table()

        # Save InputForm
        self.window.save_new_log_entry()

        # Save to File
        generic_save_data_to_file(self.adif_outputfile_name2, self.window.model.get_data_from_table(),
                                  self.window.custom_fields_list)

        result = parse_adif_for_data(self.adif_outputfile_name2)

        self.assertEqual(self.adi_expect, result)
