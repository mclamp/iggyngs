'''
Created on Apr 25, 2016

@author: mclamp
'''


import unittest
import os, shutil

from iggyngs.CopyDirAnalysis import CopyDirAnalysis 

class Test(unittest.TestCase):

    def __init__(self,*args,**kwargs):
        super(Test,self).__init__(*args,**kwargs)
        
    def testCopyDirAnalysis(self):

        if os.path.exists('tmpdata'):
           shutil.rmtree('tmpdata') 

        cda = CopyDirAnalysis('data','tmpdata')
        cda.run()

        self.assertEqual(os.path.exists('tmpdata'),True,"Data didn't copy to new directory tmpdata")


        cda = CopyDirAnalysis('data','tmpdata',True)
        cda.run()

        self.assertEqual(os.path.exists('tmpdata'),True,"Data didn't copy to new directory tmpdata")

        try:
          cda = CopyDirAnalysis('data','tmpdata',False)
          cda.run()
        except Exception as e:
          self.assertEqual(str(e),"Destination directory [tmpdata] exists. Can't create CopyDirAnalysis without overwrite options","Exception differed when catching overwrite False")

    def tearDown(self):
        if os.path.exists('tmpdata'):
          shutil.rmtree('tmpdata')

if __name__ == "__main__":
    unittest.main()
