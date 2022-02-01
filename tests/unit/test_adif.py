from unittest import TestCase

from KissXPLog.adif import remove_header_from_file, fix_time_without_seconds, \
    fix_band_and_freq_when_one_of_them_is_available


class RemoveHeaderFromAdif(TestCase):
    def test_remove_header_from_file(self):
        adif_with_header = "<ADIF_VER:5>2.2.7<ProgramID:8>AnyStuff<ProgramVersion:5>7.7.7<EOH><CALL:3>AAA<QSO_DATE:8" \
                           ">20190814<MODE:3>FT8<BAND:3>40m<TIME_ON:6>182500<EOR> "
        expect = "<CALL:3>AAA<QSO_DATE:8>20190814<MODE:3>FT8<BAND:3>40m<TIME_ON:6>182500<EOR>"

        result = remove_header_from_file(adif_with_header)
        self.assertEqual(expect, result)

    def test_pass_qso_without_header(self):
        adif_without_header = "<CALL:3>AAA<QSO_DATE:8>20190814<MODE:3>FT8<BAND:3>40m<TIME_ON:6>182500<EOR>"
        expect = "<CALL:3>AAA<QSO_DATE:8>20190814<MODE:3>FT8<BAND:3>40m<TIME_ON:6>182500<EOR>"

        result = remove_header_from_file(adif_without_header)
        self.assertEqual(expect, result)


class CommonImportProblems(TestCase):
    def test_convert_time_from_four_to_six_digits(self):
        expect = {"TIME_ON": "155500"}
        self.assertDictEqual(expect, fix_time_without_seconds({"TIME_ON": "1555"}))

    def test_do_nothing_if_freq_and_band(self):
        expected = {"FREQ": "7.012345", "BAND": "40m"}
        result = fix_band_and_freq_when_one_of_them_is_available(expected)
        self.assertEqual(expected, result)

    def test_edit_freq_if_band(self):
        expected = {"BAND": "40m", "FREQ": "7.0"}
        self.assertEqual(expected, fix_band_and_freq_when_one_of_them_is_available({"BAND": "40m"}))

    def test_edit_freq_if_band_case_sensitive(self):
        expected = {"BAND": "40M", "FREQ": "7.0"}
        self.assertEqual(expected, fix_band_and_freq_when_one_of_them_is_available({"BAND": "40M"}))

    def test_edit_band_if_freq(self):
        expected = {"FREQ": "7.012345", "BAND": "40m"}
        self.assertEqual(expected, fix_band_and_freq_when_one_of_them_is_available({"FREQ": "7.012345"}))

    def test_do_nothing_in_case_no_feq_and_no_band(self):
        expected = {}
        self.assertEqual(expected, fix_band_and_freq_when_one_of_them_is_available({}))
