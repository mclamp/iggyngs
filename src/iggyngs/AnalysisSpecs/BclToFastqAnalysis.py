import os, re, logging

from abc import ABCMeta, abstractmethod

from iggyngs.io.SampleSheetFile import SampleSheetFile    
from iggyngs.Command            import Command
from iggyngs.Analysis           import Analysis

class BclToFastqAnalysis(Analysis):

    def __init__(self,runname,samplesheet,rundir,outdir,logdir,basesmask,mismatches,threads,test=True,verbose=True):

       Analysis.__init__(self)

       self.runname     = runname
       self.samplesheet = samplesheet
       self.rundir      = rundir
       self.outdir      = outdir
       self.logdir      = logdir
       self.basesmask   = basesmask
       self.mismatches  = mismatches
       self.threads     = threads
       self.test        = test
       self.verbose     = verbose
