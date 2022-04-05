import os
import plistlib
import tempfile
import unittest
from unittest.mock import patch, mock_open, Mock

from KissXPLog.qrz_lookup import update_plist, get_plist
from KissXPLog import config


class PlistTestCase(unittest.TestCase):

    @patch('KissXPLog.config.plist_path', "../tmp/test_plist.plist")
    def test_update_plist(self):
        with patch('requests.get') as mock_request:
            url = 'https://www.country-files.com/cty/cty.plist'

            # set a `status_code` attribute on the mock object
            # with value 200
            mock_request.return_value.status_code = 200
            # set fake content
            mock_request.return_value.content = b'Yep, this PLIST is working'

            try:
                update_plist(config.plist_path)
                with open(config.plist_path) as cf:
                    contents = cf.read()
            finally:
                os.remove(config.plist_path)
            # test if requests.get was called
            # with the given url or not
            mock_request.assert_called_once_with(url)
            self.assertEqual(contents, "Yep, this PLIST is working")

    @patch('KissXPLog.config.plist_path', "../tmp/test_plist.plist")
    def test_get_plist_file_exists(self):
        pl = dict(
            TestCase=dict(
                Country='Sov Mil Order of Malta',
                Prefix='1A',
                ADIF=246,
                CQZone=15,
                ITUZone=28,
                Continent='EU',
                Latitude=41.9,
                Longitude=-12.43,
                GMTOffset=-1.0,
                ExactCallsign=False, ),
        )
        with open(config.plist_path, 'wb') as fp:
            plistlib.dump(pl, fp)
        plist = get_plist()
        self.assertEqual(plist, pl)

        return None

    @patch('KissXPLog.config.plist_path', "../tmp/test_plist.plist")
    def test_get_plist_file_not_exists(self):
        try:
            os.remove(config.plist_path)
        except FileNotFoundError:
            print("File does not exist, no deleting necessary, carry on...")

        with patch("KissXPLog.qrz_lookup.update_plist") as update_plist_patch:
            get_plist()
        update_plist_patch.assert_called()
