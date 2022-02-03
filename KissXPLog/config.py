import json
import logging
import os

work_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(work_dir, "data")
config_file = os.path.join(data_dir, "config.json")

user_settings = {}
user_settings['Autosave'] = None
user_settings['AutosaveIntervall'] = None
user_settings['MY_BANDS'] = None
user_settings['MY_Modes'] = None
user_settings['STATION_CALLSIGN'] = None
user_settings['MY_CQ_ZONE'] = None
user_settings['MY_ITU_ZONE'] = None




def save_user_settings_to_file():
    with open(config_file, "w") as open_file:
        json.dump(user_settings, open_file, indent=4)
        logging.debug(f"File {config_file} was written successfully")


def load_user_settings_from_file():
    data = None
    try:
        with open(config_file, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        logging.error(f"File not found: {config_file}.")
    except PermissionError:
        logging.error(f"Access Denied to file: {config_file}.")
    except IOError:
        logging.error(f"IO Error.")
    return data
