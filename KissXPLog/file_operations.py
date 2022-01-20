import json
import logging

from PyQt5.QtWidgets import QFileDialog

from KissXPLog.adif import export_to_adif
from KissXPLog.messages import show_error_message
from KissXPLog.config import *


def initial_file_dialog_config(file_extension):
    filedialog = QFileDialog()
    filedialog.setDirectory(data_dir)
    filedialog.setViewMode(QFileDialog.Detail)
    if file_extension == "json":
        filedialog.setDefaultSuffix("json")
        filedialog.setNameFilter("Json Datenbank (*.json);;All files (*.*)")
        filedialog.selectFile("QSO_MGM_Export.json")
    elif file_extension == "adif" or "adi":
        filedialog.setDefaultSuffix("adi")
        filedialog.setNameFilter("Adif (*.adi);;All files (*.*)")
        filedialog.selectFile("QSO_Export.adi")
    else:
        logging.error(f"Data Type is not supported: {file_extension}")

    return filedialog


def generic_save_data_to_file(filename, data_to_write, exclude_fields=None):
    logging.debug(f"Save table to: {filename}.")
    # Todo Add saver way for > [0]
    file_extension = str(filename).strip().split(".", 1)[1]
    if file_extension == "json":
        write_file_as_json(filename, data_to_write)
    elif file_extension == "adi" or file_extension == "adif":
        export_to_adif(filename, data_to_write, exclude_fields)
    else:
        show_error_message("Error", f"Data Type is not supported: {file_extension}")
        return


def read_data_from_json_file(file_to_read_from):
    try:
        with open(file_to_read_from, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        show_error_message("Error", "File not found: {}.".format(file_to_read_from))
    except PermissionError:
        show_error_message("Error", "Access Denied to file: {}.".format(file_to_read_from))
    except IOError:
        show_error_message("Error", "IO Error.")
    except Exception as e:
        show_error_message("Error", "IDK man, something went wrong: {}".format(e))
    return data


def write_file_as_json(filename, data_to_write):
    with open(filename, "w") as open_file:
        json.dump(data_to_write, open_file, indent=4)
        logging.debug(f"File {filename} was written successfully")
