# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logger_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(726, 625)
        MainWindow.setMinimumSize(QtCore.QSize(726, 625))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(7, 7, 7, 7)
        self.gridLayout.setObjectName("gridLayout")
        self.le_name = QtWidgets.QLineEdit(self.centralwidget)
        self.le_name.setMinimumSize(QtCore.QSize(0, 22))
        self.le_name.setMaximumSize(QtCore.QSize(150, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.le_name.setFont(font)
        self.le_name.setObjectName("le_name")
        self.gridLayout.addWidget(self.le_name, 4, 2, 1, 2)
        self.lb_date = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_date.sizePolicy().hasHeightForWidth())
        self.lb_date.setSizePolicy(sizePolicy)
        self.lb_date.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_date.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_date.setFont(font)
        self.lb_date.setObjectName("lb_date")
        self.gridLayout.addWidget(self.lb_date, 0, 5, 1, 1)
        self.bt_new = QtWidgets.QPushButton(self.centralwidget)
        self.bt_new.setMinimumSize(QtCore.QSize(0, 22))
        self.bt_new.setMaximumSize(QtCore.QSize(16777215, 22))
        self.bt_new.setObjectName("bt_new")
        self.gridLayout.addWidget(self.bt_new, 3, 11, 1, 1)
        self.le_filter = QtWidgets.QLineEdit(self.centralwidget)
        self.le_filter.setMinimumSize(QtCore.QSize(150, 22))
        self.le_filter.setMaximumSize(QtCore.QSize(150, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.le_filter.setFont(font)
        self.le_filter.setObjectName("le_filter")
        self.gridLayout.addWidget(self.le_filter, 13, 2, 1, 2)
        self.lb_freq = QtWidgets.QLabel(self.centralwidget)
        self.lb_freq.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_freq.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_freq.setFont(font)
        self.lb_freq.setObjectName("lb_freq")
        self.gridLayout.addWidget(self.lb_freq, 5, 8, 1, 1)
        self.cb_mode = QtWidgets.QComboBox(self.centralwidget)
        self.cb_mode.setMinimumSize(QtCore.QSize(0, 22))
        self.cb_mode.setMaximumSize(QtCore.QSize(125, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.cb_mode.setFont(font)
        self.cb_mode.setObjectName("cb_mode")
        self.gridLayout.addWidget(self.cb_mode, 8, 6, 1, 3)
        self.lb_rst_rcvd = QtWidgets.QLabel(self.centralwidget)
        self.lb_rst_rcvd.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_rst_rcvd.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_rst_rcvd.setFont(font)
        self.lb_rst_rcvd.setObjectName("lb_rst_rcvd")
        self.gridLayout.addWidget(self.lb_rst_rcvd, 7, 5, 1, 1)
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setMinimumSize(QtCore.QSize(0, 22))
        self.timeEdit.setMaximumSize(QtCore.QSize(60, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.timeEdit.setFont(font)
        self.timeEdit.setObjectName("timeEdit")
        self.gridLayout.addWidget(self.timeEdit, 3, 6, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(13, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 12, 1, 1)
        self.lb_rst_sent = QtWidgets.QLabel(self.centralwidget)
        self.lb_rst_sent.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_rst_sent.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_rst_sent.setFont(font)
        self.lb_rst_sent.setObjectName("lb_rst_sent")
        self.gridLayout.addWidget(self.lb_rst_sent, 5, 5, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.formLayout.setVerticalSpacing(4)
        self.formLayout.setObjectName("formLayout")
        self.lb_comment = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_comment.sizePolicy().hasHeightForWidth())
        self.lb_comment.setSizePolicy(sizePolicy)
        self.lb_comment.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_comment.setMaximumSize(QtCore.QSize(60, 22))
        self.lb_comment.setObjectName("lb_comment")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lb_comment)
        self.le_comment = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_comment.sizePolicy().hasHeightForWidth())
        self.le_comment.setSizePolicy(sizePolicy)
        self.le_comment.setMinimumSize(QtCore.QSize(0, 22))
        self.le_comment.setMaximumSize(QtCore.QSize(500, 22))
        self.le_comment.setObjectName("le_comment")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_comment)
        self.te_notes = QtWidgets.QTextEdit(self.centralwidget)
        self.te_notes.setMaximumSize(QtCore.QSize(500, 100))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.te_notes.setFont(font)
        self.te_notes.setObjectName("te_notes")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.te_notes)
        self.lb_notes = QtWidgets.QLabel(self.centralwidget)
        self.lb_notes.setMinimumSize(QtCore.QSize(46, 100))
        self.lb_notes.setMaximumSize(QtCore.QSize(46, 100))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_notes.setFont(font)
        self.lb_notes.setObjectName("lb_notes")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lb_notes)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(2, QtWidgets.QFormLayout.FieldRole, spacerItem1)
        self.gridLayout.addLayout(self.formLayout, 12, 1, 1, 4)
        self.lb_name = QtWidgets.QLabel(self.centralwidget)
        self.lb_name.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_name.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_name.setFont(font)
        self.lb_name.setObjectName("lb_name")
        self.gridLayout.addWidget(self.lb_name, 4, 1, 1, 1)
        self.le_rst_rcvd = QtWidgets.QLineEdit(self.centralwidget)
        self.le_rst_rcvd.setMinimumSize(QtCore.QSize(0, 22))
        self.le_rst_rcvd.setMaximumSize(QtCore.QSize(80, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.le_rst_rcvd.setFont(font)
        self.le_rst_rcvd.setObjectName("le_rst_rcvd")
        self.gridLayout.addWidget(self.le_rst_rcvd, 7, 6, 1, 1)
        self.lb_call = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_call.sizePolicy().hasHeightForWidth())
        self.lb_call.setSizePolicy(sizePolicy)
        self.lb_call.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_call.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_call.setFont(font)
        self.lb_call.setObjectName("lb_call")
        self.gridLayout.addWidget(self.lb_call, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(13, 115, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 12, 12, 1, 1)
        self.cb_band = QtWidgets.QComboBox(self.centralwidget)
        self.cb_band.setMinimumSize(QtCore.QSize(0, 22))
        self.cb_band.setMaximumSize(QtCore.QSize(70, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.cb_band.setFont(font)
        self.cb_band.setObjectName("cb_band")
        self.gridLayout.addWidget(self.cb_band, 4, 9, 1, 1)
        self.le_country = QtWidgets.QLineEdit(self.centralwidget)
        self.le_country.setMinimumSize(QtCore.QSize(0, 22))
        self.le_country.setMaximumSize(QtCore.QSize(150, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.le_country.setFont(font)
        self.le_country.setObjectName("le_country")
        self.gridLayout.addWidget(self.le_country, 7, 2, 1, 2)
        self.lb_county = QtWidgets.QLabel(self.centralwidget)
        self.lb_county.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_county.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_county.setFont(font)
        self.lb_county.setObjectName("lb_county")
        self.gridLayout.addWidget(self.lb_county, 7, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(13, 19, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 5, 4, 1, 1)
        self.lb_mode = QtWidgets.QLabel(self.centralwidget)
        self.lb_mode.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_mode.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_mode.setFont(font)
        self.lb_mode.setObjectName("lb_mode")
        self.gridLayout.addWidget(self.lb_mode, 8, 5, 1, 1)
        self.cb_submodes = QtWidgets.QComboBox(self.centralwidget)
        self.cb_submodes.setMinimumSize(QtCore.QSize(0, 22))
        self.cb_submodes.setMaximumSize(QtCore.QSize(125, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.cb_submodes.setFont(font)
        self.cb_submodes.setObjectName("cb_submodes")
        self.gridLayout.addWidget(self.cb_submodes, 9, 6, 1, 3)
        self.le_call = QtWidgets.QLineEdit(self.centralwidget)
        self.le_call.setMinimumSize(QtCore.QSize(0, 22))
        self.le_call.setMaximumSize(QtCore.QSize(150, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.le_call.setFont(font)
        self.le_call.setInputMethodHints(QtCore.Qt.ImhUppercaseOnly)
        self.le_call.setObjectName("le_call")
        self.gridLayout.addWidget(self.le_call, 0, 2, 1, 2)
        self.lb_submodes = QtWidgets.QLabel(self.centralwidget)
        self.lb_submodes.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_submodes.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_submodes.setFont(font)
        self.lb_submodes.setObjectName("lb_submodes")
        self.gridLayout.addWidget(self.lb_submodes, 9, 5, 1, 1)
        self.lb_filter = QtWidgets.QLabel(self.centralwidget)
        self.lb_filter.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_filter.setMaximumSize(QtCore.QSize(46, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_filter.setFont(font)
        self.lb_filter.setObjectName("lb_filter")
        self.gridLayout.addWidget(self.lb_filter, 13, 1, 1, 1)
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setEnabled(True)
        self.dateEdit.setMinimumSize(QtCore.QSize(90, 22))
        self.dateEdit.setMaximumSize(QtCore.QSize(90, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.dateEdit.setFont(font)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 0, 6, 1, 2)
        self.le_rst_sent = QtWidgets.QLineEdit(self.centralwidget)
        self.le_rst_sent.setMinimumSize(QtCore.QSize(0, 22))
        self.le_rst_sent.setMaximumSize(QtCore.QSize(80, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.le_rst_sent.setFont(font)
        self.le_rst_sent.setObjectName("le_rst_sent")
        self.gridLayout.addWidget(self.le_rst_sent, 5, 6, 1, 1)
        self.lb_canton = QtWidgets.QLabel(self.centralwidget)
        self.lb_canton.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_canton.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_canton.setFont(font)
        self.lb_canton.setObjectName("lb_canton")
        self.gridLayout.addWidget(self.lb_canton, 8, 1, 1, 1)
        self.bt_save = QtWidgets.QPushButton(self.centralwidget)
        self.bt_save.setMinimumSize(QtCore.QSize(0, 22))
        self.bt_save.setMaximumSize(QtCore.QSize(16777215, 22))
        self.bt_save.setObjectName("bt_save")
        self.gridLayout.addWidget(self.bt_save, 0, 11, 1, 1)
        self.cb_canton = QtWidgets.QComboBox(self.centralwidget)
        self.cb_canton.setMinimumSize(QtCore.QSize(0, 22))
        self.cb_canton.setMaximumSize(QtCore.QSize(150, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.cb_canton.setFont(font)
        self.cb_canton.setObjectName("cb_canton")
        self.gridLayout.addWidget(self.cb_canton, 8, 2, 1, 2)
        self.bt_column_filter = QtWidgets.QPushButton(self.centralwidget)
        self.bt_column_filter.setMinimumSize(QtCore.QSize(0, 22))
        self.bt_column_filter.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.bt_column_filter.setFont(font)
        self.bt_column_filter.setObjectName("bt_column_filter")
        self.gridLayout.addWidget(self.bt_column_filter, 13, 5, 1, 1)
        self.lb_utc = QtWidgets.QLabel(self.centralwidget)
        self.lb_utc.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_utc.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_utc.setFont(font)
        self.lb_utc.setObjectName("lb_utc")
        self.gridLayout.addWidget(self.lb_utc, 3, 5, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(13, 19, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 0, 1, 1)
        self.lb_band = QtWidgets.QLabel(self.centralwidget)
        self.lb_band.setMinimumSize(QtCore.QSize(0, 22))
        self.lb_band.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_band.setFont(font)
        self.lb_band.setObjectName("lb_band")
        self.gridLayout.addWidget(self.lb_band, 4, 8, 1, 1)
        self.le_freq = QtWidgets.QLineEdit(self.centralwidget)
        self.le_freq.setMinimumSize(QtCore.QSize(0, 22))
        self.le_freq.setMaximumSize(QtCore.QSize(70, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.le_freq.setFont(font)
        self.le_freq.setObjectName("le_freq")
        self.gridLayout.addWidget(self.le_freq, 5, 9, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gp_eqsl = QtWidgets.QGroupBox(self.centralwidget)
        self.gp_eqsl.setObjectName("gp_eqsl")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.gp_eqsl)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cb_eqsl_rcvd_new = QtWidgets.QCheckBox(self.gp_eqsl)
        self.cb_eqsl_rcvd_new.setMinimumSize(QtCore.QSize(45, 22))
        self.cb_eqsl_rcvd_new.setMaximumSize(QtCore.QSize(45, 22))
        self.cb_eqsl_rcvd_new.setObjectName("cb_eqsl_rcvd_new")
        self.horizontalLayout_2.addWidget(self.cb_eqsl_rcvd_new)
        self.cb_eqsl_sent_new = QtWidgets.QCheckBox(self.gp_eqsl)
        self.cb_eqsl_sent_new.setMinimumSize(QtCore.QSize(45, 22))
        self.cb_eqsl_sent_new.setMaximumSize(QtCore.QSize(45, 22))
        self.cb_eqsl_sent_new.setObjectName("cb_eqsl_sent_new")
        self.horizontalLayout_2.addWidget(self.cb_eqsl_sent_new)
        self.gridLayout_3.addWidget(self.gp_eqsl, 1, 0, 1, 1)
        self.gb_lotw = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_lotw.setObjectName("gb_lotw")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.gb_lotw)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cb_lotw_rcvd_new = QtWidgets.QCheckBox(self.gb_lotw)
        self.cb_lotw_rcvd_new.setMinimumSize(QtCore.QSize(45, 22))
        self.cb_lotw_rcvd_new.setMaximumSize(QtCore.QSize(45, 22))
        self.cb_lotw_rcvd_new.setObjectName("cb_lotw_rcvd_new")
        self.horizontalLayout_3.addWidget(self.cb_lotw_rcvd_new)
        self.cb_lotw_sent_new = QtWidgets.QCheckBox(self.gb_lotw)
        self.cb_lotw_sent_new.setMinimumSize(QtCore.QSize(45, 22))
        self.cb_lotw_sent_new.setMaximumSize(QtCore.QSize(45, 22))
        self.cb_lotw_sent_new.setObjectName("cb_lotw_sent_new")
        self.horizontalLayout_3.addWidget(self.cb_lotw_sent_new)
        self.gridLayout_3.addWidget(self.gb_lotw, 1, 1, 1, 1)
        self.gb_card = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_card.setMinimumSize(QtCore.QSize(0, 80))
        self.gb_card.setMaximumSize(QtCore.QSize(16777215, 80))
        self.gb_card.setObjectName("gb_card")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gb_card)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cbo_rcvd_options = QtWidgets.QComboBox(self.gb_card)
        self.cbo_rcvd_options.setMinimumSize(QtCore.QSize(90, 22))
        self.cbo_rcvd_options.setMaximumSize(QtCore.QSize(80, 22))
        self.cbo_rcvd_options.setObjectName("cbo_rcvd_options")
        self.gridLayout_2.addWidget(self.cbo_rcvd_options, 0, 4, 1, 1)
        self.lb_qsl_rcvd = QtWidgets.QLabel(self.gb_card)
        self.lb_qsl_rcvd.setObjectName("lb_qsl_rcvd")
        self.gridLayout_2.addWidget(self.lb_qsl_rcvd, 0, 3, 1, 1)
        self.lb_qsl_sent = QtWidgets.QLabel(self.gb_card)
        self.lb_qsl_sent.setObjectName("lb_qsl_sent")
        self.gridLayout_2.addWidget(self.lb_qsl_sent, 0, 0, 1, 1)
        self.cbo_sent_options = QtWidgets.QComboBox(self.gb_card)
        self.cbo_sent_options.setMinimumSize(QtCore.QSize(90, 22))
        self.cbo_sent_options.setMaximumSize(QtCore.QSize(80, 22))
        self.cbo_sent_options.setObjectName("cbo_sent_options")
        self.gridLayout_2.addWidget(self.cbo_sent_options, 0, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 0, 2, 1, 1)
        self.gridLayout_3.addWidget(self.gb_card, 0, 0, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_3, 12, 6, 1, 6)
        self.lb_continent = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_continent.setFont(font)
        self.lb_continent.setObjectName("lb_continent")
        self.gridLayout.addWidget(self.lb_continent, 5, 1, 1, 1)
        self.le_continent = QtWidgets.QLineEdit(self.centralwidget)
        self.le_continent.setMinimumSize(QtCore.QSize(0, 22))
        self.le_continent.setMaximumSize(QtCore.QSize(150, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.le_continent.setFont(font)
        self.le_continent.setObjectName("le_continent")
        self.gridLayout.addWidget(self.le_continent, 5, 2, 1, 1)
        self.lb_cq = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_cq.setFont(font)
        self.lb_cq.setObjectName("lb_cq")
        self.gridLayout.addWidget(self.lb_cq, 9, 1, 1, 1)
        self.lb_itu = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lb_itu.setFont(font)
        self.lb_itu.setObjectName("lb_itu")
        self.gridLayout.addWidget(self.lb_itu, 10, 1, 1, 1)
        self.le_cq = QtWidgets.QLineEdit(self.centralwidget)
        self.le_cq.setMinimumSize(QtCore.QSize(0, 22))
        self.le_cq.setMaximumSize(QtCore.QSize(150, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.le_cq.setFont(font)
        self.le_cq.setObjectName("le_cq")
        self.gridLayout.addWidget(self.le_cq, 9, 2, 1, 1)
        self.le_itu = QtWidgets.QLineEdit(self.centralwidget)
        self.le_itu.setMinimumSize(QtCore.QSize(0, 22))
        self.le_itu.setMaximumSize(QtCore.QSize(150, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.le_itu.setFont(font)
        self.le_itu.setObjectName("le_itu")
        self.gridLayout.addWidget(self.le_itu, 10, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setMinimumSize(QtCore.QSize(0, 0))
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 726, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.le_call, self.dateEdit)
        MainWindow.setTabOrder(self.dateEdit, self.timeEdit)
        MainWindow.setTabOrder(self.timeEdit, self.cb_band)
        MainWindow.setTabOrder(self.cb_band, self.le_freq)
        MainWindow.setTabOrder(self.le_freq, self.le_rst_sent)
        MainWindow.setTabOrder(self.le_rst_sent, self.le_rst_rcvd)
        MainWindow.setTabOrder(self.le_rst_rcvd, self.tableView)
        MainWindow.setTabOrder(self.tableView, self.bt_column_filter)
        MainWindow.setTabOrder(self.bt_column_filter, self.bt_save)
        MainWindow.setTabOrder(self.bt_save, self.bt_new)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lb_date.setText(_translate("MainWindow", "Date:"))
        self.bt_new.setText(_translate("MainWindow", "Clear"))
        self.lb_freq.setText(_translate("MainWindow", "Freq (MHz):"))
        self.lb_rst_rcvd.setText(_translate("MainWindow", "RST RCVD:"))
        self.lb_rst_sent.setText(_translate("MainWindow", "RST Sent:"))
        self.lb_comment.setText(_translate("MainWindow", "Comment:"))
        self.lb_notes.setText(_translate("MainWindow", "Notes:"))
        self.lb_name.setText(_translate("MainWindow", "Name:"))
        self.lb_call.setText(_translate("MainWindow", "Callsign:"))
        self.lb_county.setText(_translate("MainWindow", "Country:"))
        self.lb_mode.setText(_translate("MainWindow", "Mode:"))
        self.lb_submodes.setText(_translate("MainWindow", "SubModes"))
        self.lb_filter.setText(_translate("MainWindow", "Filter:"))
        self.lb_canton.setText(_translate("MainWindow", "Canton:"))
        self.bt_save.setText(_translate("MainWindow", "Save"))
        self.bt_column_filter.setText(_translate("MainWindow", "Column Filter"))
        self.lb_utc.setText(_translate("MainWindow", "UTC:"))
        self.lb_band.setText(_translate("MainWindow", "Band:"))
        self.gp_eqsl.setTitle(_translate("MainWindow", "Eqsl"))
        self.cb_eqsl_rcvd_new.setText(_translate("MainWindow", "Rcvd"))
        self.cb_eqsl_sent_new.setText(_translate("MainWindow", "Sent"))
        self.gb_lotw.setTitle(_translate("MainWindow", "Lotw"))
        self.cb_lotw_rcvd_new.setText(_translate("MainWindow", "Rcvd"))
        self.cb_lotw_sent_new.setText(_translate("MainWindow", "Sent"))
        self.gb_card.setTitle(_translate("MainWindow", "Card"))
        self.lb_qsl_rcvd.setText(_translate("MainWindow", "Rcvd:"))
        self.lb_qsl_sent.setText(_translate("MainWindow", "Sent:"))
        self.lb_continent.setText(_translate("MainWindow", "Continent:"))
        self.lb_cq.setText(_translate("MainWindow", "CQ-Zone:"))
        self.lb_itu.setText(_translate("MainWindow", "ITU Zone"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
