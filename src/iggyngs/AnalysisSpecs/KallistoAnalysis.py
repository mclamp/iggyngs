import os, re, logging

from iggyngs.Analysis           import Analysis

class KallistoAnalysis(Analysis):

    def __init__(self,fastqfile1,fastqfile2,genome,outdir,logdir,test=True,verbose=True):

       Analysis.__init__(self)

       self.fastqfile1   = fastqfile1
       self.fastqfile2   = fastqfile2
       self.genome       = genome
       self.outdir      = outdir
       self.logdir      = logdir
       self.test        = test
       self.verbose     = verbose

    def makeCommands(self):

        if not os.path.isabs(self.outdir):
           self.outdir = os.path.join(os.getcwd(),self.outdir)

        if not os.path.exists(self.fastqfile1):
           raise Exception("Fastq file 1 [%s] doesn't exist.  Can't run kallisto"%self.fastqfile1)

        if not os.path.exists(self.fastqfile2):
           raise Exception("Fastq file 2 [%s] doesn't exist.  Can't run kallisto"%self.fastqfile2)

        if not os.path.exists(self.genome):
           raise Exception("Kallisto genome index file [%s] doesn't exist. Can't run kallisto"%self.genome)
        if not os.path.isdir(self.outdir):
           os.makedirs(self.outdir)

        fastqname1 = os.path.basename(self.fastqfile1)
        fastqname2 = os.path.basename(self.fastqfile2)

        outfile = os.path.join(self.outdir,fastqname1 +".TrimmomaticPE.log")

       
        command = "module load gcc/5.2.0-fasrc01 openmpi/1.10.0-fasrc01 kallisto/0.42.4-fasrc01;"
        command = command + "kallisto quant -i " + self.genome + " -b 100 -t 32 -o " + self.outdir + " " + self.fastqfile1 + " " + self.fastqfile2

        self.commands.append(command)
        self.outfiles.append(outfile)

