import os, re, logging, shutil

from iggyngs.AnalysisSpecs.AnalysisSpec import AnalysisSpec 

class CopyDirAnalysisSpec(AnalysisSpec):
    srcdir    = None
    destdir   = None
    overwrite = False

    def __init__(self,srcdir,destdir,overwrite=False):
       AnalysisSpec.__init__(self)
       
       self.srcdir    = srcdir
       self.destdir   = destdir
       self.overwrite = overwrite

       self.checkDirectories()

    def checkDirectories(self):
       logger = logging.getLogger("Illumina")

       if not os.path.exists(self.srcdir):
          logger.info("Source directory [%s] doesn't exist. Can't create CopyDirAnalysis"%self.srcdir)
          raise Exception ("Source directory [%s] doesn't exist. Can't create CopyDirAnalysis"%self.srcdir)

       if not self.overwrite and os.path.exists(self.destdir):
          logger.info("Destination directory [%s] exists. Can't create CopyDirAnalysis without overwrite options"%self.destdir)
          raise Exception ("Destination directory [%s] exists. Can't create CopyDirAnalysis without overwrite options"%self.destdir)

    def run(self):

       logger = logging.getLogger("Illumina")

       if not self.test:
         if self.overwrite and os.path.exists(self.destdir):
            logger.info("Removing existing destination directory [%s]"%self.destdir)
            shutil.rmtree(self.destdir)

         shutil.copytree(self.srcdir, self.destdir) 
       else:
         print "****** Test run only for copying directories ******"
         logger.info("****** Test run only for copying directories ******")

    def makeCommands(self):
       pass
       
      
     
 
