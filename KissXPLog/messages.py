import logging

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


def logging_setup(logfile):
    """
    Sets up a basic logging environment. Per default, logs everything at DEBUG level
    Parameters
    ----------
    logfile : str
        Path to logfile where the logs should be written into

    Returns
    -------
    None
    """
    logging.basicConfig(
        filename=logfile,  # All logs are written into this logfile
        format='%(asctime)s: %(levelname)s - %(message)s',  # The formate is [datatimee]: [level] - [message]
        level=logging.DEBUG,  # Everything will be logged. Possible levels: DEBUG, INFO, WARN, ERROR, CRITICAL
        datefmt='%m/%d/%Y %H:%M:%S'  # datetime format: 03/26/2019 13:59:09
    )

def show_info_message(title, message):
    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec_()
    logging.info(message)


def show_error_message(title, message):
    err_box = QtWidgets.QMessageBox()
    err_box.setIcon(QMessageBox.Icon.Warning)
    err_box.setWindowTitle(title)
    err_box.setText(message)
    err_box.exec_()
    logging.error(message)