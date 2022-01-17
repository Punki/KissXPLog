import sys
import logging

from PyQt5 import QtWidgets

from KissXPLog.config import *
from KissXPLog.kiss_xp_log import MainWindow
from KissXPLog.messages import logging_setup


def main():
    logging_setup("KissXPLog.log")

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logging.info(f"Directory {data_dir} created!")

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
