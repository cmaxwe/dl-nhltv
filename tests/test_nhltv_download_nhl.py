import unittest
#############
# Expanding PYTHONPATH hack start
# A bit of a hack to make it easier to use cross without project file:
import os
import sys
import json
fullCurrentPath = os.path.realpath(__file__)
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

    def test_checkForNewGame(self):
        json_source = self.dl.checkForNewGame('2017-03-14', '2017-03-17')
        self.assertTrue(isinstance(json_source, dict))

    def test_lookForTheNextGameToGet(self):
        testDataFile = os.path.join("data", "schedule.gamecontent.media.epg")
        with open(testDataFile) as data_file:
            json_source = json.load(data_file)

        game, favTeamHomeAway = self.dl.lookForTheNextGameToGet(json_source)
        self.assertEquals(game["teams"]["away"]["team"]['abbreviation'], "DET", "Expecting DET as away team")
        self.assertEqual(favTeamHomeAway, "AWAY")

    def test_getGameId(self):
        gameID, contentID, eventID = self.dl.getGameId()
        self.assertTrue(isinstance(gameID, int), "Expected gameID to be of type int")
        self.assertEqual(gameID, 2016021035, "Expected gameID=2016021035")

        self.assertTrue(isinstance(contentID, str), "Expected contentID to be of type str")
        self.assertEqual(contentID, "50172503", "Expected contentID=50172503")

        self.assertTrue(isinstance(eventID, str), "Expected contentID to be of type str")
        self.assertEqual(eventID, "221-1004480", "Expected eventID=221-1004480")


if __name__ == '__main__':
    unittest.main()
