from unittest import TestCase

from KissXPLog.kiss_xp_log import add_new_information_to_qso_list, are_minimum_qso_data_present, remove_empty_fields


# Expect, Actual!
class QSO_ListForGui(TestCase):

    def test_add_new_qsos(self):
        old_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                    {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]

        new_qsos = [{"CALL": "CCC", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                    {"CALL": "DDD", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]

        expect = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                  {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                  {"CALL": "CCC", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                  {"CALL": "DDD", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]

        result = add_new_information_to_qso_list(old_qsos, new_qsos)
        self.assertEqual(expect, result)

    def test_no_changes(self):
        old_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                    {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]
        new_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                    {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]
        expect = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                  {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]

        result = add_new_information_to_qso_list(old_qsos, new_qsos)
        self.assertEqual(expect, result)

    def test_update_qsos(self):
        old_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                    {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                    {"CALL": "CCC", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                    {"CALL": "DDD", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}
                    ]
        new_qsos = [
            {"CALL": "CCC", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"}]

        expect = [
            {"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
            {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
            {"CALL": "CCC", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"},
            {"CALL": "DDD", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]

        result = add_new_information_to_qso_list(old_qsos, new_qsos)
        self.assertEqual(expect, result)

    def test_remove_empty_fields(self):
        input = {"CALL": "AAA", "QSO_DATE": "20190814", "MODE": False, "BAND": None, "TIME_ON": ""}
        expect = {"CALL": "AAA", "QSO_DATE": "20190814"}

        self.assertDictEqual(expect, remove_empty_fields(input))


class MinimalQSODataPresent(TestCase):
    ### Absolutes Minimum
    # Callsign
    # Date
    # UTC Time
    # Frequency
    # Mode
    # RST Sent / RST RCVD
    # {"CALL": "AAA", "QSO_DATE": "20200117", "TIME_ON": "182500", "FREQ": "7.012345", "MODE": "FT8", "RST_SENT": "-15","RST_RCVD": "-15"}
    def test_all_fields_no_data(self):
        empty_qso = {"CALL": "", "QSO_DATE": "", "TIME_ON": "", "FREQ": "", "MODE": "", "RST_SENT": "", "RST_RCVD": ""}
        self.assertFalse(are_minimum_qso_data_present(empty_qso))

    def test_just_some_fields_all_data(self):
        fields_missing = {"CALL": "AAA", "QSO_DATE": "20200117", "TIME_ON": "182500", "MODE": "FT8", "RST_SENT": "-15"}
        self.assertFalse(are_minimum_qso_data_present(fields_missing))

    def test_all_fields_with_missing_data(self):
        data_missing = {"CALL": "AAA", "QSO_DATE": "", "TIME_ON": "182500", "FREQ": "", "MODE": "FT8",
                        "RST_SENT": "-15",
                        "RST_RCVD": "-15"}
        self.assertFalse(are_minimum_qso_data_present(data_missing))

    def test_minimal_qso_with_fields_and_data(self):
        valid_qso = {"CALL": "AAA", "QSO_DATE": "20200117", "TIME_ON": "182500", "FREQ": "7.012345", "MODE": "FT8",
                     "RST_SENT": "-15", "RST_RCVD": "-15"}
        self.assertTrue(are_minimum_qso_data_present(valid_qso))
