'''
Created on Apr 24, 2016

@author: mclamp
'''

import unittest
import os, sys, shutil, pprint

from iggyngs.io.SampleSheetFile        import SampleSheetFile 
from iggyngs.io.NextSeqSampleSheetFile import NextSeqSampleSheetFile 

class Test(unittest.TestCase):

    def __init__(self,*args,**kwargs):
        super(Test,self).__init__(*args,**kwargs)

        self.file1 = 'data/H3KG7BGXY.NextSeq.singleindex.SampleSheet.csv'
        self.file2 = 'data/H7HHVAFXX.NextSeq.dualindex.SampleSheet.csv'

    def testSampleSheetFile(self):
       
        ssfile = NextSeqSampleSheetFile(self.file1)

        ssfile.parse()

        #pprint.pprint(ssfile.sections,width=1)

        self.outfile = 'test.NextSeqDualIndex.csv'

        print "Lanes ",len(ssfile.lanes)

        for l in ssfile.lanes:
           pprint.pprint( l.__dict__,width=1)

        ssfile.writeLane(self.outfile,1)

    def tearDown(self):
        if os.path.exists(self.outfile):
          os.remove(self.outfile)

if __name__ == "__main__":
    unittest.main()
