def remove_empty_fields(qso_to_check):
    """Removes None, "", False values from dict."""
    cleaned_qso = {k: v for k, v in qso_to_check.items() if v}
    return cleaned_qso


def prune_qsos(qsos_to_check):
    """
    Remove Empty Fields from Qsos.
    :param qsos_to_check:
    :type qsos_to_check:List[dict]
    :return:List[dict]
    """
    return list(map(remove_empty_fields, qsos_to_check))


def add_new_information_to_qso_list(old_qsos, new_qsos):
    # Only Update the Dict if more Fields are in the new
    # Quadratischer Aufwand da doppel loop!
    new_qsos = remove_duplicates_in_new_qsos(old_qsos, new_qsos)
    old_qsos = update_old_qsos_with_new_information(old_qsos, new_qsos)
    old_qsos = add_new_qsos_to_list(old_qsos, new_qsos)
    return old_qsos


def are_minimum_qso_data_present(qso_to_check):
    minimal_qso_keys = ["CALL", "QSO_DATE", "TIME_ON", "FREQ", "MODE", "RST_SENT", "RST_RCVD"]
    # Sicherstellen alle benötigten Keys vorhanden sind und Values nicht None oder '' sind.
    for k in minimal_qso_keys:
        if not qso_to_check.get(k):
            return False
    return True


def remove_duplicates_in_new_qsos(old_qso_dict_list, new_qso_dict_list):
    # Remove duplicate dicts from new qso list
    for dict_old in old_qso_dict_list:
        for dict_new in new_qso_dict_list:
            if dict_old == dict_new:
                new_qso_dict_list.remove(dict_new)
    return new_qso_dict_list


def update_old_qsos_with_new_information(old_qso_dict_list, new_qso_dict_list):
    # Compare Unique Values from Qso and Update
    for dict_old in old_qso_dict_list:
        for dict_new in new_qso_dict_list:
            if dict_old.get("CALL") == dict_new.get("CALL") and \
                    dict_old.get("QSO_DATE") == dict_new.get("QSO_DATE") and \
                    dict_old.get("MODE") == dict_new.get("MODE") and \
                    dict_old.get("BAND") == dict_new.get("BAND") and \
                    dict_old.get("TIME_ON") == dict_new.get("TIME_ON"):
                # Nimm den Eintrag mit mehr Einträgen im Zweifel
                if len(dict_old) <= len(dict_new):
                    dict_old.update(dict_new)
                new_qso_dict_list.remove(dict_new)
    return old_qso_dict_list


def add_new_qsos_to_list(old_qso_dict_list, new_qso_dict_list):
    old_qso_dict_list.extend(new_qso_dict_list)
    return old_qso_dict_list
