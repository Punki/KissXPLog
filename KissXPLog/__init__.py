import logging
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# module_path = os.path.abspath(os.getcwd())
# if module_path not in sys.path:
#     sys.path.append(module_path)

from PyQt5 import QtWidgets

from KissXPLog.config import *
from KissXPLog.kiss_xp_log import MainWindow
from KissXPLog.messages import logging_setup
from pathlib import Path


def main():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logging.info(f"Directory {data_dir} created!")

    myfile = Path(logfile_path)
    myfile.touch(exist_ok=True)
    logging_setup()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
