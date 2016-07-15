import os, re, logging

from abc import ABCMeta, abstractmethod

from iggyngs.Command                   import Command

class Analysis2(object):
    __metaclass__ = ABCMeta

    test            = False
    debug           = False

    name            = None

    inputs          = []

    comstr          = []
    comobj          = []

    stdouts         = []
    stderrs         = []

    slurm           = False
    run             = False
    retries         = 5
    currentstatus   = 'NEW'

    slurminfo       = {}
    status          = {}

    def __init__(self,name):
        self.name = name


    def setInputs(self,inputs):
        self.inputs = inputs

    def setCommands(self,commands):
        self.comobj = []
        self.comstr = commands

        for com in self.comstr:
            self.comobj.append(Command(com))


    def run(self):
        
        for com in self.comobj:

            if not self.test:
                com.run()

                self.stdouts.append(com.outstr)
                self.stderrs.append(com.errstr)

            else:
                print "Command : %s"%com.command
                print "*********** Test mode. not running **************"
                
