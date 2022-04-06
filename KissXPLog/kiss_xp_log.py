import hashlib
import json
import logging
import re
import threading
from functools import partial
from time import sleep

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, QRegExp, Qt, QDateTime, QDate, QTime
from PyQt5.QtWidgets import QAbstractItemView, QMenu, QAction, QFileDialog, QMessageBox

from KissXPLog import UserConfig, config
from KissXPLog.adif import parse_adif_for_data, band_to_frequency, \
    frequency_to_band
from KissXPLog.const_adif_fields import QSL_RCVD_ENUMERATION, QSL_SENT_ENUMERATION, MODES_WITH_SUBMODE, \
    BAND_WITH_FREQUENCY, CANTONS
from KissXPLog.dialog.config_dialog import ConfigDialog
from KissXPLog.file_operations import read_data_from_json_file, initial_file_dialog_config, generic_save_data_to_file
from KissXPLog.logger_gui import Ui_MainWindow
from KissXPLog.messages import show_error_message, show_info_message
from KissXPLog.qrz_lookup import get_dxcc_from_callsign, update_plist
from KissXPLog.qso_operations import are_minimum_qso_data_present, remove_empty_fields, add_new_information_to_qso_list, \
    prune_qsos
from KissXPLog.table_model import TableModel


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.cdw = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # MenuBarStuff
        self._createActions()
        self._createMenuBar()
        self._connectActions()
        self._createFullDevMenu()

        self.show()

        # Autosave Options
        self.autosave = False
        self.autosave_interval = 10
        self.last_autosaved_hash = None
        self.timed_autosave_thread = None

        self.table_is_editable = False
        self.data = []
        # Bool for New oder Update
        self.update_qso = False
        # Which row should be Updated
        self.row = None
        self._do_we_have_unsaved_changes = False

        self.all_dxcc = {}

        self.row_index = ['CALL', 'QSO_DATE', 'TIME_ON', 'FREQ', 'BAND', 'MODE', 'SUBMODE', 'RST_SENT', 'RST_RCVD',
                          'DXCC', 'COUNTRY', 'STATE', 'QSL_SENT', 'QSL_RCVD', 'QSLSDATE', 'EQSL_QSL_SENT',
                          'EQSL_QSL_RCVD',
                          'LOTW_QSL_SENT', 'LOTW_QSL_RCVD', 'NAME', 'NOTES']
        self.bands = BAND_WITH_FREQUENCY
        self.custom_fields_list = []

        self.modes = MODES_WITH_SUBMODE
        self.ui.cb_canton.setDisabled(True)

        # Load Config File
        self.user_config = UserConfig()
        self.load_user_settings()

        self.model = TableModel(self.data, self.row_index)
        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSourceModel(self.model)
        self.ui.tableView.setModel(self.proxyModel)

        self.ui.tableView.setSortingEnabled(True)
        self.ui.tableView.sortByColumn(-1, Qt.AscendingOrder)
        self.ui.tableView.setAlternatingRowColors(True)
        self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.ui.tableView.doubleClicked.connect(self.get_table_row_data)

        # Window Settings
        self.setWindowTitle("Kiss XP Log for QSO")
        # Anzeige von Text in Statusleiste Vorlage -> DEV
        self.ui.statusbar.showMessage("I'm the status bar - Hi, how are you? :)", 20000)

        # Fill in Comboboxes
        self.ui.cb_band.addItems(self.bands)
        self.ui.cb_mode.addItems(self.modes)
        self.ui.cbo_sent_options.addItems(QSL_SENT_ENUMERATION)
        self.ui.cbo_rcvd_options.addItems(QSL_RCVD_ENUMERATION)

        self.ui.bt_new.clicked.connect(self.clear_new_log_entry_form)
        self.ui.bt_save.clicked.connect(self.save_or_edit_handler)
        self.ui.le_filter.textChanged.connect(self.filter_for_table)

        self.ui.dateEdit.setMaximumDate(QDate.currentDate())
        self.ui.dateEdit.setCalendarPopup(True)

        # self.ui.de_qsl_sent_date.setDate(QDate.currentDate())
        self.ui.de_qsl_sent_date.setDisabled(True)

        # Filtern der Spalten mit Button
        currentQMenu = QMenu()
        for column in range(self.model.columnCount()):
            currentQAction = QAction(self.model.row_index[column], currentQMenu)
            currentQAction.setCheckable(True)
            currentQAction.setChecked(True)
            currentQAction.toggled.connect(partial(self.setColumnVisible, column))
            currentQMenu.addAction(currentQAction)
        self.ui.bt_column_filter.setMenu(currentQMenu)

        # Start Autosave if Conditions are given:
        self.start_timed_autosave_thread()

    def _createActions(self):
        # File Menu Actions
        self.configAction = QAction("Show Konfig Dialog", self)
        self.saveAction = QAction("&Save Table", self)
        self.loadAction = QAction("&Load Table", self)
        self.importAdifAction = QAction("&Import Adif", self)
        self.exportAdifAction = QAction("&Export Adif", self)
        self.exitAction = QAction("&Exit", self)
        # Edit Menu Actions
        self.newAction = QAction("&New", self)
        self.discardAction = QAction("&Discard", self)
        self.editTableAction = QAction("&Edit Table", self)
        self.getNewPlistAction = QAction("&Update Plist")

    def _createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.configAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.loadAction)
        fileMenu.addAction(self.importAdifAction)
        fileMenu.addAction(self.exportAdifAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.newAction)
        editMenu.addAction(self.discardAction)
        editMenu.addAction(self.editTableAction)
        editMenu.addAction(self.getNewPlistAction)

    def _connectActions(self):
        # UE: Make Timestamp and Country after Call
        self.ui.le_call.editingFinished.connect(self.new_dxcc_lookup_thread)
        # UE: Fill Freq from Band und Vice Versa
        self.ui.le_freq.textEdited.connect(self.set_band_from_frequency)
        self.ui.cb_band.currentIndexChanged.connect(self.set_frequency_from_band)
        # UE: fill in default values for RST (59/599)
        self.ui.cb_mode.currentIndexChanged.connect(self.set_default_rst)
        # Call should always be Uppercase
        self.ui.le_call.textChanged.connect(lambda: self.ui.le_call.setText(self.ui.le_call.text().upper()))
        # Enable Cantons if Country is Swiss
        self.ui.le_country.textChanged.connect(self.enable_canton_if_swiss)
        # Fill the Submodes from Mode select
        self.ui.cb_mode.currentIndexChanged.connect(self.fill_in_sub_modes)
        # Activate and set Sent Date to today if Card is Send
        self.ui.cbo_sent_options.currentIndexChanged.connect(self.activate_and_set_Date_if_sent)

        # Connect File actions
        self.configAction.triggered.connect(self.show_config_window)
        self.saveAction.triggered.connect(self.json_save_file_chooser)
        self.loadAction.triggered.connect(self.json_load_file_chooser)
        self.importAdifAction.triggered.connect(self.adif_load_file_chooser)
        self.exportAdifAction.triggered.connect(self.adif_save_file_chooser)
        self.exitAction.triggered.connect(self.close)
        # Connect Edit actions
        self.newAction.triggered.connect(self.clear_new_log_entry_form)
        self.discardAction.triggered.connect(self.reset_form)
        self.editTableAction.triggered.connect(self.edit_qso_table_switch)
        self.getNewPlistAction.triggered.connect(lambda: update_plist(config.plist_path))
        # Connect Help actions
        # self.helpContentAction.triggered.connect(self.helpContent)
        # self.aboutAction.triggered.connect(self.about)

    #New > Schliesse bisherige Table >> Save ja/nein, erstelle empty DB.
    #Open > Schliesse bisherige Table >> Save ja/nein, öffne neue DB.
    #Update > Füge Neue Daten zu bestehender DB hinzu.

    def _createFullDevMenu(self):
        self.new_dev_menu_method = QAction("Simple Thread", self)
        # self.devTimePrintAction = QAction("&Print with Timer", self)
        # self.devAutosaveAction = QAction("&Enable Autosave", self)
        self.dev_fill_up_fields_menu_method = QAction("AutoFill Fields", self)
        self.dev_new_file = QAction("New File", self)
        self.dev_open_file = QAction("Open File", self)
        self.dev_update_file = QAction("Update File", self)

        devMenu = self.menuBar().addMenu("&DEV")
        devMenu.addAction(self.new_dev_menu_method)
        devMenu.addAction(self.dev_fill_up_fields_menu_method)
        devMenu.addAction(self.dev_new_file)
        devMenu.addAction(self.dev_open_file)
        # devMenu.addAction(self.devTimePrintAction)
        # devMenu.addAction(self.devAutosaveAction)
        self.new_dev_menu_method.triggered.connect(self.new_thread_methoden_test)
        self.dev_fill_up_fields_menu_method.triggered.connect(self.dev_fill_all_fields)
        self.dev_new_file.triggered.connect(self.dev_new_menu_triggered)
        self.dev_open_file.triggered.connect(self.dev_open_file_menu_triggered)
        # self.devAutosaveAction.triggered.connect(self.start_timed_autosave_thread)
        # self.devTimePrintAction.triggered.connect(lambda: self.auto_timer_dev(10))

    def new_thread_methoden_test(self):
        t = threading.Thread(target=self.print_something_useful, daemon=True)
        print(f"Threads activ: {threading.enumerate()}")
        t.start()

    def print_something_useful(self):
        print("Something useful..")
        print(f"Threads activ: {threading.enumerate()}")
        sleep(10)
        self.ui.le_call.setText("Gogogo...")
        sleep(10)
        print("after Sleep..")

    def dev_fill_all_fields(self):
        self.ui.le_call.setText("HB9")
        self.new_dxcc_lookup_thread()
        self.ui.cb_mode.setCurrentIndex(self.ui.cb_mode.findText("CW"))
        self.ui.cb_band.setCurrentIndex(self.ui.cb_band.findText("80m"))
        self.ui.cbo_sent_options.setCurrentIndex(self.ui.cbo_sent_options.findText("Yes"))

    def dev_new_menu_triggered(self):
        self.close()
        self.__init__()

    def dev_open_file_menu_triggered(self):
        self.dev_new_menu_triggered()
        self.json_load_file_chooser()




    def set_do_we_have_unsaved_changes(self, do_we_have_unsaved_changes):
        # Todo clean Observer
        self._do_we_have_unsaved_changes = do_we_have_unsaved_changes
        if self.autosave:
            if self.autosave_interval == 0:
                self.autosave_to_file()

    def load_user_settings(self):
        logging.info(f"Loaded User Config.")
        self.autosave = self.user_config.user_settings.get('Autosave')
        if asave := self.user_config.user_settings.get('AutosaveIntervall'):
            self.autosave_interval = int(asave)
        if self.user_config.user_settings.get('MY_BANDS'):
            self.bands = self.user_config.user_settings.get('MY_BANDS')
        else:
            self.modes = MODES_WITH_SUBMODE
        if self.user_config.user_settings.get('MY_Modes'):
            self.modes = self.user_config.user_settings.get('MY_Modes')
        else:
            self.bands = BAND_WITH_FREQUENCY

    def show_config_window(self):
        self.cdw = ConfigDialog(self)
        self.cdw.show()

    def start_timed_autosave_thread(self):
        if self.timed_autosave_thread and self.autosave_interval:
            print(f"Threads activ: {threading.enumerate()}")
            logging.debug(f"Start Autosave Thread..")
            self.timed_autosave_thread = threading.Timer(self.autosave_interval, self.start_timed_autosave_thread)
            self.timed_autosave_thread.daemon = True
            self.timed_autosave_thread.start()
            self.autosave_to_file()
        else:
            logging.info("No Interval set for Autosave..")

    def stop_timed_autosave_thread(self):
        if self.timed_autosave_thread:
            logging.debug(f"Stopping Autosave Thread..")
            self.timed_autosave_thread.cancel()

    def autosave_to_file(self):
        if actual_table := self.model.get_data_from_table():
            data_md5 = hashlib.md5(json.dumps(actual_table, sort_keys=True).encode('utf-8')).hexdigest()
            if self.last_autosaved_hash != data_md5:
                logging.info(f"Saving Table...")
                self.last_autosaved_hash = data_md5
                generic_save_data_to_file("autosaved.json", self.model.get_data_from_table())
                self.set_do_we_have_unsaved_changes(False)
            else:
                logging.info(f"Nothing new to save..")
        else:
            logging.info("Table is empty...")

    def auto_timer_dev(self, wait_in_sec):
        threading.Timer(wait_in_sec, lambda: self.auto_timer_dev(wait_in_sec)).start()
        self.print_something_useful()

    def activate_and_set_Date_if_sent(self):
        if self.ui.cbo_sent_options.currentText() == 'Yes':
            self.ui.de_qsl_sent_date.setDisabled(False)
            # Only set Current Date if not already set..
            if self.ui.de_qsl_sent_date.date().toString("yyyyMMdd") == "20000101":
                self.ui.de_qsl_sent_date.setDate(QDate.currentDate())
        else:
            self.ui.de_qsl_sent_date.setDisabled(True)
            self.ui.de_qsl_sent_date.setDate(QDate.fromString("20000101", "yyyyMMdd"))

    def enable_canton_if_swiss(self):
        if self.ui.le_country.text() == 'Switzerland':
            self.ui.cb_canton.setDisabled(False)
            self.ui.cb_canton.addItems(CANTONS)
        else:
            self.ui.cb_canton.setDisabled(True)

    def fill_in_sub_modes(self):
        self.ui.cb_submodes.clear()
        selected_mode = self.ui.cb_mode.currentText()
        sub_mode = MODES_WITH_SUBMODE.get(selected_mode)
        if len(sub_mode) <= 1:
            self.ui.cb_submodes.setDisabled(True)
        else:
            self.ui.cb_submodes.setEnabled(True)
            self.ui.cb_submodes.addItems(sub_mode)

    def set_default_rst(self):
        if not self.ui.le_rst_sent.text():
            if not self.ui.le_rst_rcvd.text():
                if self.ui.cb_mode.currentText() == "CW":
                    self.ui.le_rst_sent.setText("599")
                    self.ui.le_rst_rcvd.setText("599")
                elif self.ui.cb_mode.currentText() == "SSB":
                    self.ui.le_rst_sent.setText("59")
                    self.ui.le_rst_rcvd.setText("59")

    def new_dxcc_lookup_thread(self):
        callsign = self.ui.le_call.text()
        t = threading.Thread(target=self.dxcc_lookup, args=(callsign,), daemon=True)
        t.start()

    def dxcc_lookup(self, callsign):
        try:
            all_dxcc = get_dxcc_from_callsign(callsign)
        except TypeError:
            show_error_message("No QRZ-info found",
                               f"Your callsign {callsign} is invalid and we cannot find any QRZ-info to it!")
            return
        self.set_time_after_callsign_enter()
        self.auto_enter_dxcc_infos_from_callsign(all_dxcc)

    def set_time_after_callsign_enter(self):
        # if time not changed, set to now:
        if self.ui.timeEdit.time().toString("HHmmss") == '000000':
            if self.ui.dateEdit.date().toString("yyyyMMdd") == '20000101':
                self.set_gui_date_and_time_to_now()

    def auto_enter_dxcc_infos_from_callsign(self, all_dxcc):
        # Improvement for better User experience
        if len(all_dxcc) > 0:
            if all_dxcc['Country']:
                if not self.ui.le_country.text():
                    self.ui.le_country.setText(all_dxcc['Country'])
            if all_dxcc['Continent']:
                if not self.ui.le_continent.text():
                    self.ui.le_continent.setText(all_dxcc['Continent'])
            if all_dxcc['ITUZone']:
                if not self.ui.le_itu.text():
                    self.ui.le_itu.setText(str(all_dxcc['ITUZone']))
            if all_dxcc['CQZone']:
                if not self.ui.le_cq.text():
                    self.ui.le_cq.setText(str(all_dxcc['CQZone']))

    def set_frequency_from_band(self):
        # check if freq is empty!
        if not self.ui.le_freq.text():
            if band := self.ui.cb_band.currentText():
                freq = band_to_frequency(band)
                self.ui.le_freq.setText(str(freq))

    def set_band_from_frequency(self):
        if not self.ui.cb_band.currentText():
            freq = self.ui.le_freq.text()
            self.ui.cb_band.setCurrentText(frequency_to_band(freq))

    def setColumnVisible(self, column, isChecked):
        if isChecked:
            self.ui.tableView.showColumn(column)
            logging.debug(f"Column {column} set to shown")
        else:
            self.ui.tableView.hideColumn(column)
            logging.debug(f"Column {column} set to hidden")

    def filter_for_table(self):
        text = self.ui.le_filter.text()
        self.proxyModel.setFilterKeyColumn(0)
        self.proxyModel.setFilterRegExp(QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))

    def set_gui_date_and_time_to_now(self):
        self.ui.timeEdit.setTime(QDateTime.currentDateTimeUtc().time())
        self.ui.dateEdit.setDate(QDateTime.currentDateTime().date())

    def edit_qso_table_switch(self):
        if self.model.get_data_from_table():
            if self.table_is_editable is False:
                self.table_is_editable = True
                show_info_message("Info", "Unlocking table...")
                logging.info("Unlocking table...")
                self.ui.tableView.setEditTriggers(QAbstractItemView.DoubleClicked)
                self.ui.tableView.setStyleSheet("QTableView{border : 1px solid red}")
            else:
                self.table_is_editable = False
                show_info_message("Info", "Locking table....")
                logging.info("Locking table....")
                self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.ui.tableView.setStyleSheet("QTableView{border : none}")
        else:
            logging.info("Table edit requested, but Table is empty.")
            show_error_message("Info", "Can not edit an empty table..")

    def get_dict_from_inputform(self):
        new_qso = {'CALL': self.ui.le_call.text(),
                   'QSO_DATE': self.ui.dateEdit.date().toString("yyyyMMdd"),
                   'TIME_ON': self.ui.timeEdit.time().toString("HHmmss"),
                   'MODE': self.ui.cb_mode.currentText(),
                   'SUBMODE': self.ui.cb_submodes.currentText(),

                   'RST_SENT': self.ui.le_rst_sent.text(),
                   'RST_RCVD': self.ui.le_rst_rcvd.text(),
                   'BAND': self.ui.cb_band.currentText(),
                   'FREQ': self.ui.le_freq.text(),
                   'NAME': self.ui.le_name.text(),
                   'NOTES': self.ui.te_notes.toPlainText(),
                   'COMMENT': self.ui.le_comment.text(),

                   'QSL_RCVD': QSL_RCVD_ENUMERATION.get(self.ui.cbo_rcvd_options.currentText())[0],
                   'QSL_SENT': QSL_SENT_ENUMERATION.get(self.ui.cbo_sent_options.currentText())[0],
                   'QSLSDATE': (
                       self.ui.de_qsl_sent_date.date().toString(
                           "yyyyMMdd") if self.ui.de_qsl_sent_date.isEnabled() else ''),

                   'EQSL_QSL_RCVD': True if self.ui.cb_eqsl_rcvd_new.isChecked() else '',
                   'EQSL_QSL_SENT': True if self.ui.cb_eqsl_sent_new.isChecked() else '',

                   'LOTW_QSL_RCVD': True if self.ui.cb_lotw_rcvd_new.isChecked() else '',
                   'LOTW_QSL_SENT': True if self.ui.cb_lotw_sent_new.isChecked() else '',

                   'COUNTRY': self.ui.le_country.text(),
                   'STATE': self.ui.cb_canton.currentText()
                   }
        return new_qso

    def save_new_log_entry(self):
        new_qso = self.get_dict_from_inputform()
        new_qso = remove_empty_fields(new_qso)
        if are_minimum_qso_data_present(new_qso):
            self.clear_new_log_entry_form()
            self.model.add_new_qso_method_two(new_qso)
            # self.model.add_new_qso_method_one(new_qso)
        else:
            # Todo Show Hint which fields needs to edit for a minimal qso.. (ggf roter Rahmen über felder oä)
            show_error_message("No Valid QSO", "Please fill in all the required fields.")

    def clear_new_log_entry_form(self):
        self.update_qso = False
        self.ui.le_call.clear()
        self.ui.cb_mode.setCurrentIndex(0)
        self.ui.cb_submodes.clear()
        self.ui.le_rst_sent.clear()
        self.ui.le_rst_rcvd.clear()
        self.ui.cb_band.setCurrentIndex(0)
        self.ui.le_freq.clear()
        self.ui.le_name.clear()
        self.ui.le_comment.clear()
        self.ui.te_notes.clear()
        self.ui.le_country.clear()
        self.ui.cb_canton.setCurrentIndex(0)
        self.ui.le_continent.clear()
        self.ui.le_cq.clear()
        self.ui.le_itu.clear()

        self.ui.cbo_rcvd_options.setCurrentIndex(0)
        self.ui.cbo_sent_options.setCurrentIndex(0)
        self.ui.de_qsl_sent_date.setDate(QDate.fromString("20000101", "yyyyMMdd"))

        self.ui.cb_eqsl_rcvd_new.setChecked(False)
        self.ui.cb_eqsl_sent_new.setChecked(False)

        self.ui.cb_lotw_rcvd_new.setChecked(False)
        self.ui.cb_lotw_sent_new.setChecked(False)

        self.ui.dateEdit.setDate(QDate.fromString("20000101", "yyyyMMdd"))
        self.ui.timeEdit.setTime(QTime.fromString('000000', "HHmmss"))

    # Switch verbergen/anzeigen von Tabellenspalte
    def hide_and_seek(self):
        if self.ui.tableView.horizontalHeader().isSectionHidden(0):
            logging.debug("Eckstein, Eckstein...")
            self.ui.tableView.horizontalHeader().showSection(0)
        else:
            logging.debug("..alles muss versteckt sein..")
            self.ui.tableView.horizontalHeader().hideSection(0)

    def reset_form(self):
        self.clear_new_log_entry_form()
        self.ui.tableView.sortByColumn(-1, Qt.AscendingOrder)

    def generic_load_file_to_table(self, filename):
        logging.debug("Load table from {} ...".format(filename))
        # file_extension = str(filename).strip().split(".", 1)[1]
        file_extension = str(filename).strip()
        file_extension = re.search('\w*$', file_extension).group(0)
        if file_extension == "json":
            loaded_data = read_data_from_json_file(filename)
        elif file_extension == "adif" or file_extension == "adi":
            loaded_data = parse_adif_for_data(filename)
        else:
            show_error_message("Error", f"Data Type is not supported: {file_extension}")
            return
        new_full_qso_list = add_new_information_to_qso_list(self.model.get_data_from_table(), loaded_data)
        new_clean_full_qso_list = prune_qsos(new_full_qso_list)
        self.model.add_new_qsos_list(new_clean_full_qso_list)

    def json_save_file_chooser(self):
        logging.debug("Open File Select for Save in JSON")
        filedialog = initial_file_dialog_config("json")
        filedialog.setWindowTitle('Choose location to save data as JSON')
        filedialog.setAcceptMode(QFileDialog.AcceptSave)
        if filedialog.exec_():
            filename = filedialog.selectedFiles()[0]
            logging.debug(f"JSON File will be saved to {filename}")
            generic_save_data_to_file(filename, self.model.get_data_from_table())
            return True

    def json_load_file_chooser(self):
        logging.debug("Open File Select for Load in JSON")
        filedialog = initial_file_dialog_config("json")
        filedialog.setWindowTitle('Choose JSON file to open')
        filedialog.setFileMode(QFileDialog.ExistingFile)
        filedialog.setAcceptMode(QFileDialog.AcceptOpen)
        if filedialog.exec_():
            filename = filedialog.selectedFiles()[0]
            logging.debug(f"JSON File {filename} will be loaded")
            self.generic_load_file_to_table(filename)

    def adif_save_file_chooser(self):
        logging.debug("Open File Select for Export in Adif")
        filedialog = initial_file_dialog_config("adi")
        filedialog.setWindowTitle('Choose location to save data as ADIF')
        filedialog.setAcceptMode(QFileDialog.AcceptSave)
        if filedialog.exec_():
            filename = filedialog.selectedFiles()[0]
            logging.debug(f"ADIF File {filename} will be exported")
            generic_save_data_to_file(filename, self.model.get_data_from_table(), self.custom_fields_list)
            self.set_do_we_have_unsaved_changes(False)

    def adif_load_file_chooser(self):
        logging.debug("Open File Select for Import in Adif")
        filedialog = initial_file_dialog_config("adi")
        filedialog.setWindowTitle('Choose ADIF file to open')
        filedialog.setFileMode(QFileDialog.ExistingFile)
        filedialog.setAcceptMode(QFileDialog.AcceptOpen)
        if filedialog.exec_():
            filename = filedialog.selectedFiles()[0]
            logging.debug(f"ADIF File {filename} will be imported")
            self.generic_load_file_to_table(filename)

    def get_table_row_data(self, index):
        self.clear_new_log_entry_form()
        # Get the Real Row bcs > Filtering and Sorting..
        new_row = self.proxyModel.mapToSource(index).row()
        edit_QSO_dict = self.model.get_data_row_from_table(new_row)
        self.update_qso = True
        self.row = new_row
        self.fill_values_to_edit_form(edit_QSO_dict)

    def save_or_edit_handler(self):
        # Called by SaveButton
        self.set_do_we_have_unsaved_changes(True)
        if self.update_qso:
            self.update_qso = False
            updated_qso = self.get_dict_from_inputform()
            updated_qso = remove_empty_fields(updated_qso)
            row = self.row
            self.model.update_single_qso(row, updated_qso)
            self.clear_new_log_entry_form()
        else:
            logging.info("Saving new Entry on row {}".format(self.row))
            self.save_new_log_entry()

    def fill_values_to_edit_form(self, edit_QSO_dict):
        self.ui.le_call.setText(edit_QSO_dict.get('CALL'))
        self.ui.dateEdit.setDate(QDate.fromString(edit_QSO_dict.get('QSO_DATE'), "yyyyMMdd"))
        self.ui.timeEdit.setTime(QTime.fromString(edit_QSO_dict.get('TIME_ON'), "HHmmss"))
        self.ui.cb_mode.setCurrentText(edit_QSO_dict.get('MODE'))
        self.ui.cb_submodes.setCurrentText(edit_QSO_dict.get('SUBMODE'))
        self.ui.le_rst_sent.setText(edit_QSO_dict.get('RST_SENT'))
        self.ui.le_rst_rcvd.setText(edit_QSO_dict.get('RST_RCVD'))
        self.ui.cb_band.setCurrentText(edit_QSO_dict.get('BAND').lower() if edit_QSO_dict.get('BAND') else "")
        self.ui.le_freq.setText(edit_QSO_dict.get('FREQ'))
        self.ui.le_name.setText(edit_QSO_dict.get('NAME'))
        self.ui.te_notes.setText(edit_QSO_dict.get('NOTES'))
        self.ui.le_comment.setText(edit_QSO_dict.get('COMMENT'))
        self.ui.de_qsl_sent_date.setDate(QDate.fromString(edit_QSO_dict.get('QSLSDATE'), "yyyyMMdd"))

        self.ui.le_country.setText(edit_QSO_dict.get('COUNTRY'))
        if self.ui.le_country.text() == 'Switzerland':
            self.ui.cb_canton.setCurrentText(edit_QSO_dict.get('STATE'))

        # QSL_RCVD = Key:'Y' >> Value:'YES'
        # Mappin from 'Y' to 'YES'
        for key, value in QSL_RCVD_ENUMERATION.items():
            if value[0] == edit_QSO_dict.get('QSL_RCVD'):
                self.ui.cbo_rcvd_options.setCurrentText(key)
                break

        for key, value in QSL_SENT_ENUMERATION.items():
            if value[0] == edit_QSO_dict.get('QSL_SENT'):
                self.ui.cbo_sent_options.setCurrentText(key)
                break

        self.ui.cb_eqsl_rcvd_new.setChecked(True if edit_QSO_dict.get('EQSL_QSL_RCVD') else False)
        self.ui.cb_eqsl_sent_new.setChecked(True if edit_QSO_dict.get('EQSL_QSL_SENT') else False)

        self.ui.cb_lotw_rcvd_new.setChecked(True if edit_QSO_dict.get('LOTW_QSL_RCVD') else False)
        self.ui.cb_lotw_sent_new.setChecked(True if edit_QSO_dict.get('LOTW_QSL_SENT') else False)

    def closeEvent(self, event):
        if self._do_we_have_unsaved_changes:
            reply = QMessageBox.question(self, 'Window Close', "Save Changes before Exit?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                if self.json_save_file_chooser():
                    event.accept()
                else:
                    event.ignore()

        # self.stop_timed_autosave_thread()
        print("Im Done with this...")
