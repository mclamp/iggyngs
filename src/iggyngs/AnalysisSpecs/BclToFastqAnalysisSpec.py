import os, re, logging

from abc import ABCMeta, abstractmethod

from iggyngs.Illumina.io.SampleSheetFile      import SampleSheetFile    
from iggyngs.Command                          import Command
from iggyngs.AnalysisSpecs.AnalysisSpec       import AnalysisSpec

class BclToFastqAnalysisSpec(AnalysisSpec):

    def __init__(self,runname,samplesheet,rundir,outdir,logdir,basesmask,mismatches,threads,test=True,verbose=True):

       AnalysisSpec.__init__(self)

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
