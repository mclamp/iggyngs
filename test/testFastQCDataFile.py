'''
Created on Apr 25, 2016

@author: mclamp
'''


import unittest
import os, shutil, pprint

from iggyngs.io.FastQCDataFile  import FastQCDataFile

class Test(unittest.TestCase):

    def __init__(self,*args,**kwargs):
        super(Test,self).__init__(*args,**kwargs)
        
    def testFastQCAnalysis(self):
        fastqc = FastQCDataFile('data/fastqc_data.txt')

        pprint.pprint(fastqc.__dict__,width=1)
        #self.assertTrue(os.path.isdir('testFastQC'),"Output directory testFastQC doesn't exist")
        #self.assertTrue(os.path.isdir('testFastQC/sample_1.fq.FastQC'),"Output directory testFastQC/sample_1.fq.FastQC doesn't exist")
        #self.assertTrue(os.path.exists('testFastQC/sample_1.fq.FastQC/sample_1_fastqc.html'),"Output testFastQC/sample_1.fq.FastQC/sample_1_fastqc.html doesn't exist")
        #self.assertTrue(os.path.exists('testFastQC/sample_1.fq.FastQC/sample_1_fastqc.zip'),"Output testFastQC/sample_1.fq.FastQC/sample_1_fastqc.zip doesn't exist")
        #self.assertTrue(os.path.exists('testFastQC/sample_1.fq.FastQC.log'),"Output testFastQC/sample_1.fq.FastQC.log doesn't exist")

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
