"""
Created on Apr 22 2016
Harvard FAS Informatics
All rights reserved.

@author: mclamp 
"""

import unittest, sys, os, re

from iggyngs.io.RunInfoFile import RunInfoFile 

class RunInfoFileTest(unittest.TestCase):

    def setUp(self):
       self.file1 = 'data/H2LC5AFXX.RunInfo.xml'
       self.file2 = 'data/H2LC5AFXX.bad1.RunInfo.xml'
       self.file3 = 'data/H2LC5AFXX.bad2.RunInfo.xml'

    def testRunInfoFile1(self):
      rif  = RunInfoFile(self.file1)
      rif.parse()
      rdict    = rif.rdict
      datetext = rif.datetext

      self.assertTrue(datetext == "150527")
    
    def testRunInfoFile2(self): 
      rif  = RunInfoFile(self.file1)

      caught = False

      try:
        rif.parse()
        rdict    = rif.rdict
        datetext = rif.datetext
      except Exception as e:

        if re.search('Number element', str(e), re.I):
           caught = True

      self.assertTrue(caught)


    def testRunInfoFile2(self):
      rif  = RunInfoFile(self.file3)

      caught = False

      try:
        rif.parse()
        rdict    = rif.rdict
        datetext = rif.datetext
      except Exception as e:
        if re.search('NumCycles element', str(e), re.I):
           caught = True

      self.assertTrue(caught)

    def tearDown(self):
        pass

    def testName(self):
        pass


if __name__ == "__main__":
    unittest.main()
