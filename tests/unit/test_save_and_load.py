import json
from unittest import TestCase
from unittest.mock import patch, MagicMock, mock_open

from KissXPLog.kiss_xp_log import MainWindow, read_data_from_json_file
from KissXPLog.file_operations import write_file_as_json, generic_save_data_to_file


class SaveAndLoadToFileTest(TestCase):

    # File extension JSON
    @patch('KissXPLog.kiss_xp_log.read_data_from_json_file')
    def test_load_file_to_table_json(self, mock):
        mc = MagicMock()
        MainWindow.generic_load_file(mc, "someFile.json")
        mock.assert_called_once_with("someFile.json")

    # File extension ADI
    @patch('KissXPLog.kiss_xp_log.parse_adif_for_data')
    def test_generic_load_file_adi(self, mock):
        mc = MagicMock()
        MainWindow.generic_load_file(mc, "someFile.adi")
        mock.assert_called_once_with("someFile.adi")

    # File extension ADI
    @patch('KissXPLog.kiss_xp_log.parse_adif_for_data')
    def test_load_file_to_table_adif(self, mock):
        mc = MagicMock()
        MainWindow.generic_load_file(mc, "someFile.adif")
        mock.assert_called_once_with("someFile.adif")

    # File extension JSON
    @patch('KissXPLog.file_operations.write_file_as_json')
    def test_generic_save_data_to_file_json(self, mock):
        generic_save_data_to_file("someFile.json", "Data")
        mock.assert_called_once_with("someFile.json", "Data")

    # File extension ADI
    @patch('KissXPLog.file_operations.export_to_adif')
    def test_generic_save_data_to_file_adi(self, mock):
        generic_save_data_to_file("someFile.adi", "some_Data", "IgnoreFiles")
        mock.assert_called_once_with("someFile.adi", "some_Data", "IgnoreFiles")

    # File extension ADIF
    @patch('KissXPLog.file_operations.export_to_adif')
    def test_generic_save_data_to_file_adif(self, mock):
        generic_save_data_to_file("someFile.adif", "some_Data", "IgnoreFiles")
        mock.assert_called_once_with("someFile.adif", "some_Data", "IgnoreFiles")

    # Check if the Method gets Called Correctly
    @patch("KissXPLog.file_operations.QFileDialog")
    def test_adif_load_file_chooser(self, mock_my_class):
        my_adi_file = "some_file.adi"

        mc = mock_my_class.return_value
        mc.selectedFiles.return_value = [my_adi_file]

        mock_self = MagicMock()
        MainWindow.adif_load_file_chooser(mock_self)
        mock_self.load_file_to_table.assert_called_once_with(my_adi_file)

    # Check if the Method gets Called Correctly
    @patch("KissXPLog.file_operations.QFileDialog")
    def test_adi_load_file_chooser(self, mock_my_class):
        my_adi_file = "some_file.adif"

        mc = mock_my_class.return_value
        mc.selectedFiles.return_value = [my_adi_file]

        mock_self = MagicMock()
        MainWindow.adif_load_file_chooser(mock_self)
        mock_self.load_file_to_table.assert_called_once_with(my_adi_file)

    # Check if the Method gets Called Correctly
    @patch("KissXPLog.file_operations.QFileDialog")
    def test_json_load_file_chooser(self, mock_my_class):
        my_adi_file = "some_file.json"
        mc = mock_my_class.return_value
        mc.selectedFiles.return_value = [my_adi_file]

        mock_self = MagicMock()
        MainWindow.json_load_file_chooser(mock_self)
        mock_self.load_file_to_table.assert_called_once_with(my_adi_file)

    # Check JSON read
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"CALL": "AAA", "MODE": "FT8"}))
    def test_read_data_from_json_file(self, mock_file):
        expected_output = {"CALL": "AAA", "MODE": "FT8"}
        filename = "/data/export.json"
        result = read_data_from_json_file(filename)

        # simple assertion that open was called
        mock_file.assert_called_with(filename, "r")
        self.assertEqual(expected_output, result)

    @patch('json.dump')
    @patch('builtins.open', new_callable=mock_open())
    def test_write_file_as_json(self, m, m_json):
        data = {"CALL": "AAA", "MODE": "FT8"}
        filename = "/data/export.json"
        write_file_as_json(filename, data)

        # simple assertion that your open was called
        m.assert_called_with(filename, 'w')

        # assert that you called m_json with your data
        m_json.assert_called_with(data, m.return_value.__enter__.return_value, indent=4)

# app = QApplication([])
# @patch('KissXPLog.kiss_xp_log.MainWindow.mock_dev_two')
# def test_mock_dev_one(self, mock):
#     instance = MainWindow()
#     instance.mock_dev_one()
#     mock.assert_called_once_with("bingo")
#
# def test_mock_dev_one2(self):
#     thing = MainWindow()
#     thing.mock_dev_two = MagicMock(return_value=3)
#     thing.mock_dev_one()
#     thing.mock_dev_two.assert_called_once_with("bingo")
