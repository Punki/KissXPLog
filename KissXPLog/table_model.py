import logging

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTime, QDate


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, input_data, table_head_names):
        super(TableModel, self).__init__()
        self._data = input_data
        # print("Data: ", self._data)
        # row_index accessible with []
        self.row_index = table_head_names

    def data(self, index, role=None):
        if role == Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.isValid():
                # Assign Values to Header (not always are all data present in source.)
                # Format Date and Time for View
                if self.row_index[index.column()] == 'QSO_DATE':
                    raw_format_date = self._data[index.row()].get(self.row_index[index.column()])
                    return QDate.fromString(raw_format_date, "yyyyMMdd")
                elif self.row_index[index.column()] == 'TIME_ON':
                    raw_format_time = self._data[index.row()].get(self.row_index[index.column()])
                    # return QTime.fromString(raw_format_time, "HHmmss").toString("HH:mm")
                    return QTime.fromString(raw_format_time, "HHmmss")

                return self._data[index.row()].get(self.row_index[index.column()])
            else:
                logging.error("Too Big", index.column())
                return None

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    # Need for Edit..
    def setData(self, index, new_item_value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            item_name = self.row_index[index.column()]
            if item_name == 'QSO_DATE':
                new_item_value = new_item_value.toString("yyyyMMdd")
            if item_name == 'TIME_ON':
                new_item_value = new_item_value.toString("HHmmss")
            new_item = {item_name: new_item_value}
            # print("New QSO: ", item_name, ": ", new_item)
            self._data[index.row()].update(new_item)
            # print('newListWithItem:', self._data[index.row()])
            self.dataChanged.emit(index, index)
            return True
        return QtCore.QAbstractTableModel.setData(self, index, new_item_value, role)

    # ADD new QSO method1
    def add_new_qso_method_one(self, new_qso):
        self.beginResetModel()
        self._data.append(new_qso)
        self.endResetModel()

    # ADD new QSO method2
    def add_new_qso_method_two(self, qso):
        self.layoutAboutToBeChanged.emit()
        self._data.append(qso)
        self.layoutChanged.emit()

    # List with multiple Dicts
    def extend_multiple_qsos(self, qsos):
        self.layoutAboutToBeChanged.emit()
        self._data.extend(qsos)
        self.layoutChanged.emit()

    # Switch List Complete
    def add_new_qsos_list(self, qsos):
        self.layoutAboutToBeChanged.emit()
        self._data = qsos
        self.layoutChanged.emit()

    # Update Single QSO
    def update_single_qso(self, row, qso):
        logging.debug("Updating...")
        # print("Bevor Update: ", self._data[row])
        self.layoutAboutToBeChanged.emit()
        self._data[row].update(qso)
        self.layoutChanged.emit()
        # print("After Update: ", self._data[row])

    # Zeile
    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self._data)

    # Spalten
    def columnCount(self, index=QtCore.QModelIndex()):
        return len(self.row_index)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        # section is the index of the column/row.
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            try:
                return self.row_index[section]
            except (IndexError,):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                return section
            except (IndexError,):
                return QtCore.QVariant()

    # def sort(self, index, order=QtCore.Qt.AscendingOrder):
    #     self.layoutAboutToBeChanged.emit()
    #     # get the header for sorting
    #     key = self.row_index[index]
    #     # sorting, if value is None then use ""
    #     self._data = sorted(self._data, key=lambda my_dict: my_dict.get(key, ""))
    #     if order == Qt.DescendingOrder:
    #         self._data.reverse()
    #     self.layoutChanged.emit()

    def get_data_from_table(self):
        data_copy = self._data.copy()
        return data_copy

    def get_data_row_from_table(self, row):
        return self._data[row]
