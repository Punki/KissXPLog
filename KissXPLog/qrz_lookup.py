import logging
import os.path
import plistlib
import requests


# Source PLIST File: https://www.country-files.com/cty/cty.plist

def update_plist(plist_path: str):
    url = 'https://www.country-files.com/cty/cty.plist'
    logging.debug(f"Fetch new Plist from {url}....\n")
    r = requests.get(url, allow_redirects=True)
    open(plist_path, 'wb').write(r.content)
    logging.debug(f"Updated CTY.plist..")
    return None


def get_plist():
    plist_path = "../cty.plist"
    if not os.path.exists(plist_path):
        update_plist(plist_path)
    else:
        logging.debug(f"File exists, no download necessary")

    with open(plist_path, 'rb') as plist_file:
        data = plistlib.load(plist_file)
    return data


def get_dxcc_from_callsign(callsign: str):
    dxcc = get_plist()
    # Alle Keys zu all_regex hinzufügen
    all_regex = list(dxcc.keys())
    # Sortiere von Lang nach kurz
    all_regex.sort(key=len, reverse=True)

    for element in all_regex:
        if callsign.startswith(element):
            logging.debug("Found Match")
            return dxcc.get(element)
    logging.debug(f"No DXCC Data found to {callsign}")
    return None
