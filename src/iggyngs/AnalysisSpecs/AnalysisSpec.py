import os, re, logging

from iggyngs.Command                   import Command
from iggyngs.AnalysisStatus            import AnalysisStatus

class AnalysisSpec(object):

    test         = False
    
    inputs       = []
    inputtypes   = []
    
    outputs      = []
    outputtypes  = []

    commands     = []
    outfiles     = []
    
    id           = None
    status       = None
    name         = "Base"

    date_created = None
    last_updated = None

    summary      = {}
    parameters   = {}
    
    def __init__(self):

       self.status = AnalysisStatus()
       
       self.inputs       = []
       self.inputtypes   = []
       self.outputs      = []
       self.outputtypes  = []
       self.commands     = []
       self.outfiles     = []
       self.id           = None
       self.name         = "Base"
       self.date_created = None
       self.last_updated = None
       self.summary      = {}
       self.parameters   = {}
       
    def setInputs(self,inputs):
        self.inputs = inputs

    def setInputTypes(self,inputtypes):
        self.inputtypes = inputtypes

    def setOutputs(self,outputs):
        self.outputs = outputs
        
    def setParameters(self,params):
        self.params = params
        
    def init(self):
        pass
    
    def run(self):

        self.status.addStatus("RUNNING")

        try:
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

         self.status.addStatus("COMPLETE")

        except Error:
            self.logger.info("ERROR in %s Analysis Module"%self.name)
            self.status.addStatus("FAILED")

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
        cmd.run()

        print cmd.outstr
        fh.close()


    def toString(self):

        str  = "%-30s %-30s\n"%("Name",         self.name)
        str += "%-30s %-30s\n"%("ID",           self.id)
        str += "%-30s %-30s\n"%("CurrentStatus",self.status.getCurrentStatus())
        str += "%-30s %-30s\n"%("DateCreated",  self.date_created)
        str += "%-30s %-30s\n"%("LastUpdated",  self.last_updated)

        str += "\nInputs\n"

        i = 0;

        while i < len(self.inputs):
            str += "%-30s %-30s\n"%(self.inputs[i],self.inputtypes[i])
            i = i + 1

        str += "\nOutputs\n"
        i = 0

        while i < len(self.outputs):
            str += "%-30s %-30s\n"%(self.outputs[i],self.outputtypes[i])
            i = i + 1

        str += "\nStatus History\n";
        i = 0

        while i < len(self.status.status):
            str += "%-30s %-30s\n"%(self.status.status[i],self.status.timestamp[i])
            i = i + 1
            
        return str
        

