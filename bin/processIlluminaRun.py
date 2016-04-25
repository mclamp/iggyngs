#!/usr/bin/env python

import sys, re, os, pprint, logging, shutil

scriptdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptdir + "/../src/")

from argparse  import ArgumentParser

from IlluminaRunName                  import IlluminaRunName

from ioformats.RunInfoFile            import RunInfoFile

from ioformats.HiSeqSampleSheetFile   import HiSeqSampleSheetFile
from ioformats.NextSeqSampleSheetFile import NextSeqSampleSheetFile

from HiSeqBclToFastqAnalysis          import HiSeqBclToFastqAnalysis
from NextSeqBclToFastqAnalysis        import NextSeqBclToFastqAnalysis

from IlluminaRunProcessor             import IlluminaRunProcessor

def printArgumentString(args):
    opts = vars(args)
    argstring = ", ".join("=".join((str(k),str(opts[k]))) for k in opts)

    print('Starting Illumina processing for [' + argstring + ']')

def run(args):
 
  runname          = args.runname

  irp = IlluminaRunProcessor(runname)

  logger    = irp.logger
  runstring = irp.runstring

  irp.test             = True            if args.test       else False
  irp.force            = True            if args.force      else False
  irp.mismatches       = args.mismatches if args.mismatches else 0
  irp.cores            = args.cores      if args.cores      else 4

  irp.setParentIndir(args.parentindir)   if args.parentindir   else False 
  irp.setParentOutdir(args.parentoutdir) if args.parentoutdir  else False

  irp.setSampleSheetFile(args.samplesheet)
  irp.setRunInfoFile(os.path.join(args.parentindir,runname,"RunInfo.xml"))

  irp.rundir          = os.path.join(args.parentindir,runname)

  irp.validateInput()

  irp.logger.info(irp.runstring + "Processing lanes for [%s]"%irp.runname)


  for idx, l in enumerate(irp.samplesheet.lanes):

     logger.info(runstring + "Processing lane [%d]"%idx) 

     indexstring   = l.makeIndexString()
     userLaneLabel = l.userLaneLabel
     subIDs        = l.subIDs
     userLaneName  = l.userLaneName

     lanedir       = os.path.join(irp.outdir,"Lane"+ str(userLaneLabel) + ".indexlength_"+str(indexstring))

     logger.info(runstring + "Processing lane label [%s]"%userLaneLabel) 
     logger.info(runstring + "Number of samplesheet lines for lane [%s] are [%d]"%(userLaneLabel,len(l.ssSampleLines)))
     logger.info(runstring + "Indexstring for lane [%s] is [%s]"%(userLaneLabel,indexstring))
     logger.info(runstring + "Lane output directory is [%s]"%(lanedir))

     #  Make the basesmask
     logger.info(runstring + "Making bases mask for lane [%s]"%userLaneLabel)
     basesmask = l.makeBasesMask(irp.runinfo.rdict)
     logger.info(runstring + "Made bases mask for lane [%s] [%s]"%(userLaneLabel,basesmask))

     #  Write the lane samplesheet
     lanessfile = os.path.join(irp.outdir,"SampleSheet.Lane"+userLaneLabel+".csv")
     irp.samplesheet.writeLane(lanessfile,userLaneLabel) 

     #  Make the BclToFastqAnalysis obj and construct the command line

     if irp.runType == "HiSeq":
       bcl2fastq = HiSeqBclToFastqAnalysis(runname,lanessfile,irp.rundir,lanedir,irp.outdir,basesmask,irp.mismatches,irp.cores,irp.test)
       bcl2fastq.run()
     elif irp.runType == "NextSeq":
       bcl2fastq = NextSeqBclToFastqAnalysis(runname,lanessfile,irp.rundir,lanedir,irp.outdir,basesmask,irp.mismatches,irp.cores,irp.test)
       bcl2fastq.run()

     #   Run (if not test)

     #   Check output/post-process output

  # End lane loop

if __name__ == "__main__":

    parser        = ArgumentParser(description = 'Process Illumina Run - create fastq files')

    parser.add_argument('-i','--parentindir'   ,     required=True,   help='Parent directory where the individual run directories live')
    parser.add_argument('-o','--parentoutdir'     ,  required=True,   help="Directory under which to put the output - name defaults to run name")
    parser.add_argument('-r','--runname'      ,      required=True,   help="Name of run")
    parser.add_argument('-s','--samplesheet'    ,    required=False,  help="Use this samplesheet file.  Default is SampleSheet.csv in the run directory")
    parser.add_argument('-m','--mismatches'   ,      required=False,  help="Number of mismatches [0]",type=int)
    parser.add_argument('-c','--cores'      ,        required=False,  help="Number of cores to run on [4]", type=int)
    parser.add_argument('-f','--force'      ,        required=False,  help="Force overwrite of any existing output directories [False]", action="store_true")
    parser.add_argument('-t','--test' ,              required=False,  help="Generate the command lines/sample sheets but don't run [True]",action="store_true")

    args = parser.parse_args()

    run(args)
