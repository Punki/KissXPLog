from unittest import TestCase

from KissXPLog.adif import remove_header_from_file, qso_status_from_adif_to_custom_mapping, \
    qso_status_from_custom_to_adif_mapping


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
        single_qso_dict_input = {"CARD_SEND": "Y", "CARD_RCVD": "R"}
        expect = {"CARD_SEND": "Y", "CARD_RCVD": "R", "CST_CARD_SEND": True, "CST_CARD_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_and_Request_CARD(self):
        single_qso_dict_input = {"CARD_SEND": "Q", "CARD_RCVD": "Y"}
        expect = {"CARD_SEND": "Q", "CARD_RCVD": "Y", "CST_CARD_RCVD": True, "CST_CARD_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Send_CARD(self):
        single_qso_dict_input = {"CARD_SEND": "Y"}
        expect = {"CARD_SEND": "Y", "CST_CARD_SEND": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_CARD(self):
        single_qso_dict_input = {"CARD_RCVD": "Y"}
        expect = {"CARD_RCVD": "Y", "CST_CARD_RCVD": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Request_CARD(self):
        single_qso_dict_input = {"CARD_SEND": "Q"}
        expect = {"CARD_SEND": "Q", "CST_CARD_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)


class MappingAdifToCustomStatusEQSL(TestCase):
    def test_SEND_and_Request_EQSL(self):
        single_qso_dict_input = {"EQSL_SEND": "Y", "EQSL_RCVD": "R"}
        expect = {"EQSL_SEND": "Y", "EQSL_RCVD": "R", "CST_EQSL_SEND": True, "CST_EQSL_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_and_Request_EQSL(self):
        single_qso_dict_input = {"EQSL_SEND": "Q", "EQSL_RCVD": "Y"}
        expect = {"EQSL_SEND": "Q", "EQSL_RCVD": "Y", "CST_EQSL_RCVD": True, "CST_EQSL_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Send_EQSL(self):
        single_qso_dict_input = {"EQSL_SEND": "Y"}
        expect = {"EQSL_SEND": "Y", "CST_EQSL_SEND": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_EQSL(self):
        single_qso_dict_input = {"EQSL_RCVD": "Y"}
        expect = {"EQSL_RCVD": "Y", "CST_EQSL_RCVD": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Request_EQSL(self):
        single_qso_dict_input = {"EQSL_SEND": "Q"}
        expect = {"EQSL_SEND": "Q", "CST_EQSL_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)


class MappingAdifToCustomStatusLOTW(TestCase):
    def test_SEND_and_Request_LOTW(self):
        single_qso_dict_input = {"LOTW_SEND": "Y", "LOTW_RCVD": "R"}
        expect = {"LOTW_SEND": "Y", "LOTW_RCVD": "R", "CST_LOTW_SEND": True, "CST_LOTW_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_and_Request_LOTW(self):
        single_qso_dict_input = {"LOTW_SEND": "Q", "LOTW_RCVD": "Y"}
        expect = {"LOTW_SEND": "Q", "LOTW_RCVD": "Y", "CST_LOTW_RCVD": True, "CST_LOTW_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Send_LOTW(self):
        single_qso_dict_input = {"LOTW_SEND": "Y"}
        expect = {"LOTW_SEND": "Y", "CST_LOTW_SEND": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_LOTW(self):
        single_qso_dict_input = {"LOTW_RCVD": "Y"}
        expect = {"LOTW_RCVD": "Y", "CST_LOTW_RCVD": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Request_LOTW(self):
        single_qso_dict_input = {"LOTW_SEND": "Q"}
        expect = {"LOTW_SEND": "Q", "CST_LOTW_REQUEST": True}

        result = qso_status_from_adif_to_custom_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)


class MappingCustomToAdifStatusCARD(TestCase):
    def test_SEND_and_Request_CARD(self):
        single_qso_dict_input = {"CST_CARD_SEND": True, "CST_CARD_REQUEST": True}
        expect = {"CST_CARD_SEND": True, "CST_CARD_REQUEST": True, "CARD_SEND": "Y", "CARD_RCVD": "R"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_and_Request_CARD(self):
        single_qso_dict_input = {"CST_CARD_RCVD": True, "CST_CARD_REQUEST": True}
        expect = {"CST_CARD_RCVD": True, "CST_CARD_REQUEST": True, "CARD_SEND": "Q", "CARD_RCVD": "Y"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Send_CARD(self):
        single_qso_dict_input = {"CST_CARD_SEND": True}
        expect = {"CST_CARD_SEND": True, "CARD_SEND": "Y", "CARD_RCVD": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_CARD(self):
        single_qso_dict_input = {"CST_CARD_RCVD": True}
        expect = {"CST_CARD_RCVD": True, "CARD_RCVD": "Y", "CARD_SEND": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Request_CARD(self):
        single_qso_dict_input = {"CST_CARD_REQUEST": True}
        expect = {"CST_CARD_REQUEST": True, "CARD_SEND": "Q", "CARD_RCVD": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)


class MappingCustomToAdifStatusEQSL(TestCase):
    def test_SEND_and_Request_EQSL(self):
        single_qso_dict_input = {"CST_EQSL_SEND": True, "CST_EQSL_REQUEST": True}
        expect = {"CST_EQSL_SEND": True, "CST_EQSL_REQUEST": True, "EQSL_SEND": "Y", "EQSL_RCVD": "R"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_and_Request_EQSL(self):
        single_qso_dict_input = {"CST_EQSL_RCVD": True, "CST_EQSL_REQUEST": True}
        expect = {"CST_EQSL_RCVD": True, "CST_EQSL_REQUEST": True, "EQSL_SEND": "Q", "EQSL_RCVD": "Y"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Send_EQSL(self):
        single_qso_dict_input = {"CST_EQSL_SEND": True}
        expect = {"CST_EQSL_SEND": True, "EQSL_SEND": "Y", "EQSL_RCVD": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_EQSL(self):
        single_qso_dict_input = {"CST_EQSL_RCVD": True}
        expect = {"CST_EQSL_RCVD": True, "EQSL_RCVD": "Y", "EQSL_SEND": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Request_EQSL(self):
        single_qso_dict_input = {"CST_EQSL_REQUEST": True}
        expect = {"CST_EQSL_REQUEST": True, "EQSL_SEND": "Q", "EQSL_RCVD": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)


class MappingCustomToAdifStatusLOTW(TestCase):
    def test_SEND_and_Request_LOTW(self):
        single_qso_dict_input = {"CST_LOTW_SEND": True, "CST_LOTW_REQUEST": True}
        expect = {"CST_LOTW_SEND": True, "CST_LOTW_REQUEST": True, "LOTW_SEND": "Y", "LOTW_RCVD": "R"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_and_Request_LOTW(self):
        single_qso_dict_input = {"CST_LOTW_RCVD": True, "CST_LOTW_REQUEST": True}
        expect = {"CST_LOTW_RCVD": True, "CST_LOTW_REQUEST": True, "LOTW_SEND": "Q", "LOTW_RCVD": "Y"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Send_LOTW(self):
        single_qso_dict_input = {"CST_LOTW_SEND": True}
        expect = {"CST_LOTW_SEND": True, "LOTW_SEND": "Y", "LOTW_RCVD": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_RCVD_LOTW(self):
        single_qso_dict_input = {"CST_LOTW_RCVD": True}
        expect = {"CST_LOTW_RCVD": True, "LOTW_RCVD": "Y", "LOTW_SEND": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)

    def test_Request_LOTW(self):
        single_qso_dict_input = {"CST_LOTW_REQUEST": True}
        expect = {"CST_LOTW_REQUEST": True, "LOTW_SEND": "Q", "LOTW_RCVD": "N"}

        result = qso_status_from_custom_to_adif_mapping(single_qso_dict_input)
        self.assertEqual(expect, result)
