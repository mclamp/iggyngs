'''
Created on November 12 2016

@author: mclamp

'''


import unittest
import os, shutil

from iggyngs.AnalysisSpecs.CopyDirAnalysisSpec import CopyDirAnalysisSpec 
from iggyngs.AnalysisDB                        import AnalysisDB
from iggyngs.config                            import settings

class Test(unittest.TestCase):

    def __init__(self,*args,**kwargs):
        super(Test,self).__init__(*args,**kwargs)
        
    def testAnalysisDB(self):

        anadb  = AnalysisDB('tmpdb.sqlite')
        tables = anadb.getTables()

        self.assertTrue(len(tables) == 7,"Number of analysis tables")
        
        if os.path.exists('tmpdata'):
           shutil.rmtree('tmpdata') 

        cda = CopyDirAnalysisSpec()

        anadb.saveAnalysis(cda)

        self.assertTrue(cda.id == 1,"Test AnalysisDB analysis id generation")
        
        cda.setInputs(['data'])
        cda.setOutputs(['tmpdata'])
        cda.setParameters({'overwrite': False})

        anadb.saveAnalysis(cda)
        
        cda.init()
        cda.run()

        anadb.saveAnalysis(cda)


        dbcda = anadb.fetchAnalysisByID(1)


        cda = CopyDirAnalysisSpec()

        anadb.saveAnalysis(cda)

        self.assertTrue(cda.id == 2,"Test AnalysisDB analysis id generation")
        
        cda.setInputs(['data'])
        cda.setOutputs(['tmpdata'])
        cda.setParameters({'overwrite': False})

        anadb.saveAnalysis(cda)
        
        cda.init()
        cda.run()

        anadb.saveAnalysis(cda)
        

        cda = CopyDirAnalysisSpec()
        cda.setInputs(['data'])
        cda.setOutputs(['tmpdata'])
        cda.setParameters({'overwrite': True})
        anadb.saveAnalysis(cda)
        cda.init()
        cda.run()
        anadb.saveAnalysis(cda)

        cda = CopyDirAnalysisSpec()
        cda.setInputs(['data'])
        cda.setOutputs(['tmpdata'])
        cda.setParameters({'overwrite': True})
        anadb.saveAnalysis(cda)
        cda.init()
        cda.run()
        anadb.saveAnalysis(cda)

        cda = CopyDirAnalysisSpec()
        cda.setInputs(['data'])
        cda.setOutputs(['tmpdata'])
        cda.setParameters({'overwrite': True})
        anadb.saveAnalysis(cda)
        cda.init()
        cda.run()
        anadb.saveAnalysis(cda)

        cda = CopyDirAnalysisSpec()
        cda.setInputs(['data'])
        cda.setOutputs(['tmpdata'])
        cda.setParameters({'overwrite': True})
        anadb.saveAnalysis(cda)
        cda.init()
        cda.run()
        anadb.saveAnalysis(cda)

        cda = CopyDirAnalysisSpec()
        cda.setInputs(['data'])
        cda.setOutputs(['tmpdata'])
        cda.setParameters({'overwrite': True})
        anadb.saveAnalysis(cda)
        cda.init()
        cda.run()
        anadb.saveAnalysis(cda)

    def tearDown(self):
        if os.path.exists('tmpdata'):
          shutil.rmtree('tmpdata')

        #if os.path.exists('tmpdb.sqlite'):
          #os.remove('tmpdb.sqlite')

        if os.path.exists(settings.LOGFILE):
          os.remove(settings.LOGFILE)
        
if __name__ == "__main__":
    unittest.main()
