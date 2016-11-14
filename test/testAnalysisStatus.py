'''
Created on 2016-11-12

@author: mclamp
'''

import unittest
import os, shutil

from datetime import datetime

from iggyngs.AnalysisStatus import AnalysisStatus

class Test(unittest.TestCase):

    def testAnalysisStatus(self):


        status = AnalysisStatus("NEW")

        status.addStatus("RUNNING")


        print status.status
        print status.timestamp

        print status.getCurrentStatus()
        print status.getCurrentTimestamp()


    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
