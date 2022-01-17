import logging
import re


# todo Exception handling
# verify Adif Data


def parse_adif_for_data(filename):
    new_data = read(filename)
    return parse_adif(new_data)


def read(filename):
    logging.info("Reading file {}".format(filename))
    try:
        with open(filename, "r") as file_handler:
            adif_raw_file_input = file_handler.read()
    except FileNotFoundError:
        logging.error("ADIF-File not found: {}.".format(filename))
    except PermissionError:
        logging.error("Access Denied to file {}.".format(filename))
    except Exception as e:
        logging.error("IDK man, something went wrong: {}".format(e))
        adif_raw_file_input = False
    return adif_raw_file_input


def export_to_adif(filename, qsos_to_write, exclude_list):
    adif_ver = "3"
    program_id = "0.1"
    program_version = "0.1"
    app_created = "KissXPLog"
    app_created_date = "18.11.2020 23:24:41"  # datetime.today().strftime("%d.%m.%Y %H:%M:%S")

    # Open File + Handler.
    try:
        with open(filename, "w") as open_file:
            # Write Header to File:
            # logging.debug("Bummel")
            open_file.write(f"<ADIF_VER:{len(adif_ver)}>{adif_ver}" + "\n")
            open_file.write(f"<ProgramID:{len(program_id)}>{program_id}" + "\n")
            open_file.write(f"<ProgramVersion:{len(program_version)}>{program_version}" + "\n")
            open_file.write(f"<{app_created}:{len(app_created_date)}>{app_created_date}" + "\n")
            open_file.write("<EOH>" + "\n")
    except Exception as e:
        logging.error("Error while writing header to file {}: {}".format(filename, e))
    # Write Data to File:
    with open(filename, "a") as open_file:
        # logging.debug("Bimmel")
        for qso in qsos_to_write:
            for element in qso:
                if element in exclude_list:
                    continue
                try:
                    # logging.debug("Bammel")
                    open_file.write(f"<{element}:{len(qso.get(element))}>{qso.get(element)}")
                    logging.debug("Logging Element {} of qso {}".format(element, qso))
                except Exception as e:
                    logging.error("Error while writing qso {} to file {}: {}".format(qso, filename, e))
            # logging.info("Bömmel")
            open_file.write("<EOR> \n")


def remove_header_from_file(adif_text_file):
    # Split the Header and the QSO's
    splittet_raw_with_header = re.split("(?i)<eoh>", adif_text_file)
    if len(splittet_raw_with_header) == 2:
        # Remove Header[0]..
        return splittet_raw_with_header[1].strip()
    else:
        return splittet_raw_with_header[0].strip()


def parse_adif(adif_text_file):
    raw_all_in_one_qso = remove_header_from_file(adif_text_file)
    # Get a String for One QSO
    raw_full_qso_list = re.split("(?i)<eor>", raw_all_in_one_qso)
    # Remove Whitespaces at the beginning and end of the String
    raw_full_qso_list = [i.strip() for i in raw_full_qso_list]
    raw_full_qso_list = list(filter(None, raw_full_qso_list))

    # Final List with the Processed QSOs
    list_of_QSOs = []

    # Split the List in Single QSOs
    for single_raw_qso in raw_full_qso_list:
        actual_qso = {}
        actual_qso = split_single_QSO(single_raw_qso)
        # Collection of all QSOs
        list_of_QSOs.append(actual_qso)

    return list_of_QSOs


def split_single_QSO(single_raw_qso):
    field_value = {}
    # Spezial Pattern for Adif: <QSO_DATE:8>20190823
    # [^abc] >>Matches any character except for an a, b or c
    # + >> Matches One or more
    # pattern = re.compile("<(.*?):(\d*).*?>([^<]+)")
    pattern = re.compile("<([^:]+):(\d+[^>]*)>([^<]+)?")
    single_qso_dict = {}
    # List of Triples with Name, Length, Value
    fields_and_values_from_qso = pattern.findall(single_raw_qso)

    for item in fields_and_values_from_qso:
        field_name = item[0].upper().strip()
        field_length = int(item[1])

        try:
            field_value = item[2][0:int(item[1])]
        except len(item[2].strip()) != field_length:
            logging.error("We have a Problem! - Field value is: ", item[2], "and length for Field is: ", field_length)

        # Write the QSO in a Dictionary (Key:Value)
        single_qso_dict[field_name] = field_value

    qso_status_from_adif_to_custom_mapping(single_qso_dict)
    return single_qso_dict


def qso_status_from_adif_to_custom_mapping(single_qso_dict):
    all_options = ["CARD", "EQSL", "LOTW"]

    for option in all_options:

        generic_send = single_qso_dict.get(F"{option}_SEND")
        generic_rcvd = single_qso_dict.get(F"{option}_RCVD")

        CST_Option_SEND = F"CST_{option}_SEND"
        CST_Option_RCVD = F"CST_{option}_RCVD"
        CST_Option_REQUEST = F"CST_{option}_REQUEST"

        if generic_send == 'Y' and generic_rcvd == 'R':
            single_qso_dict.update({CST_Option_SEND: True})
            single_qso_dict.update({CST_Option_REQUEST: True})

        elif generic_rcvd == 'Y' and generic_send == 'Q':
            single_qso_dict.update({CST_Option_RCVD: True})
            single_qso_dict.update({CST_Option_REQUEST: True})

        if generic_send == 'Q':
            single_qso_dict.update({CST_Option_REQUEST: True})
        if generic_send == 'Y':
            single_qso_dict.update({CST_Option_SEND: True})
        if generic_rcvd == 'Y':
            single_qso_dict.update({CST_Option_RCVD: True})

    return single_qso_dict


def qso_status_from_custom_to_adif_mapping(single_qso_dict):
    all_options = ["CARD", "EQSL", "LOTW"]

    for option in all_options:
        # 'CST_CARD_SEND'/'CST_CARD_RCVD'/'CST_CARD_REQUEST'
        cst_generic_send = F"CST_{option}_SEND"
        cst_generic_rcvd = F"CST_{option}_RCVD"
        cst_generic_request = F"CST_{option}_REQUEST"

        # Values holen, true or false
        cst_card_send = single_qso_dict.get(cst_generic_send)
        cst_card_rcvd = single_qso_dict.get(cst_generic_rcvd)
        cst_card_request = single_qso_dict.get(cst_generic_request)

        # 'CARD_SEND'/'CARD_RCVD'
        Option_SEND = F"{option}_SEND"
        Option_RCVD = F"{option}_RCVD"

        # Don't Touch Fields if nothing changed
        if cst_card_send or cst_card_rcvd or cst_card_request:

            single_qso_dict.update({Option_SEND: 'N'})
            single_qso_dict.update({Option_RCVD: 'N'})

            if cst_card_send and cst_card_request:
                single_qso_dict.update({Option_SEND: 'Y'})
                single_qso_dict.update({Option_RCVD: 'R'})

            elif cst_card_rcvd and cst_card_request:
                single_qso_dict.update({Option_RCVD: 'Y'})
                single_qso_dict.update({Option_SEND: 'Q'})

            else:
                if cst_card_request:
                    single_qso_dict.update({Option_SEND: 'Q'})
                if cst_card_send:
                    single_qso_dict.update({Option_SEND: 'Y'})
                if cst_card_rcvd:
                    single_qso_dict.update({Option_RCVD: 'Y'})

    return single_qso_dict
