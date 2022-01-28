from unittest import TestCase

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
                      'QSL_RCVD': 'R', 'QSL_SENT': 'Y', 'EQSL_QSL_RCVD': False, 'EQSL_QSL_SENT': True,
                      'LOTW_QSL_RCVD': True, 'LOTW_QSL_SENT': False,
                      'COUNTRY': 'Swiss', 'STATE': 'VS'}
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
