'''
Created on 2016-07-15

@author: mclamp
'''

import unittest
import os, shutil

from iggyngs.Analysis2 import Analysis2

class Test(unittest.TestCase):

    inputs   = ['file1.dat','file2.dat']
    commands = ['ls -l /tmp/']

    def testAnalysis2(self):
        
        ana2 = Analysis2("TestAnalysis")

        self.assertTrue(ana2.name == 'TestAnalysis',"Test of analysis2 name")
        
        ana2.setInputs(self.inputs);

        self.assertTrue(len(ana2.inputs) == 2,"Test of analysis2 number of inputs")

        self.assertTrue(ana2.inputs[1] == 'file2.dat',"Test of analysis2 second input name")

        ana2.setCommands(self.commands)

        self.assertTrue(len(ana2.comobj) == 1,"Test of analysis2 number of commands")

        self.assertTrue(ana2.comstr[0] == self.commands[0],"Test of analysis1 command 1")


        ana2.run()

        for str in ana2.stdouts:
            print '\n'.join(str)


        for str in ana2.stderrs:
            print '\n'.join(str)


        ana2.test = True

        ana2.run()

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
