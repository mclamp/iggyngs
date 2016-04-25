'''
Created on Apr 21, 2016

@author: mclamp
'''
import unittest
import os, shutil

from iggyngs.IlluminaRunName import IlluminaRunName

class Test(unittest.TestCase):

    def __init__(self,*args,**kwargs):
        super(Test,self).__init__(*args,**kwargs)
        self.runname1 = '150605_D00365_0511_BC6FHCANXX'
        self.runname2 = '150605_D00365_0511_BC6FHCANXX'
        
    def testIlluminaRunName(self):
       
        runname = IlluminaRunName(self.runname1)

        #{'pos_and_flowcell': 'BC6FHCANXX', 'machineID': 'D00365', 'counter': '0511', 'pos': 'B', 'flowcell': 'C6FHCANXX', 'runName': '150605_D00365_0511_BC6FHCANXX', 'date': '150605'}
    
        self.assertEqual(runname.pos_and_flowcell,"BC6FHCANXX","Run name returned wrong pos_and_flowcell [%s]"%runname.pos_and_flowcell)
        self.assertEqual(runname.machineID,"D00365","Run name returned wrong machine ID [%s]"%runname.machineID)
        self.assertEqual(runname.counter,"0511","Run name returned wrong counter [%s]"%runname.counter)
        self.assertEqual(runname.date,"150605","Run name returned wrong date [%s]"%runname.date)
        self.assertEqual(runname.flowcell,"C6FHCANXX","Run name returned wrong flowcell [%s]"%runname.flowcell)
        self.assertEqual(runname.runType,"HiSeq","Run name returned wrong run type [%s]"%runname.runType)
 

if __name__ == "__main__":
    unittest.main()
