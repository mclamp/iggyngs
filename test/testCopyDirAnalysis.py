'''
Created on Apr 25, 2016

@author: mclamp
'''


import unittest
import os, shutil

from iggyngs.AnalysisSpecs.CopyDirAnalysisSpec import CopyDirAnalysisSpec 

class Test(unittest.TestCase):

    def __init__(self,*args,**kwargs):
        super(Test,self).__init__(*args,**kwargs)
        
    def testCopyDirAnalysisSpec(self):

        if os.path.exists('tmpdata'):
           shutil.rmtree('tmpdata') 

        cda = CopyDirAnalysisSpec()

        cda.setInputs(['data'])
        cda.setOutputs(['tmpdata'])
        cda.setParameters({'overwrite': False})
        cda.init()
        
        self.assertTrue(cda.status.getCurrentStatus() == "NEW","Test new status of analysis")
        self.assertTrue(len(cda.status.status)        == 1,    "Test number of statuses")
        self.assertTrue(len(cda.status.timestamp)     == 1,    "Test number of status timestamps")
        
        cda.run()

        print cda.status.status
        
        self.assertTrue(cda.status.getCurrentStatus() == "COMPLETE","Test completion of analysis")
        self.assertTrue(len(cda.status.status)        == 3,         "Test number of analysis statuses")
        
        self.assertEqual(os.path.exists('tmpdata'),True,            "Data didn't copy to new directory tmpdata")

        cda = CopyDirAnalysisSpec()

        cda.setInputs(['data'])
        cda.setOutputs(['tmpdata'])
        cda.setParameters({'overwrite': True})
        cda.init()
        
        cda.run()

        self.assertEqual(os.path.exists('tmpdata'),True,            "Data didn't copy to new directory tmpdata")

        try:
            cda = CopyDirAnalysisSpec()

            cda.setInputs(['data'])
            cda.setOutputs(['tmpdata'])
            cda.setParameters({'overwrite': False})
            cda.init()
            
            cda.run()
        except Exception as e:
          self.assertEqual(str(e),"Destination directory [tmpdata] exists. Can't create CopyDirAnalysis without overwrite options","Exception differed when catching overwrite False")

    def tearDown(self):
        if os.path.exists('tmpdata'):
          shutil.rmtree('tmpdata')

if __name__ == "__main__":
    unittest.main()
