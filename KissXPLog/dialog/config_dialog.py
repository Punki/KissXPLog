import logging

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog

from KissXPLog import user_settings, save_user_settings_to_file
from KissXPLog.const_adif_fields import MODES_WITH_SUBMODE, BAND_WITH_FREQUENCY
from KissXPLog.dialog.filter_dialog import FilterDialog
from KissXPLog.dialog.form import Ui_Widget
from KissXPLog.messages import show_error_message


# pyuic5 -x .\form.ui -o .\form.py


class ConfigDialog(QtWidgets.QWidget, Ui_Widget):
    def __init__(self, parent=None):
        super().__init__()
        self.ui2 = Ui_Widget()
        self.setup_ui = self.ui2.setupUi(self)
        self.other_class_handle = parent
        self.ui2.cb_autosave_interval.setMaximum(59)
        self.ui2.cb_autosave_interval.setMinimum(0)

        # Alle möglichen Werte
        self.modes = MODES_WITH_SUBMODE
        self.bands = BAND_WITH_FREQUENCY
        # Checked Werte von Main
        # Dict if none configfile was used, otherwise is a list.
        if type(self.other_class_handle.bands) is dict:
            self.checked_bands = list(self.other_class_handle.bands.keys())
        else:
            self.checked_bands = self.other_class_handle.bands
        if type(self.other_class_handle.modes) is dict:
            self.checked_modes = list(self.other_class_handle.modes.keys())
        else:
            self.checked_modes = self.other_class_handle.modes

        self.ui2.cb_autosave.setChecked(self.other_class_handle.autosave)
        self.ui2.cb_autosave_interval.setValue(self.other_class_handle.autosave_interval)

        # Connect Action to buttons
        self.ui2.pb_save.clicked.connect(self.save_config)
        self.ui2.pb_chancel.clicked.connect(self.close)
        self.ui2.pb_bands_filter.clicked.connect(self.show_bands_filter_dialog)
        self.ui2.pb_modes_filter.clicked.connect(self.show_modes_filter_dialog)

    def save_config(self):
        logging.debug(f"Save Configuration ...")
        # Save to File:
        user_settings['Autosave'] = self.ui2.cb_autosave.isChecked()
        user_settings['AutosaveIntervall'] = self.ui2.cb_autosave_interval.value()
        user_settings['MY_BANDS'] = self.checked_bands

        my_modes_with_sub = {}
        for mode in self.checked_modes:
            my_modes_with_sub[mode] = MODES_WITH_SUBMODE.get(mode)
        user_settings['MY_Modes'] = self.checked_modes
        save_user_settings_to_file()
        # Set Settings Live:
        self.other_class_handle.ui.cb_mode.clear()
        self.other_class_handle.ui.cb_mode.addItems(my_modes_with_sub)

        self.other_class_handle.ui.cb_band.clear()
        self.other_class_handle.ui.cb_band.addItems(self.checked_bands)
        if self.ui2.cb_autosave.isChecked():
            if self.ui2.cb_autosave_interval.value() < 0:
                show_error_message("Error", "Interval must be >= 0")
                return
            else:
                self.other_class_handle.autosave = self.ui2.cb_autosave.isChecked()
                self.other_class_handle.autosave_interval = self.ui2.cb_autosave_interval.value() * 60
                self.other_class_handle.start_timed_autosave_thread()
        self.close()

    def show_modes_filter_dialog(self):
        all_items = self.modes
        set_checked_items = self.checked_modes
        modefilterdialog = FilterDialog("Select Modes", "", all_items, set_checked_items, self)
        if modefilterdialog.exec_() == QDialog.Accepted:
            self.checked_modes = modefilterdialog.get_selected_items()
            self.checked_modes.insert(0, '')

    def show_bands_filter_dialog(self):
        all_items = self.bands
        set_checked_items = self.checked_bands
        modefilterdialog = FilterDialog("Select Bands", "", all_items, set_checked_items, self)
        if modefilterdialog.exec_() == QDialog.Accepted:
            self.checked_bands = modefilterdialog.get_selected_items()
            self.checked_bands.insert(0, '')
