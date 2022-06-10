import logging

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from KissXPLog.config import logfile_path


def logging_setup():
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
        filename=logfile_path,  # All logs are written into this logfile
        format='%(asctime)s: %(threadName)s - %(name)s - %(levelname)s - %(message)s',
        # The formate is [datatimee]: [threadname] - [name] - [level] - [message]
        datefmt='%Y/%m/%d %H:%M:%S'  # datetime format: 2019/03/26 13:59:09
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
