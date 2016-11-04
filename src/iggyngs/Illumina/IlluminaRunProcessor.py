import sys, re, os, pprint, logging, shutil

from iggyngs.IlluminaRunName                  import IlluminaRunName

from iggyngs.io.RunInfoFile                   import RunInfoFile

from iggyngs.io.HiSeqSampleSheetFile          import HiSeqSampleSheetFile
from iggyngs.io.NextSeqSampleSheetFile        import NextSeqSampleSheetFile

from iggyngs.HiSeqBclToFastqAnalysis          import HiSeqBclToFastqAnalysis
from iggyngs.NextSeqBclToFastqAnalysis        import NextSeqBclToFastqAnalysis

class IlluminaRunProcessor(object):

  def __init__(self,runname):
    self.logger = self.getLogger()

    self.logger.info('Starting Illumina processing for run [' + runname + ']')
    self.runstring     = "["+runname+"] "

    self.setRunName(runname)

  def validateInput(self):

    logger    = self.logger
    runstring = self.runstring

    if not self.runname:
      logger.error("Run name not specified")
      raise Exception("Run name not specified")

    if not self.parentindir:
      logger.error("Parent input directory not specified")
      raise Exception("Parent input directory not specified")

    if not self.parentoutdir:
      logger.error("Parent output directory not specified")
      raise Exception("Parent output directory not specified")

    if not os.path.exists(self.parentindir):
      logger.error("Parent input directory doesn't exist [%s]"%self.parentindir)
      raise Exception("Parent input directory [%s] doesn't exist"%self.parentindir)

    if not os.path.exists(self.parentoutdir):
      logger.error("Parent output directory doesn't exist [%s]"%self.parentoutdir)
      raise Exception("Parent output directory [%s] doesn't exist"%self.parentindir)

  def setRunName(self,runname):

    self.runname          = runname
    self.runstring        = "["+runname+"] "

    logger    = self.logger
    runstring = self.runstring 

    logger.info(runstring + "Creating IlluminaRunName object from [%s]"%runname)

    self.runnameobj       = IlluminaRunName(runname)
    self.runType          = self.runnameobj.runType

  def setRunInfoFile(self,runinfofile):
 
    logger    = self.logger
    runstring = self.runstring 

    logger.info(runstring + "Choosing RunInfoFile [%s]"%runinfofile)

    if not os.path.isfile(runinfofile):
      logger.error(runstring + "RunInfoFile [%s] doesn't exist"%runinfofile)
      raise Exception("RunInfoFile [%s] doesn't exist"%runinfofile)

    logger.info(runstring + "Creating RunInfo File Object[%s]"%runinfofile)
    runinfo          = RunInfoFile(runinfofile)

    logger.info(runstring + "Parsing RunInfo File [%s]"%runinfofile)
    runinfo.parse() 

    self.runinfo = runinfo 

  def setSampleSheetFile(self,samplesheetfile=None):

    logger    = self.logger
    runstring = self.runstring

    # Create the default samplesheet file from the run directory
    if not samplesheetfile:
      samplesheetfile = os.path.join(self.parentindir,self.runname,"SampleSheet.csv")
      logger.info(runstring + "Choosing default samplesheet file [%s]"%samplesheetfile)

    # Check the samplesheet file exists
    if not os.path.isfile(samplesheetfile):
      logger.error(runstring + "Samplesheet file [%s] doesn't exist"%samplesheetfile)
      raise Exception("Samplesheet file [%s] doesn't exist"%samplesheetfile)

    logger.info(runstring + "Creating SampleSheet object from [%s]"%samplesheetfile)

    # Create the samplesheet according to the run type
    if self.runType == "HiSeq": 
      samplesheet      = HiSeqSampleSheetFile(samplesheetfile)
    elif self.runType == "NextSeq":
      samplesheet      = NextSeqSampleSheetFile(samplesheetfile)
    else:
      raise Exception("Unknown runtype [%s] from run anme [%s]"%(runType,runname))

    # Finally parse the samplesheet - this extracts sample,submission,lane and index data
    logger.info(runstring + "Parsing samplesheet file [%s]"%samplesheetfile)
    samplesheet.parse()

    self.samplesheetfile = samplesheetfile
    self.samplesheet     = samplesheet

  def setOutputDir(self,outdir):

    """ Creates the output directory.   If it exists then will delete the existing if the --force option is present"""

    logger    = self.logger
    runstring = self.runstring
    force     = self.force

    logger.info(runstring + "Output directory is [%s}"%outdir)

    # Checks for existence and deletes if --force option is set
    if os.path.exists(outdir):

      if not force:
        msg = runstring + "Old output directory exists.  Use the --force option to overwrite or remove [%s}"%outdir
        logger.error(msg)
        exit(msg)
      else:
        try:
          logger.info(runstring + "Removing old output directory [%s}"%outdir)
          shutil.rmtree(outdir) 
        except OSError as err:
          msg =  runstring + "Error removing existing output directory [%s]"%err
          logger.error(msg)
          exit(msg)


    # Creates the output directory and sets permissions to 0755
    try:
      logger.info(runstring + "Making output directory is [%s}"%outdir)
      os.mkdir( outdir, 0775 );
    except OSError as err:
      msg = runstring + "Error making output directory [%s]"%err
      logger.error(msg)
      exit(msg)

    return outdir

  def setParentIndir(self,dir):

    """ The parent input directory.  Doesn't do a check for existence here"""

    self.parentindir = dir
    self.rundir          = os.path.join(self.parentindir,self.runname)

  def setParentOutdir(self,dir):

    """ The parent output directory.  Doesn't do a check for existence here"""

    self.parentoutdir = dir
    self.outdir          = os.path.join(self.parentoutdir,self.runname)

    self.setOutputDir(self.outdir)

  def getLogger(self):

    fh        = logging.FileHandler('/tmp/Illumina.log')
    logger    = logging.getLogger('Illumina')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    fh.setFormatter(formatter)

    logger.addHandler(fh) 
    logger.setLevel(logging.INFO)

    return logger 


