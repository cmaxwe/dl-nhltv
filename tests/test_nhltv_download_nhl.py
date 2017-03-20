import unittest
#############
# Expanding PYTHONPATH hack start
# A bit of a hack to make it easier to use cross without project file:
import os
import sys
import json
fullCurrentPath = os.path.realpath(__file__)
global currentPath
currentPath = os.path.dirname(fullCurrentPath)
relativePath = os.path.join(currentPath, "..")
classPath = os.path.realpath(relativePath)
sys.path.insert(0, classPath)
#
#############
from nhltv_lib.download_nhl import DownloadNHL


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
    sample_masterFile = os.path.join(sampleDataFolder, "master.m3u8")
    sample_inputFile = os.path.join(sampleDataFolder, "input.m3u8")

    def tearDown(self):
        if os.path.isfile(self.download_file):
            os.remove(self.download_file)

    def test_checkForNewGame(self):
        json_source = self.dl.checkForNewGame('2017-03-14', '2017-03-17')
        self.assertTrue(isinstance(json_source, dict))

    def test_lookForTheNextGameToGet(self):
        with open(self.sample_schedule_epg_file) as data_file:
            json_source = json.load(data_file)

        game, favTeamHomeAway = self.dl.lookForTheNextGameToGet(json_source)
        self.assertEquals(game["teams"]["away"]["team"]['abbreviation'], "DET", "Expecting DET as away team")
        self.assertEqual(favTeamHomeAway, "AWAY")

    def test_getGameId(self):
        gameID, contentID, eventID = self.dl.getGameId()
        self.assertTrue(isinstance(gameID, int), "Expected gameID to be of type int")
        self.assertTrue(isinstance(contentID, str), "Expected contentID to be of type str")
        self.assertTrue(isinstance(eventID, str), "Expected contentID to be of type str")

    def test_getQualityUrlFromMasterDropToNextBest_m3u8(self):
        quality_url = self.dl.getQualityUrlFromMaster_m3u8(self.sample_masterFile)
        self.assertTrue("3500K" in quality_url)

    def test_createDownloadFile(self):
        quality_url = "http://hlslive-akc.med2.med.nhl.com/hdnts=exp=1489918789~acl=/*~id=nhlGatewayId:3821533~data=50068103~hmac=8004dc987fb52ff4b2aff47edbf6845a686755bdd2f34d66e9da312a265cb97f/5fa5a38415b1e0787f24aa9005f8377a/ls04/nhl/2017/03/17/NHL_GAME_VIDEO_BOSEDM_M2_HOME_20170317_1488820214854/3500K/3500_complete-trimmed.m3u8"
        self.dl.createDownloadFile(self.sample_inputFile, self.download_file, quality_url)

if __name__ == '__main__':
    unittest.main()
