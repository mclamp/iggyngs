import os, re, logging

from iggyngs.io.SampleSheetFile import SampleSheetFile    
from iggyngs.Command                   import Command
from iggyngs.BclToFastqAnalysis        import BclToFastqAnalysis

class NextSeqBclToFastqAnalysis(BclToFastqAnalysis):

    def __init__(self,runname,samplesheet,rundir,outdir,logdir,basesmask,mismatches,threads,test=True,verbose=True):
        BclToFastqAnalysis.__init__(self,runname,samplesheet,rundir,outdir,logdir,basesmask,mismatches,threads,test,verbose)

    def run(self):  
        logger    = logging.getLogger('Illumina')
        #self.Run.log('Running bcl2fastq...')

        command = 'source new-modules.sh; module load legacy/0.0.1-fasrc01; module load bcl2fastq2; echo "Using bcl2fastq: "; which bcl2fastq; '

        command += 'bcl2fastq --runfolder-dir '      + self.rundir \
                          + ' --barcode-mismatches ' + str(self.mismatches) \
                          + ' --output-dir '         + self.outdir \
                          + ' --use-bases-mask '     + self.basesmask

        #if self.Run.maskShortAdapterReads:
        #    command += ' --mask-short-adapter-reads ' + str(self.Run.maskShortAdapterReads)

        #if self.Run.minTrimmedReadLength is not None:
        #    command += ' --minimum-trimmed-read-length ' + str(self.Run.minTrimmedReadLength)

        command += '; '

        print "Command is ["+command+"]"

        logger.info(command) 

        outfile = os.path.join(self.logdir,"run."+self.runname+".log")

        print command

        if not self.test:
          self.shell(command, outfile)
