from unittest import TestCase

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication

from KissXPLog import MainWindow


class TestJsonFileHandling(TestCase):
    app = QApplication([])

    def setUp(self):
        self.window = MainWindow()

    def test_input_values_converted_korrekt(self):
        input_data = {'CALL': 'TESTTESTTEST', 'QSO_DATE': '20201119', 'TIME_ON': '155300',
                      'MODE': 'JT65', 'SUBMODE': 'JT65A', 'RST_SENT': '-18', 'RST_RCVD': '-23',
                      'BAND': '40m', 'FREQ': '7', 'NAME': 'JohnDoe', 'NOTES': 'notes?', 'COMMENT': 'nope',
                      'QSL_RCVD': 'R', 'QSL_SENT': 'Y', 'EQSL_QSL_RCVD': "", 'EQSL_QSL_SENT': "",
                      'LOTW_QSL_RCVD': "", 'LOTW_QSL_SENT': "", 'COUNTRY': 'Switzerland', 'STATE': 'VS',
                      'QSLSDATE': '20221231', 'CQZone': '', 'Continent': '', 'ITUZone': ''}
        self.window.fill_values_to_edit_form(input_data)
        output = self.window.get_dict_from_inputform()
        self.assertDictEqual(input_data, output)

    def test_qsl_sent_option1(self):
        input_data = {'QSL_SENT': 'Y', 'QSL_RCVD': 'Y'}
        self.window.fill_values_to_edit_form(input_data)
        fulloutput = self.window.get_dict_from_inputform()
        only_test_fields = {'QSL_SENT': fulloutput.get('QSL_SENT'), 'QSL_RCVD': fulloutput.get('QSL_RCVD')}
        self.assertEqual(input_data, only_test_fields)

    def test_qsl_sent_option2(self):
        input_data = {'QSL_SENT': 'N', 'QSL_RCVD': 'Y'}
        self.window.fill_values_to_edit_form(input_data)
        fulloutput = self.window.get_dict_from_inputform()
        only_test_fields = {'QSL_SENT': fulloutput.get('QSL_SENT'), 'QSL_RCVD': fulloutput.get('QSL_RCVD')}
        self.assertEqual(input_data, only_test_fields)

    def test_qsl_sent_option3(self):
        input_data = {'QSL_SENT': 'R', 'QSL_RCVD': 'Y'}
        self.window.fill_values_to_edit_form(input_data)
        fulloutput = self.window.get_dict_from_inputform()
        only_test_fields = {'QSL_SENT': fulloutput.get('QSL_SENT'), 'QSL_RCVD': fulloutput.get('QSL_RCVD')}
        self.assertEqual(input_data, only_test_fields)

    def test_qsl_sent_option4(self):
        input_data = {'QSL_SENT': 'Q', 'QSL_RCVD': 'Y'}
        self.window.fill_values_to_edit_form(input_data)
        fulloutput = self.window.get_dict_from_inputform()
        only_test_fields = {'QSL_SENT': fulloutput.get('QSL_SENT'), 'QSL_RCVD': fulloutput.get('QSL_RCVD')}
        self.assertEqual(input_data, only_test_fields)

    def test_qsl_sent_option5(self):
        input_data = {'QSL_SENT': 'I', 'QSL_RCVD': 'Y'}
        self.window.fill_values_to_edit_form(input_data)
        fulloutput = self.window.get_dict_from_inputform()
        only_test_fields = {'QSL_SENT': fulloutput.get('QSL_SENT'), 'QSL_RCVD': fulloutput.get('QSL_RCVD')}
        self.assertEqual(input_data, only_test_fields)

    def test_qsl_rcvd_option1(self):
        input_data = {'QSL_SENT': 'Y', 'QSL_RCVD': 'N'}
        self.window.fill_values_to_edit_form(input_data)
        fulloutput = self.window.get_dict_from_inputform()
        only_test_fields = {'QSL_SENT': fulloutput.get('QSL_SENT'), 'QSL_RCVD': fulloutput.get('QSL_RCVD')}
        self.assertEqual(input_data, only_test_fields)

    def test_qsl_rcvd_option2(self):
        input_data = {'QSL_SENT': 'Y', 'QSL_RCVD': 'R'}
        self.window.fill_values_to_edit_form(input_data)
        fulloutput = self.window.get_dict_from_inputform()
        only_test_fields = {'QSL_SENT': fulloutput.get('QSL_SENT'), 'QSL_RCVD': fulloutput.get('QSL_RCVD')}
        self.assertEqual(input_data, only_test_fields)

    def test_qsl_rcvd_option3(self):
        input_data = {'QSL_SENT': 'Y', 'QSL_RCVD': 'I'}
        self.window.fill_values_to_edit_form(input_data)
        fulloutput = self.window.get_dict_from_inputform()
        only_test_fields = {'QSL_SENT': fulloutput.get('QSL_SENT'), 'QSL_RCVD': fulloutput.get('QSL_RCVD')}
        self.assertEqual(input_data, only_test_fields)

    # QSL Sent-Date Tests:
    def test_qslSentDate_is_activ(self):
        input_data = {'QSL_SENT': 'Y'}
        self.window.fill_values_to_edit_form(input_data)
        self.assertTrue(self.window.ui.de_qsl_sent_date.isEnabled())

    def test_qslSentDate_is_deactivated(self):
        input_data = {'QSL_SENT': 'N'}
        self.window.fill_values_to_edit_form(input_data)
        self.assertFalse(self.window.ui.de_qsl_sent_date.isEnabled())

    def test_qslSentDate_is_set(self):
        input_data = {'QSLSDATE': '22221231'}
        self.window.fill_values_to_edit_form(input_data)
        self.assertEqual('22221231', self.window.ui.de_qsl_sent_date.date().toString("yyyyMMdd"))

    def test_qslSentDate_is_set_to_today_if_card_sent_is_yes(self):
        input_data = {'QSL_SENT': 'Y'}
        self.window.fill_values_to_edit_form(input_data)
        self.assertEqual(QDate.currentDate().toString("yyyyMMdd"),
                         self.window.ui.de_qsl_sent_date.date().toString("yyyyMMdd"))

    def test_qslSentDate_converted_correctly(self):
        input_data = {'QSL_SENT': 'Y', 'QSLSDATE': '22221231'}
        self.window.fill_values_to_edit_form(input_data)
        fulloutput = self.window.get_dict_from_inputform()
        only_test_fields = {'QSL_SENT': fulloutput.get('QSL_SENT'), 'QSLSDATE': fulloutput.get('QSLSDATE')}
        self.assertEqual(input_data, only_test_fields)

    def test_dont_write_qslSentDate_if_qslSend_is_not_Yes(self):
        input_data = {'QSL_SENT': 'N', 'QSLSDATE': '22221231'}
        self.window.fill_values_to_edit_form(input_data)
        fulloutput = self.window.get_dict_from_inputform()
        self.assertEqual("", fulloutput.get('QSLSDATE'))

    # QSL Sent-Date Error Checks -> Set Date to Today:
    def test_qslSentDate_is_None(self):
        input_data = {'QSL_SENT': 'Y', 'QSLSDATE': None}
        self.window.fill_values_to_edit_form(input_data)
        self.assertEqual(QDate.currentDate().toString("yyyyMMdd"),
                         self.window.ui.de_qsl_sent_date.date().toString("yyyyMMdd"))

    def test_qslSentDate_is_Empty(self):
        input_data = {'QSL_SENT': 'Y', 'QSLSDATE': ""}
        self.window.fill_values_to_edit_form(input_data)
        self.assertEqual(QDate.currentDate().toString("yyyyMMdd"),
                         self.window.ui.de_qsl_sent_date.date().toString("yyyyMMdd"))

    def test_qslSentDate_is_invalid(self):
        input_data = {'QSL_SENT': 'Y', 'QSLSDATE': "999999999999999"}
        self.window.fill_values_to_edit_form(input_data)
        self.assertEqual(QDate.currentDate().toString("yyyyMMdd"),
                         self.window.ui.de_qsl_sent_date.date().toString("yyyyMMdd"))

    def test_qslSentDate_is_not_set(self):
        input_data = {'QSL_SENT': 'Y'}
        self.window.fill_values_to_edit_form(input_data)
        self.assertEqual(QDate.currentDate().toString("yyyyMMdd"),
                         self.window.ui.de_qsl_sent_date.date().toString("yyyyMMdd"))
