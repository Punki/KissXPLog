import logging
import re

# todo Exception handling
# verify Adif Data
from KissXPLog.static_adif_fields import BAND_WITH_FREQUENCY


def parse_adif_for_data(filename):
    new_data = read(filename)
    return parse_adif(new_data)


def read(filename):
    logging.info("Reading file {}".format(filename))
    try:
        with open(filename, "r") as file_handler:
            adif_raw_file_input = file_handler.read()
    except FileNotFoundError:
        logging.error(f"ADIF-File not found: {filename}.")
    except PermissionError:
        logging.error(f"Access Denied to file {filename}.")
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
        logging.error(f"Error while writing header to file {filename}: {e}")
    # Write Data to File:
    with open(filename, "a") as open_file:
        for qso in qsos_to_write:
            for element in qso:
                if element in exclude_list:
                    continue
                try:
                    open_file.write(f"<{element}:{len(qso.get(element))}>{qso.get(element)}")
                    logging.debug(f"Logging Element {element} of qso {qso}")
                except Exception as e:
                    logging.error(f"Error while writing qso {qso} to file {filename}: {e}")
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

    #qso_status_from_adif_to_custom_mapping(single_qso_dict)
    fix_time_without_seconds(single_qso_dict)
    fix_band_and_freq_when_one_of_them_is_available(single_qso_dict)
    return single_qso_dict


def frequency_to_band(MHz_to_check):
    try:
        MHz_to_check = float(MHz_to_check)
        for band in BAND_WITH_FREQUENCY:
            if BAND_WITH_FREQUENCY.get(band)[0] <= MHz_to_check <= BAND_WITH_FREQUENCY.get(band)[1]:
                return band
    except ValueError as e:
        logging.error("Could not convert 'MHz_to_check' to float: {0}".format(e))


def band_to_frequency(band):
    band = str(band).lower()
    if band in BAND_WITH_FREQUENCY:
        return BAND_WITH_FREQUENCY.get(band)[0]


def fix_time_without_seconds(single_qso_dict):
    if len(single_qso_dict.get('TIME_ON')) < 6:
        t_on = single_qso_dict.get('TIME_ON')
        t_on += "00"
        single_qso_dict.update({'TIME_ON': t_on})
    return single_qso_dict


def fix_band_and_freq_when_one_of_them_is_available(single_qso_dict):
    if single_qso_dict.get('BAND') != single_qso_dict.get('FREQ'):
        band = single_qso_dict.get('BAND')
        freq = single_qso_dict.get('FREQ')
        if band and not freq:
            if freq := band_to_frequency(band):
                single_qso_dict['FREQ'] = str(freq)
        elif freq and not band:
            if band := frequency_to_band(freq):
                single_qso_dict['BAND'] = str(band)

    return single_qso_dict

