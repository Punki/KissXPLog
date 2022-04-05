import json
import logging
import os

work_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(work_dir, "data")
config_file = os.path.join(data_dir, "config.json")
plist_path = os.path.join(data_dir, 'cty.plist')


class UserConfig:
    def __init__(self):
        self.user_settings = {}
        if os.path.exists(config_file):
            self.user_settings = self.load_user_settings_from_file()
        else:
            self.create_default_value_user_config()

    def create_default_value_user_config(self):
        if not self.user_settings:
            self.user_settings['Autosave'] = False
            self.user_settings['AutosaveIntervall'] = 10
            self.user_settings['MY_BANDS'] = None
            self.user_settings['MY_Modes'] = None
            self.user_settings['STATION_CALLSIGN'] = None
            self.user_settings['MY_CQ_ZONE'] = None
            self.user_settings['MY_ITU_ZONE'] = None

    def save_user_settings_to_file(self):
        with open(config_file, "w") as open_file:
            json.dump(self.user_settings, open_file, indent=4)
            logging.debug(f"File {config_file} was written successfully")

    def load_user_settings_from_file(self):
        data = {}
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
