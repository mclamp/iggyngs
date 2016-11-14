import os, re, logging

from iggyngs.AnalysisSpecs.AnalysisSpec           import AnalysisSpec

class TrimmomaticPEAnalysisSpec(AnalysisSpec):

    def __init__(self,fastqfile1,fastqfile2,outdir,logdir,test=True,verbose=True):

       AnalysisSpec.__init__(self)

       self.fastqfile1   = fastqfile1
       self.fastqfile2   = fastqfile2
       self.outdir      = outdir
       self.logdir      = logdir
       self.test        = test
       self.verbose     = verbose

    def makeCommands(self):

        if not os.path.isabs(self.outdir):
           self.outdir = os.path.join(os.getcwd(),self.outdir)

        if not os.path.exists(self.fastqfile1):
           raise Exception("Fastq file 1 [%s] doesn't exist.  Can't run TrimmomaticPE"%self.fastqfile1)

        if not os.path.exists(self.fastqfile2):
           raise Exception("Fastq file 2 [%s] doesn't exist.  Can't run TrimmomaticPE"%self.fastqfile2)

        if not os.path.isdir(self.outdir):
           os.makedirs(self.outdir)

        fastqname1 = os.path.basename(self.fastqfile1)
        fastqname2 = os.path.basename(self.fastqfile2)

        outfile = os.path.join(self.outdir,fastqname1 +".TrimmomaticPE.log")

        command = "module load legacy/0.0.1-fasrc01; module load centos6/Trimmomatic-0.32;"
        command = command + "java -jar $TRIMMOMATIC/trimmomatic-0.32.jar PE -threads 16 -phred33 "
        command = command + self.fastqfile1 + " " + self.fastqfile2 + " " 
        command = command + os.path.join(self.outdir,fastqname1 + ".trimmed.paired.fastq") + " " 
        command = command + os.path.join(self.outdir,fastqname1 + ".trimmed.unpaired.fastq") + " " 
        command = command + os.path.join(self.outdir,fastqname2 + ".trimmed.paired.fastq") + " " 
        command = command + os.path.join(self.outdir,fastqname2 + ".trimmed.unpaired.fastq") + " " 
        command = command + "ILLUMINACLIP:$TRIMMOMATIC/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:20 2>&1 > " + outfile

        self.commands.append(command)
        self.outfiles.append(outfile)

        print self.commands

