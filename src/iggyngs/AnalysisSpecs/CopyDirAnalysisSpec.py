import os, re, logging, shutil

from iggyngs.AnalysisSpecs.AnalysisSpec import AnalysisSpec 


class CopyDirAnalysisSpec(AnalysisSpec):
    srcdir    = None
    destdir   = None
    overwrite = False

    def __init__(self):
       AnalysisSpec.__init__(self)
       
       self.name      = "CopyDir"
       
       self.logger    = logging.getLogger("IggyNGS")
       


    def init(self):
        if len(self.inputs) == 1:
            self.srcdir  = self.inputs[0]

        if len(self.outputs) == 1:
            self.destdir = self.outputs[0]

        if 'overwrite' in self.params:
            self.overwrite = self.params['overwrite']
            
    def checkDirectories(self):
        
       if not os.path.exists(self.srcdir):
          self.logger.info("Source directory [%s] doesn't exist. Can't create CopyDirAnalysis"%self.srcdir)
          raise Exception ("Source directory [%s] doesn't exist. Can't create CopyDirAnalysis"%self.srcdir)

       if not self.overwrite and os.path.exists(self.destdir):
          self.logger.info("Destination directory [%s] exists. Can't create CopyDirAnalysis without overwrite options"%self.destdir)
          raise Exception ("Destination directory [%s] exists. Can't create CopyDirAnalysis without overwrite options"%self.destdir)

    def run(self):
        self.status.addStatus("RUNNING")

        try:

         self.checkDirectories()
        
         if not self.test:
            if self.overwrite and os.path.exists(self.destdir):
                self.logger.info("Removing existing destination directory [%s]"%self.destdir)
                shutil.rmtree(self.destdir)
            elif not self.overwrite and os.path.exists(self.destdir):
                self.logger.info("Copy directory exists - can't copy without overwrite flag")
                raise Exception("Copy directory exists - can't copy without overwrite flag")
            
            shutil.copytree(self.srcdir, self.destdir) 
         else:
            print "****** Test run only for copying directories ******"
            self.logger.info("****** Test run only for copying directories ******")


     
         self.status.addStatus("COMPLETE")
        
        except Exception as e:
            self.logger.info("ERROR in %s Analysis Module [%s]"%(self.name,e))
            print "ERROR in %s Analysis [%s]"%(self.name,e)
            self.status.addStatus("FAILED")
            

        
    def makeCommands(self):
       pass
       
      
     
 
