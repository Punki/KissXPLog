from unittest import TestCase

from KissXPLog.kiss_xp_log import add_new_information_to_qso_list, are_minimum_qso_data_present, remove_empty_fields, \
    frequency_to_band, band_to_frequency


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


class MappingBandsAndFrequency(TestCase):
    def test_low_frequency(self):
        self.assertEqual("160m", frequency_to_band(1.81))
        self.assertEqual("80m", frequency_to_band(3.5))
        self.assertEqual("40m", frequency_to_band(7))
        self.assertEqual("30m", frequency_to_band(10.1))
        self.assertEqual("20m", frequency_to_band(14))
        self.assertEqual("17m", frequency_to_band(18.068))
        self.assertEqual("15m", frequency_to_band(21))
        self.assertEqual("12m", frequency_to_band(24.89))
        self.assertEqual("10m", frequency_to_band(28))

    def test_high_frequency(self):
        self.assertEqual("160m", frequency_to_band(2.0))
        self.assertEqual("80m", frequency_to_band(3.8))
        self.assertEqual("40m", frequency_to_band(7.2))
        self.assertEqual("30m", frequency_to_band(10.15))
        self.assertEqual("20m", frequency_to_band(14.35))
        self.assertEqual("17m", frequency_to_band(18.168))
        self.assertEqual("15m", frequency_to_band(21.45))
        self.assertEqual("12m", frequency_to_band(24.99))
        self.assertEqual("10m", frequency_to_band(29.7))



    def test_out_of_range_values(self):
        self.assertEqual(None, frequency_to_band(1.8))
        self.assertEqual(None, frequency_to_band(29.8))
        self.assertEqual(None, frequency_to_band(0))

    def test_negative_value(self):
        self.assertEqual(None, frequency_to_band(-14))

    def test_string(self):
        self.assertEqual("160m", frequency_to_band("1.81"))
        self.assertEqual("80m", frequency_to_band("3.5"))
        self.assertEqual("40m", frequency_to_band("7"))
        self.assertEqual("30m", frequency_to_band("10.1"))
        self.assertEqual("20m", frequency_to_band("14"))
        self.assertEqual("17m", frequency_to_band("18.068"))
        self.assertEqual("15m", frequency_to_band("21"))
        self.assertEqual("12m", frequency_to_band("24.89"))
        self.assertEqual("10m", frequency_to_band("28"))

    def test_band_to_frequency(self):
        self.assertEqual(1.81, band_to_frequency("160m"))
        self.assertEqual(3.5, band_to_frequency("80m"))
        self.assertEqual(7, band_to_frequency("40m"))
        self.assertEqual(10.1, band_to_frequency("30m"))
        self.assertEqual(14, band_to_frequency("20m"))
        self.assertEqual(18.068, band_to_frequency("17m"))
        self.assertEqual(21, band_to_frequency("15m"))
        self.assertEqual(24.89, band_to_frequency("12m"))
        self.assertEqual(28, band_to_frequency("10m"))

    def test_band_not_mapped_frequency(self):
        self.assertEqual(None, band_to_frequency("0m"))

    def test_not_string_frequency(self):
        self.assertEqual(None, band_to_frequency(20))


