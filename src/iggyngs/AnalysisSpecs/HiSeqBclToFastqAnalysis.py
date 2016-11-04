import os, re, logging

from iggyngs.io.SampleSheetFile        import SampleSheetFile    
from iggyngs.BclToFastqAnalysis        import BclToFastqAnalysis

class HiSeqBclToFastqAnalysis(BclToFastqAnalysis):

    def __init__(self,runname,samplesheet,rundir,outdir,logdir,basesmask,mismatches,threads,test=True,verbose=True):
        BclToFastqAnalysis.__init__(self,runname,samplesheet,rundir,outdir,logdir,basesmask,mismatches,threads,test,verbose)

    def makeCommands(self):  
        logger    = logging.getLogger('Illumina')

        command = 'source new-modules.sh; module load legacy/0.0.1-fasrc01; module load centos6/bcl2fastq-1.8.3 \n' + \
                  'echo "Using configureBclToFastq.pl:"; which configureBclToFastq.pl\n\n'

        indir = os.path.join(self.rundir,"Data","Intensities","BaseCalls")

        command += 'configureBclToFastq.pl --input-dir ' + indir                         + ' \\\n' \
                                       + ' --output-dir ' + self.outdir                       + ' \\\n' \
                                       + ' --sample-sheet ' + self.samplesheet                + ' \\\n' \
                                       + ' --use-bases-mask ' + self.basesmask                + ' \\\n' \
                                       + ' --mismatches ' + str(self.mismatches)  + ' \\\n' \
                                       + ' --ignore-missing-stats'                       + ' \\\n'

        # These need to come from somewhere
        #if self.Run.ignoreMissingBcl:
        #    command += ' --ignore-missing-bcl \\\n'

        #if self.Run.ignoreMissingControl:
        #    command += ' --ignore-missing-control \\\n'

        #if self.Run.withFailedReads:
        #    command += ' --with-failed-reads \\\n'

        #if self.Run.tileRegex:
        #    command += " --tiles '" + self.Run.tileRegex + "' \\\n"

        command += '\n'  #end line continuation

        command += 'cd ' + self.outdir + '; make -j ' + str(self.threads) + '\n'

        print "Command is ["+command+"]"

        logger.info(command) 

        outfile = os.path.join(self.logdir,"run."+self.runname+".log")

        print command

        self.commands.append(command)
        self.outfiles.append(outfile)

