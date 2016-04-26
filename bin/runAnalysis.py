#!/usr/bin/env python

import sys, re, os, pprint, logging, shutil

scriptdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptdir + "/../src/")

from argparse  import ArgumentParser

from iggyngs.FastQCAnalysis                   import FastQCAnalysis
from iggyngs.IlluminateAnalysis               import IlluminateAnalysis 
from iggyngs.CopyDirAnalysis                  import CopyDirAnalysis 

def printArgumentString(args):
    opts = vars(args)
    argstring = ", ".join("=".join((str(k),str(opts[k]))) for k in opts)

    print('Starting analysis run for [' + argstring + ']')

def run(args):

    printArgumentString(args)
 
    analname = args.analysis
    paramstr = args.parameters 
    force    = args.force    if args.force else False
    test     = args.test     if args.test  else False 

    params = []
    tmp  = paramstr.split(",")

    for t in tmp:
      k,v = t.split("=")
      print "K %s : %s"%(k,v)
      params.append(v)

  
    if analname == "Illuminate":
       ana = IlluminateAnalysis(params[0],params[1])
       ana.makeCommands()
       ana.run()
       print ana.data 
if __name__ == "__main__":

    parser        = ArgumentParser(description = 'Run analysis module')

    parser.add_argument('-a','--analysis'   ,     required=True,   help='Analysis module to run [FastQC,Illuminate,CopyDir]')
    parser.add_argument('-p','--parameters'   ,      required=False,  help="Parameters for the module e.g. 'rundir=mydir,outdir=myout,lane=2'")
    parser.add_argument('-f','--force'      ,        required=False,  help="Force overwrite of any existing output directories [False]", action="store_true")
    parser.add_argument('-t','--test' ,              required=False,  help="Generate the command lines/sample sheets but don't run [True]",action="store_true")

    args = parser.parse_args()

    run(args)
