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


def set_log_level(logging_level):
    print("Log level switched to: ", logging_level)
    # set Logging Level
    if logging_level == "NOSET":
        logging.getLogger().setLevel(logging.NOTSET)
    elif logging_level == "DEBUG":
        logging.getLogger().setLevel(logging.DEBUG)
    elif logging_level == "INFO":
        logging.getLogger().setLevel(logging.INFO)
    elif logging_level == "WARN":
        logging.getLogger().setLevel(logging.WARNING)
    elif logging_level == "ERROR":
        logging.getLogger().setLevel(logging.ERROR)
    elif logging_level == "CRITICAL":
        logging.getLogger().setLevel(logging.CRITICAL)

# print("Set Logging Level to {}".format(logging.getLogger().getEffectiveLevel()))


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
