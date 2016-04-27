'''
Created on Apr 27, 2016

@author: mclamp
'''


import unittest
import os, shutil

from iggyngs.KallistoAnalysis import KallistoAnalysis 

class Test(unittest.TestCase):

    def __init__(self,*args,**kwargs):
        super(Test,self).__init__(*args,**kwargs)
        
    def testKallistoAnalysis(self):
        ana = KallistoAnalysis('data/sample_1.fq.gz','data/sample_2.fq.gz','data/mm10.rsem.kall','kallout','.',False)

        ana.makeCommands()
        
        ana.run()

    #def tearDown(self):
    #    if os.path.exists('kallout'):
    #      shutil.rmtree('kallout')

if __name__ == "__main__":
    unittest.main()
