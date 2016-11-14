'''
Created on Apr 25, 2016

@author: mclamp
'''


import unittest
import os, shutil

from iggyngs.AnalysisSpecs.FastQCAnalysisSpec import FastQCAnalysisSpec

class Test(unittest.TestCase):

    def __init__(self,*args,**kwargs):
        super(Test,self).__init__(*args,**kwargs)
        
    def testFastQCAnalysisSpec(self):
        fastqcana = FastQCAnalysisSpec('data/sample_1.fq.gz','testFastQC','.',False)
        fastqcana.makeCommands()
        
        fastqcana.run()

        self.assertTrue(os.path.isdir('testFastQC'),"Output directory testFastQC doesn't exist")
        self.assertTrue(os.path.isdir('testFastQC/sample_1.fq.gz.FastQC'),"Output directory testFastQC/sample_1.fq.FastQC doesn't exist")
        self.assertTrue(os.path.exists('testFastQC/sample_1.fq.gz.FastQC/sample_1_fastqc.html'),"Output testFastQC/sample_1.fq.FastQC/sample_1_fastqc.html doesn't exist")
        self.assertTrue(os.path.exists('testFastQC/sample_1.fq.gz.FastQC/sample_1_fastqc.zip'),"Output testFastQC/sample_1.fq.FastQC/sample_1_fastqc.zip doesn't exist")
        self.assertTrue(os.path.exists('testFastQC/sample_1.fq.gz.FastQC.log'),"Output testFastQC/sample_1.fq.FastQC.log doesn't exist")

    def tearDown(self):
        if os.path.exists('testFastQC'):
          #shutil.rmtree('testFastQC')
          pass

if __name__ == "__main__":
    unittest.main()
