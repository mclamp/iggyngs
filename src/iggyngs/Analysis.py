import os, re, logging

from abc import ABCMeta, abstractmethod

from iggyngs.io.SampleSheetFile        import SampleSheetFile
from iggyngs.Command                   import Command

class Analysis(object):
    __metaclass__ = ABCMeta

    test     = False
    commands = []
    outfiles = []

    def __init__(self):
       pass

    def run(self):

         i = 0
         while i < len(self.commands):
          
            command = self.commands[i]
            outfile = self.outfiles[i]

            if not self.test:
              self.shell(command, outfile)
            else:
              print "Command : %s"%command
              print "Outfile : %s"%outfile
              print "*********** Test mode. not running **************"
 
            i = i + 1
    
    @abstractmethod
    def makeCommands(self):
       pass
 
    def shell(self, command, outputFile, append=True):

        if append:
            mode = 'a'
        else:
            mode = 'w'
        fh = open(outputFile, mode)
        fh.write(command + '\n') #write command to file

        cmd = Command(command)

        for line in cmd.run():
            line = line.strip()
            if line != '':
                fh.write(line + '\n') #write command output to file
                fh.flush()
            if self.verbose: print line
        fh.close()
