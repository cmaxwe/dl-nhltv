import unittest
#############
# Expanding PYTHONPATH hack start
# A bit of a hack to make it easier to use cross without project file:
import os
import sys
fullCurrentPath = os.path.realpath(__file__)
global currentPath
currentPath = os.path.dirname(fullCurrentPath)
relativePath = os.path.join(currentPath, "..")
classPath = os.path.realpath(relativePath)
sys.path.insert(0, classPath)
#
#############
from nhltv_lib.common import *


class TestCommon(unittest.TestCase):

    def test_whichIsTrueOnExistingCommand(self):
        self.assertTrue(which("ls"))

    def test_whichIsFalseOnMissingCommand(self):
        self.assertFalse(which("lsasdkfld"))

if __name__ == "__main__":
    unittest.main()
