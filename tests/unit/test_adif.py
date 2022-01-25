from unittest import TestCase

from KissXPLog.adif import remove_header_from_file, qso_status_from_adif_to_custom_mapping, \
    qso_status_from_custom_to_adif_mapping, fix_time_without_seconds, fix_band_and_freq_when_one_of_them_is_available


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


class MappingAdifToCustomStatusCARD(TestCase):

    def test_SEND_and_Request_CARD(self):
        single_qso_dict_input = {"QSL_SENT": "Y", "QSL_RCVD": "R"}
        expect = {"QSL_SENT": "Y", "QSL_RCVD": "R", "CST_QSL_SENT": True, "CST_QSL_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_and_Request_CARD(self):
        single_qso_dict_input = {"QSL_SENT": "Q", "QSL_RCVD": "Y"}
        expect = {"QSL_SENT": "Q", "QSL_RCVD": "Y", "CST_QSL_RCVD": True, "CST_QSL_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Sent_CARD(self):
        single_qso_dict_input = {"QSL_SENT": "Y"}
        expect = {"QSL_SENT": "Y", "CST_QSL_SENT": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_CARD(self):
        single_qso_dict_input = {"QSL_RCVD": "Y"}
        expect = {"QSL_RCVD": "Y", "CST_QSL_RCVD": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Request_CARD(self):
        single_qso_dict_input = {"QSL_SENT": "Q"}
        expect = {"QSL_SENT": "Q", "CST_QSL_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)


class MappingAdifToCustomStatusEQSL(TestCase):
    def test_SEND_and_Request_EQSL(self):
        single_qso_dict_input = {"EQSL_QSL_SENT": "Y", "EQSL_QSL_RCVD": "R"}
        expect = {"EQSL_QSL_SENT": "Y", "EQSL_QSL_RCVD": "R", "CST_EQSL_QSL_SENT": True, "CST_EQSL_QSL_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_and_Request_EQSL(self):
        single_qso_dict_input = {"EQSL_QSL_SENT": "Q", "EQSL_QSL_RCVD": "Y"}
        expect = {"EQSL_QSL_SENT": "Q", "EQSL_QSL_RCVD": "Y", "CST_EQSL_QSL_RCVD": True, "CST_EQSL_QSL_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Sent_EQSL(self):
        single_qso_dict_input = {"EQSL_QSL_SENT": "Y"}
        expect = {"EQSL_QSL_SENT": "Y", "CST_EQSL_QSL_SENT": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_EQSL(self):
        single_qso_dict_input = {"EQSL_QSL_RCVD": "Y"}
        expect = {"EQSL_QSL_RCVD": "Y", "CST_EQSL_QSL_RCVD": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Request_EQSL(self):
        single_qso_dict_input = {"EQSL_QSL_SENT": "Q"}
        expect = {"EQSL_QSL_SENT": "Q", "CST_EQSL_QSL_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)


class MappingAdifToCustomStatusLOTW(TestCase):
    def test_SEND_and_Request_LOTW(self):
        single_qso_dict_input = {"LOTW_QSL_SENT": "Y", "LOTW_QSL_RCVD": "R"}
        expect = {"LOTW_QSL_SENT": "Y", "LOTW_QSL_RCVD": "R", "CST_LOTW_QSL_SENT": True, "CST_LOTW_QSL_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_and_Request_LOTW(self):
        single_qso_dict_input = {"LOTW_QSL_SENT": "Q", "LOTW_QSL_RCVD": "Y"}
        expect = {"LOTW_QSL_SENT": "Q", "LOTW_QSL_RCVD": "Y", "CST_LOTW_QSL_RCVD": True, "CST_LOTW_QSL_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Sent_LOTW(self):
        single_qso_dict_input = {"LOTW_QSL_SENT": "Y"}
        expect = {"LOTW_QSL_SENT": "Y", "CST_LOTW_QSL_SENT": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_LOTW(self):
        single_qso_dict_input = {"LOTW_QSL_RCVD": "Y"}
        expect = {"LOTW_QSL_RCVD": "Y", "CST_LOTW_QSL_RCVD": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Request_LOTW(self):
        single_qso_dict_input = {"LOTW_QSL_SENT": "Q"}
        expect = {"LOTW_QSL_SENT": "Q", "CST_LOTW_QSL_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)


class MappingCustomToAdifStatusCARD(TestCase):
    def test_SEND_and_Request_CARD(self):
        single_qso_dict_input = {"CST_QSL_SENT": True, "CST_QSL_REQUEST": True}
        expect = {"CST_QSL_SENT": True, "CST_QSL_REQUEST": True, "QSL_SENT": "Y", "QSL_RCVD": "R"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_and_Request_CARD(self):
        single_qso_dict_input = {"CST_QSL_RCVD": True, "CST_QSL_REQUEST": True}
        expect = {"CST_QSL_RCVD": True, "CST_QSL_REQUEST": True, "QSL_SENT": "Q", "QSL_RCVD": "Y"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Sent_CARD(self):
        single_qso_dict_input = {"CST_QSL_SENT": True}
        expect = {"CST_QSL_SENT": True, "QSL_SENT": "Y", "QSL_RCVD": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_CARD(self):
        single_qso_dict_input = {"CST_QSL_RCVD": True}
        expect = {"CST_QSL_RCVD": True, "QSL_RCVD": "Y", "QSL_SENT": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Request_CARD(self):
        single_qso_dict_input = {"CST_QSL_REQUEST": True}
        expect = {"CST_QSL_REQUEST": True, "QSL_SENT": "Q", "QSL_RCVD": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)


class MappingCustomToAdifStatusEQSL(TestCase):
    def test_SEND_and_Request_EQSL(self):
        single_qso_dict_input = {"CST_EQSL_QSL_SENT": True, "CST_EQSL_QSL_REQUEST": True}
        expect = {"CST_EQSL_QSL_SENT": True, "CST_EQSL_QSL_REQUEST": True, "EQSL_QSL_SENT": "Y", "EQSL_QSL_RCVD": "R"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_and_Request_EQSL(self):
        single_qso_dict_input = {"CST_EQSL_QSL_RCVD": True, "CST_EQSL_QSL_REQUEST": True}
        expect = {"CST_EQSL_QSL_RCVD": True, "CST_EQSL_QSL_REQUEST": True, "EQSL_QSL_SENT": "Q", "EQSL_QSL_RCVD": "Y"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Sent_EQSL(self):
        single_qso_dict_input = {"CST_EQSL_QSL_SENT": True}
        expect = {"CST_EQSL_QSL_SENT": True, "EQSL_QSL_SENT": "Y", "EQSL_QSL_RCVD": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_EQSL(self):
        single_qso_dict_input = {"CST_EQSL_QSL_RCVD": True}
        expect = {"CST_EQSL_QSL_RCVD": True, "EQSL_QSL_RCVD": "Y", "EQSL_QSL_SENT": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Request_EQSL(self):
        single_qso_dict_input = {"CST_EQSL_QSL_REQUEST": True}
        expect = {"CST_EQSL_QSL_REQUEST": True, "EQSL_QSL_SENT": "Q", "EQSL_QSL_RCVD": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)


class MappingCustomToAdifStatusLOTW(TestCase):
    def test_SEND_and_Request_LOTW(self):
        single_qso_dict_input = {"CST_LOTW_QSL_SENT": True, "CST_LOTW_QSL_REQUEST": True}
        expect = {"CST_LOTW_QSL_SENT": True, "CST_LOTW_QSL_REQUEST": True, "LOTW_QSL_SENT": "Y", "LOTW_QSL_RCVD": "R"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_and_Request_LOTW(self):
        single_qso_dict_input = {"CST_LOTW_QSL_RCVD": True, "CST_LOTW_QSL_REQUEST": True}
        expect = {"CST_LOTW_QSL_RCVD": True, "CST_LOTW_QSL_REQUEST": True, "LOTW_QSL_SENT": "Q", "LOTW_QSL_RCVD": "Y"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Sent_LOTW(self):
        single_qso_dict_input = {"CST_LOTW_QSL_SENT": True}
        expect = {"CST_LOTW_QSL_SENT": True, "LOTW_QSL_SENT": "Y", "LOTW_QSL_RCVD": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_LOTW(self):
        single_qso_dict_input = {"CST_LOTW_QSL_RCVD": True}
        expect = {"CST_LOTW_QSL_RCVD": True, "LOTW_QSL_RCVD": "Y", "LOTW_QSL_SENT": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Request_LOTW(self):
        single_qso_dict_input = {"CST_LOTW_QSL_REQUEST": True}
        expect = {"CST_LOTW_QSL_REQUEST": True, "LOTW_QSL_SENT": "Q", "LOTW_QSL_RCVD": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
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
