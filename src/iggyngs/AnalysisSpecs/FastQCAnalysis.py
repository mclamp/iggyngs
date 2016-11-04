import os, re, logging

from abc import ABCMeta, abstractmethod

from iggyngs.io.SampleSheetFile import SampleSheetFile    
from iggyngs.Command            import Command
from iggyngs.Analysis           import Analysis

class FastQCAnalysis(Analysis):

    def __init__(self,fastqfile,outdir,logdir,test=True,verbose=True):

       Analysis.__init__(self)

       self.fastqfile   = fastqfile
       self.outdir      = outdir
       self.logdir      = logdir
       self.test        = test
       self.verbose     = verbose

    def makeCommands(self):

        if not os.path.isabs(self.outdir):
           self.outdir = os.path.join(os.getcwd(),self.outdir)

        fastqname = os.path.basename(self.fastqfile)
        outdir    = os.path.join(self.outdir,fastqname+".FastQC")

        if not os.path.isdir(outdir):
           print "Making dir "+outdir
           os.makedirs(outdir)

        outfile = os.path.join(self.outdir,fastqname+".FastQC.log")
        command = 'source new-modules.sh; module load fastqc;'

        command = command +  "fastqc  --extract -o " + outdir + " " + self.fastqfile 

        self.commands.append(command)
        self.outfiles.append(outfile)

