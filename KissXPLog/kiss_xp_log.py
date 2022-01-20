import logging
from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, QRegExp, Qt, QDateTime, QDate, QTime
from PyQt5.QtWidgets import QAbstractItemView, QMenu, QAction, QFileDialog

from KissXPLog.adif import qso_status_from_custom_to_adif_mapping, parse_adif_for_data
from KissXPLog.file_operations import read_data_from_json_file, initial_file_dialog_config, generic_save_data_to_file
from KissXPLog.logger_gui import Ui_MainWindow
from KissXPLog.messages import show_error_message, show_info_message
from KissXPLog.qso_operations import are_minimum_qso_data_present, remove_empty_fields, add_new_information_to_qso_list
from KissXPLog.table_model import TableModel


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.setup_ui = self.ui.setupUi(self)
        # MenuBarStuff
        self._createActions()
        self._createMenuBar()
        self._connectActions()

        self.show()

        self.table_is_editable = False
        self.data = []

        self.update_qso = False
        self.org_qso = None
        self.row = None

        self.row_index = ['CALL', 'QSO_DATE', 'TIME_ON', 'FREQ', 'BAND', 'MODE', 'RST_SENT', 'RST_RCVD', 'DXCC',
                          'COUNTRY', 'CARD_SENT', 'CARD_RCVD', 'EQSL_SENT', 'EQSL_RCVD', 'LOTW_SENT', 'LOTW_RCVD',
                          'NOTES']

        self.bands = ['', '160m', '80m', '40m', '30m', '20m', '17m', '15m', '12m', '10m']
        self.modes = ['', 'SSB', 'CW', 'FT8']
        self.custom_fields_list = ['CST_CARD_RCVD', 'CST_CARD_SENT', 'CST_CARD_REQUEST', 'CST_EQSL_RCVD',
                                   'CST_EQSL_SENT', 'CST_EQSL_REQUEST', 'CST_LOTW_RCVD', 'CST_LOTW_SENT',
                                   'CST_LOTW_REQUEST']

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
        self.ui.cb_band.addItems(self.bands)
        self.ui.cb_mode.addItems(self.modes)

        self.ui.bt_new.clicked.connect(self.clear_new_log_entry_form)
        self.ui.bt_save.clicked.connect(self.save_or_edit_handler)
        self.ui.le_filter.textChanged.connect(self.filter_for_table)

        # Filtern der Spalten mit Button
        currentQMenu = QMenu()
        for column in range(self.model.columnCount()):
            currentQAction = QAction(self.model.row_index[column], currentQMenu)
            currentQAction.setCheckable(True)
            currentQAction.setChecked(True)
            currentQAction.toggled.connect(partial(self.setColumnVisible, column))
            currentQMenu.addAction(currentQAction)
        self.ui.bt_column_filter.setMenu(currentQMenu)

    def _createActions(self):
        # File Menu Actions
        self.saveAction = QAction("&Save Table", self)
        self.loadAction = QAction("&Load Table", self)
        self.importAdifAction = QAction("&Import Adif", self)
        self.exportAdifAction = QAction("&Export Adif", self)
        self.exitAction = QAction("&Exit", self)
        # Edit Menu Actions
        self.newAction = QAction("&New", self)
        self.discardAction = QAction("&Discard", self)
        self.editTableAction = QAction("&Edit Table", self)
        # Help Menu Actions
        # self.helpContentAction = QAction("&Help Content", self)
        # self.aboutAction = QAction("&About", self)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
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

        # helpMenu = menuBar.addMenu("&Help")
        # helpMenu.addAction(self.helpContentAction)
        # helpMenu.addAction(self.aboutAction)

    def _connectActions(self):
        # Connect File actions
        self.saveAction.triggered.connect(self.json_save_file_chooser)
        self.loadAction.triggered.connect(self.json_load_file_chooser)
        self.importAdifAction.triggered.connect(self.adif_load_file_chooser)
        self.exportAdifAction.triggered.connect(self.adif_save_file_chooser)
        self.exitAction.triggered.connect(self.close)
        # Connect Edit actions
        self.newAction.triggered.connect(self.clear_new_log_entry_form)
        self.discardAction.triggered.connect(self.reset_form)
        self.editTableAction.triggered.connect(self.edit_qso_table_switch)
        # Connect Help actions
        # self.helpContentAction.triggered.connect(self.helpContent)
        # self.aboutAction.triggered.connect(self.about)

    def setColumnVisible(self, column, isChecked):
        if isChecked:
            self.ui.tableView.showColumn(column)
            logging.debug("Column {} set to shown".format(column))
        else:
            self.ui.tableView.hideColumn(column)
            logging.debug("Column {} set to hidden".format(column))

    def filter_for_table(self):
        text = self.ui.le_filter.text()
        self.proxyModel.setFilterKeyColumn(0)
        self.proxyModel.setFilterRegExp(QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))

    def update_date_and_time_for_new_qso(self):
        self.ui.timeEdit.setTime(QDateTime.currentDateTimeUtc().time())
        self.ui.dateEdit.setDate(QDateTime.currentDateTime().date())

    def edit_qso_table_switch(self):
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

    def get_dict_from_inputform(self):
        new_qso = {'CALL': self.ui.le_call.text(),
                   'QSO_DATE': self.ui.dateEdit.date().toString("yyyyMMdd"),
                   'TIME_ON': self.ui.timeEdit.time().toString("HHmmss"),
                   'MODE': self.ui.cb_mode.currentText(),
                   'RST_SENT': self.ui.le_rst_sent.text(),
                   'RST_RCVD': self.ui.le_rst_rcvd.text(),
                   'BAND': self.ui.cb_band.currentText(),
                   'FREQ': self.ui.le_freq.text(),
                   'NOTES': self.ui.te_notes.toPlainText(),

                   'CST_CARD_RCVD': self.ui.cb_card_rcvd.isChecked(),
                   'CST_CARD_SENT': self.ui.cb_card_sent.isChecked(),
                   'CST_CARD_REQUEST': self.ui.cb_card_request.isChecked(),

                   'CST_EQSL_RCVD': self.ui.cb_eqsl_rcvd.isChecked(),
                   'CST_EQSL_SENT': self.ui.cb_eqsl_sent.isChecked(),
                   'CST_EQSL_REQUEST': self.ui.cb_eqsl_request.isChecked(),

                   'CST_LOTW_RCVD': self.ui.cb_lotw_rcvd.isChecked(),
                   'CST_LOTW_SENT': self.ui.cb_lotw_sent.isChecked(),
                   'CST_LOTW_REQUEST': self.ui.cb_lotw_request.isChecked(),

                   'COUNTRY': self.ui.le_country.text()
                   }

        return new_qso

    def save_new_log_entry(self):
        new_qso = self.get_dict_from_inputform()
        new_qso = remove_empty_fields(new_qso)
        if are_minimum_qso_data_present(new_qso):
            self.clear_new_log_entry_form()
            qso_with_valid_adif_fields = qso_status_from_custom_to_adif_mapping(new_qso)
            self.model.add_new_qso_method_two(qso_with_valid_adif_fields)
            # self.model.add_new_qso_method_one(new_qso)
        else:
            # Todo Show Hint which fields needs to edit for a minimal qso.. (ggf roter Rahmen über felder oä)
            show_error_message("No Valid QSO", "Please fill in all the required fields.")

    def clear_new_log_entry_form(self):
        self.update_qso = False
        self.ui.le_call.clear()
        self.ui.cb_mode.setCurrentIndex(0)
        self.ui.le_rst_sent.clear()
        self.ui.le_rst_rcvd.clear()
        self.ui.cb_band.setCurrentIndex(0)
        self.ui.le_freq.clear()
        self.ui.te_notes.clear()
        self.ui.le_country.clear()
        self.ui.cb_card_rcvd.setChecked(False)
        self.ui.cb_card_sent.setChecked(False)
        self.ui.cb_card_request.setChecked(False)
        self.ui.cb_eqsl_rcvd.setChecked(False)
        self.ui.cb_eqsl_sent.setChecked(False)
        self.ui.cb_eqsl_request.setChecked(False)
        self.ui.cb_lotw_rcvd.setChecked(False)
        self.ui.cb_lotw_sent.setChecked(False)
        self.ui.cb_lotw_request.setChecked(False)
        self.update_date_and_time_for_new_qso()

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
        file_extension = str(filename).strip().split(".", 1)[1]
        if file_extension == "json":
            loaded_data = read_data_from_json_file(filename)
        elif file_extension == "adif" or file_extension == "adi":
            loaded_data = parse_adif_for_data(filename)
        else:
            show_error_message("Error", f"Data Type is not supported: {file_extension}")
            return
        new_full_qso_list = add_new_information_to_qso_list(self.model.get_data_from_table(), loaded_data)
        self.model.add_new_qsos_list(new_full_qso_list)

    def json_save_file_chooser(self):
        logging.debug("Open File Select for Save in JSON")
        filedialog = initial_file_dialog_config("json")
        filedialog.setWindowTitle('Choose location to save data as JSON')
        filedialog.setAcceptMode(QFileDialog.AcceptSave)
        if filedialog.exec_():
            filename = filedialog.selectedFiles()[0]
            logging.debug(f"JSON File will be saved to {filename}")
            generic_save_data_to_file(filename, self.model.get_data_from_table())

    def json_load_file_chooser(self):
        logging.debug("Open File Select for Load in JSON")
        filedialog = initial_file_dialog_config("json")
        filedialog.setWindowTitle('Choose JSON file to open')
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

    def adif_load_file_chooser(self):
        logging.debug("Open File Select for Import in Adif")
        filedialog = initial_file_dialog_config("adi")
        filedialog.setWindowTitle('Choose ADIF file to open')
        filedialog.setAcceptMode(QFileDialog.AcceptOpen)
        if filedialog.exec_():
            filename = filedialog.selectedFiles()[0]
            logging.debug(f"ADIF File {filename} will be imported")
            self.generic_load_file_to_table(filename)

    def get_table_row_data(self, index):
        # Get the Real Row bcs > Filtering and Sorting..
        new_row = self.proxyModel.mapToSource(index).row()
        edit_QSO_dict = self.model.get_data_row_from_table(new_row)
        self.update_qso = True
        self.org_qso = edit_QSO_dict
        self.row = new_row
        self.fill_values_to_edit_form(edit_QSO_dict)

    def save_or_edit_handler(self):
        if self.update_qso:
            self.update_qso = False
            updated_qso = self.get_dict_from_inputform()
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
        self.ui.le_rst_sent.setText(edit_QSO_dict.get('RST_SENT'))
        self.ui.le_rst_rcvd.setText(edit_QSO_dict.get('RST_RCVD'))
        self.ui.cb_band.setCurrentText(edit_QSO_dict.get('BAND'))
        self.ui.le_freq.setText(edit_QSO_dict.get('FREQ'))
        self.ui.te_notes.setText(edit_QSO_dict.get('NOTES'))
        self.ui.le_country.setText(edit_QSO_dict.get('COUNTRY'))

        self.ui.cb_card_rcvd.setChecked(True if edit_QSO_dict.get('CST_CARD_RCVD') else False)
        self.ui.cb_card_sent.setChecked(True if edit_QSO_dict.get('CST_CARD_SENT') else False)
        self.ui.cb_card_request.setChecked(True if edit_QSO_dict.get('CST_CARD_REQUEST') else False)
        self.ui.cb_eqsl_rcvd.setChecked(True if edit_QSO_dict.get('CST_EQSL_RCVD') else False)
        self.ui.cb_eqsl_sent.setChecked(True if edit_QSO_dict.get('CST_EQSL_SENT') else False)
        self.ui.cb_eqsl_request.setChecked(True if edit_QSO_dict.get('CST_EQSL_REQUEST') else False)
        self.ui.cb_lotw_rcvd.setChecked(True if edit_QSO_dict.get('CST_LOTW_RCVD') else False)
        self.ui.cb_lotw_sent.setChecked(True if edit_QSO_dict.get('CST_LOTW_SENT') else False)
        self.ui.cb_lotw_request.setChecked(True if edit_QSO_dict.get('CST_LOTW_REQUEST') else False)

    def update_qso_status(self):
        self.update_qso = False
        self.org_qso = None
        self.row = None
