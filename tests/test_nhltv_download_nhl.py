import unittest
#############
# Expanding PYTHONPATH hack start
# A bit of a hack to make it easier to use cross without project file:
import os
import sys
import json
from mock import patch
import nhltv_lib
import urllib2
fullCurrentPath = os.path.realpath(__file__)
global currentPath
currentPath = os.path.dirname(fullCurrentPath)
relativePath = os.path.join(currentPath, "..")
classPath = os.path.realpath(relativePath)
sys.path.insert(0, classPath)

#
#############
from nhltv_lib.download_nhl import DownloadNHL, NoGameFound
from nhltv_lib.common import getSetting


class Test_nhltv_lib_download_nhl(unittest.TestCase):
    """
    To run this do the following from anywhere in the project:
    python -m unittest discover -v
    """
    dl = DownloadNHL()
    dl.teamID = 17
    sampleDataFolder = os.path.join(currentPath, "data")
    download_file = os.path.join(sampleDataFolder, "test_download_file.txt")
    sample_schedule_epg_file = os.path.join(sampleDataFolder, "schedule.gamecontent.media.epg")
    with open(sample_schedule_epg_file) as data_file:
        json_source = json.load(data_file)

    sample_masterFile = os.path.join(sampleDataFolder, "master.m3u8")
    sample_inputFile = os.path.join(sampleDataFolder, "input.m3u8")

    def tearDown(self):
        if os.path.isfile(self.download_file):
            os.remove(self.download_file)

    def test01_checkForNewGame(self):
        json_source = self.dl.checkForNewGame('2017-03-14', '2017-03-17')
        self.assertTrue(isinstance(json_source, dict))

    @patch.object(urllib2, "urlopen")
    def test02_checkForNewGame_returns_json(self, mock_urlopen):
        mock_urlopen.return_value = open(self.sample_schedule_epg_file)
        json_source = self.dl.checkForNewGame('2017-03-14', '2017-03-17')
#         self.assertTrue(isinstance(json_source, json), "Expected json_source to be of type json")
        self.assertTrue(isinstance(json_source, dict), "Expected json_source to be of type dict")

    @patch("nhltv_lib.download_nhl.getSetting", return_value=123)
    def test03_lookForTheNextGameToGet(self, mock_common):
        game, favTeamHomeAway = self.dl.lookForTheNextGameToGet(self.json_source)
        self.assertEquals(game["teams"]["away"]["team"]['abbreviation'], "DET", "Expecting DET as away team")
        self.assertEqual(favTeamHomeAway, "AWAY")

    @patch("nhltv_lib.download_nhl.getSetting", return_value=3016021040)
    def test_lookForTheNextGameToGet_raises_NoGameFound(self, mock_common):
        with self.assertRaises(NoGameFound):
            self.dl.lookForTheNextGameToGet(self.json_source)

    @patch.object(nhltv_lib.download_nhl, "getSetting")
    @patch.object(urllib2, "urlopen")
    @patch.object(nhltv_lib.download_nhl.DownloadNHL, "checkForNewGame")
    def test04_getGameId(self, mock_checkForNewGame, mock_urlopen, mock_getSetting):
        mock_checkForNewGame.return_value = self.json_source
        mock_urlopen.return_value = self.sample_schedule_epg_file
        mock_getSetting.return_value = 123
        gameID, contentID, eventID, waitTimeInMin = self.dl.getGameId()
        self.assertTrue(isinstance(gameID, int), "Expected gameID to be of type int")
        self.assertTrue(isinstance(contentID, str), "Expected contentID to be of type str")
        self.assertTrue(isinstance(eventID, str), "Expected contentID to be of type str")
        self.assertTrue(isinstance(waitTimeInMin, int), "Expected waitTimeInMin to be of type int")

    def test05_getQualityUrlFromMasterDropToNextBest_m3u8(self):
        quality_url = self.dl.getQualityUrlFromMaster_m3u8(self.sample_masterFile)
        self.assertTrue("3500K" in quality_url)

    def test06_createDownloadFile(self):
        quality_url = "http://hlslive-akc.med2.med.nhl.com/hdnts=exp=1489918789~acl=/*~id=nhlGatewayId:3821533~data=50068103~hmac=8004dc987fb52ff4b2aff47edbf6845a686755bdd2f34d66e9da312a265cb97f/5fa5a38415b1e0787f24aa9005f8377a/ls04/nhl/2017/03/17/NHL_GAME_VIDEO_BOSEDM_M2_HOME_20170317_1488820214854/3500K/3500_complete-trimmed.m3u8"
        self.dl.createDownloadFile(self.sample_inputFile, self.download_file, quality_url)


if __name__ == '__main__':
    unittest.main()
