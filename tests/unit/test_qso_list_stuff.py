from unittest import TestCase

from KissXPLog.qso_operations import remove_duplicates_in_new_qsos, update_old_qsos_with_new_information, \
    add_new_qsos_to_list


# actual_output, expected_output
# result

class TestRemoveDuplicates(TestCase):

    def test_remove_duplicates_in_new_qsos(self):
        old_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8"},
                    {"CALL": "BBB", "QSO_DATE": "20190815", "MODE": "FT8"}]
        new_qsos = [{"CALL": "BBB", "QSO_DATE": "20190815", "MODE": "FT8"},
                    {"CALL": "EEE", "QSO_DATE": "20190815", "MODE": "FT8"}]
        expected_new_qso = [{"CALL": "EEE", "QSO_DATE": "20190815", "MODE": "FT8"}]
        self.assertEqual(expected_new_qso, remove_duplicates_in_new_qsos(old_qsos, new_qsos))

    def test_remove_duplicates_with_same_item_input(self):
        old_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8"},
                    {"CALL": "BBB", "QSO_DATE": "20190815", "MODE": "FT8"}]
        new_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8"},
                    {"CALL": "BBB", "QSO_DATE": "20190815", "MODE": "FT8"}]
        self.assertEqual([], remove_duplicates_in_new_qsos(old_qsos, new_qsos))

    def test_remove_duplicates_no_dupes_in_list(self):
        old_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8"},
                    {"CALL": "BBB", "QSO_DATE": "20190815", "MODE": "FT8"}]
        new_qsos = [{"CALL": "BBB", "QSO_DATE": "20190800", "MODE": "FT8"},
                    {"CALL": "EEE", "QSO_DATE": "20190800", "MODE": "FT8"}]
        self.assertEqual(new_qsos, remove_duplicates_in_new_qsos(old_qsos, new_qsos))

    def test_remove_duplicates_with_no_over_jumps(self):
        old_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8"},
                    {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8"}]

        new_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8"},
                    {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8"},
                    {"CALL": "CCC", "QSO_DATE": "20190814", "MODE": "FT8"},
                    {"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8"}]
        expected_new = [{"CALL": "CCC", "QSO_DATE": "20190814", "MODE": "FT8"}]
        self.assertEqual(expected_new, remove_duplicates_in_new_qsos(old_qsos, new_qsos))


class TestUpdateQSOsInDict(TestCase):
    def test_add_new_information(self):
        old_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                    {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]
        new_qsos = [
            {"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"},
            {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"}]
        # Updatet QSOs will be removed from new_qso List...
        expected_new = [
            {"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28", },
            {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"}]
        self.assertEqual(expected_new, update_old_qsos_with_new_information(old_qsos, new_qsos))

    def test_dont_update_if_QSO_not_match(self):
        old_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                    {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]
        new_qsos = [
            {"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"},
            {"CALL": "BBB", "QSO_DATE": "000000", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"}]
        expected_new = [
            {"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"},
            {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]

        self.assertEqual(expected_new, update_old_qsos_with_new_information(old_qsos, new_qsos))

    def test_not_all_elements_match(self):
        old_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                    {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]

        new_qsos = [
            {"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"},
            {"CALL": "BBB", "QSO_DATE": "000000", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"},
            {"CALL": "CCC", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"}]

        expected_new = [
            {"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"},
            {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]

        self.assertEqual(expected_new, update_old_qsos_with_new_information(old_qsos, new_qsos))

    def test_missing_fields(self):
        old_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                    {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]
        new_qsos = [
            {"CALL": "AAA", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"},
            {"CALL": "BBB", "QSO_DATE": None, "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500", "CQZ": "15",
             "ITUZ": "28"}]
        self.assertEqual(old_qsos, update_old_qsos_with_new_information(old_qsos, new_qsos))


class TestAddQSOsToList(TestCase):
    def test_add_new_qsos_to_list(self):
        old_qsos = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                    {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]

        new_qsos = [{"CALL": "CCC", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                    {"CALL": "DDD", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]

        expected_new = [{"CALL": "AAA", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                        {"CALL": "BBB", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                        {"CALL": "CCC", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"},
                        {"CALL": "DDD", "QSO_DATE": "20190814", "MODE": "FT8", "BAND": "40m", "TIME_ON": "182500"}]

        self.assertEqual(expected_new, add_new_qsos_to_list(old_qsos, new_qsos))
