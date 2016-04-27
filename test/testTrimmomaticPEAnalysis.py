'''
Created on Apr 25, 2016

@author: mclamp
'''


import unittest
import os, shutil

from iggyngs.TrimmomaticPEAnalysis import TrimmomaticPEAnalysis 

class Test(unittest.TestCase):

    def __init__(self,*args,**kwargs):
        super(Test,self).__init__(*args,**kwargs)
        
    def testTrimmomaticPEAnalysis(self):
        ana = TrimmomaticPEAnalysis('data/sample_1.fq','data/sample_2.fq','trimout','.',False)

        ana.makeCommands()
        
        ana.run()

    #def tearDown(self):
    #    if os.path.exists('trimout'):
    #      shutil.rmtree('trimout')

if __name__ == "__main__":
    unittest.main()
