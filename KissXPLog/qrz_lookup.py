import logging
import os.path
import plistlib
import requests
from KissXPLog import config


# Source PLIST File: https://www.country-files.com/cty/cty.plist

def update_plist(plist_path: str):
    url = 'https://www.country-files.com/cty/cty.plist'
    logging.debug(f"Fetch new Plist from {url}....\n")
    requests.options(allow_redirects=True, url=url)
    r = requests.get(url)
    with open(plist_path, 'wb') as pf:
        pf.write(r.content)
    logging.debug(f"Updated CTY.plist..")


def get_plist():
    if not os.path.exists(config.plist_path):
        update_plist(config.plist_path)
    else:
        logging.debug(f"File exists, no download necessary")
    try:
        with open(config.plist_path, 'rb') as plist_file:
            plist_data = plistlib.load(plist_file)
    except FileNotFoundError:
        plist_data = "File not found"
        logging.error("File {} not found".format(str(config.plist_path)))
    return plist_data


def get_dxcc_from_callsign(callsign: str):
    dxcc = get_plist()
    # Add all keys to all_regex
    all_regex = list(dxcc.keys())
    # Sort list by callsign-length (descending)
    all_regex.sort(key=len, reverse=True)

    for element in all_regex:
        if callsign.startswith(element):
            logging.debug("Found Match")
            return dxcc.get(element)
    logging.debug(f"No DXCC Data found to {callsign}")
