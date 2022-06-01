from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QDialogButtonBox, QListView, QFormLayout, QLabel, QDialog, QCheckBox, QAbstractItemView


class FilterDialog(QDialog):
    def __init__(self, title, message, all_items, set_checked_items, parent=None):
        super(FilterDialog, self).__init__(parent=parent)
        form = QFormLayout(self)
        form.addRow(QLabel(message))
        self.cb_select_all = QCheckBox("Select All", self)
        self.cb_select_all.clicked.connect(self.de_select_all)
        form.addRow(self.cb_select_all)
        self.listView = QListView(self)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        form.addRow(self.listView)
        model = QStandardItemModel(self.listView)
        self.setWindowTitle(title)
        for item in (item for item in all_items if item):
            standardItem = QStandardItem(item)
            standardItem.setCheckable(True)
            if item in set_checked_items:
                standardItem.setCheckState(True)
            model.appendRow(standardItem)
        self.listView.setModel(model)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        form.addRow(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def get_selected_items(self):
        selected = []
        model = self.listView.model()
        for index in range(model.rowCount()):
            if model.item(index).checkState():
                selected.append(model.item(index).text())
        return selected

    def de_select_all(self, event):
        model = self.listView.model()
        for index in range(model.rowCount()):
            model.item(index).setCheckState(event)


