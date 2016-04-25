'''
Created on Apr 21, 2016

@author: mclamp
'''

import unittest
import os, shutil

from iggyngs.io.SampleSheetFile      import SampleSheetFile 
from iggyngs.io.HiSeqSampleSheetFile import HiSeqSampleSheetFile 

class Test(unittest.TestCase):

    def __init__(self,*args,**kwargs):
        super(Test,self).__init__(*args,**kwargs)
        self.file = 'data/HFWFCBCXX.csv'
        
    def testSampleSheetFile(self):
       
        ssfile = HiSeqSampleSheetFile(self.file)


        ssfile.parse()

        self.outfile = 'test.HFWFCBCXX.csv'

        for l in ssfile.lanes:
           print l.userLaneLabel
           print l.ssLineIndices
        ssfile.writeLane(self.outfile,1)

        #self.assertEqual(runname.pos_and_flowcell,"BC6FHCANXX","Run name returned wrong pos_and_flowcell [%s]"%runname.pos_and_flowcell)
        #self.assertEqual(runname.machineID,"D00365","Run name returned wrong machine ID [%s]"%runname.machineID)
        #self.assertEqual(runname.counter,"0511","Run name returned wrong counter [%s]"%runname.counter)
        #self.assertEqual(runname.date,"150605","Run name returned wrong date [%s]"%runname.date)
        #self.assertEqual(runname.flowcell,"C6FHCANXX","Run name returned wrong flowcell [%s]"%runname.flowcell)
 

    def tearDown(self):
        if os.path.exists(self.outfile):
          os.remove(self.outfile)

if __name__ == "__main__":
    unittest.main()
