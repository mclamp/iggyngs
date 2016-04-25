import os, re, traceback, imp

class IlluminaRunName:
     
    def __init__(self, runName):

      match = re.match('([0-9]{6})_([0-9A-Za-z]+)_([0-9A-Za-z]+)_([0-9A-Za-z]{10})$', runName) #re.match matches from beg. of string

      if not match:
        return None

      self.runName           = match.group(0)
      self.date              = match.group(1)
      self.machineID         = match.group(2)
      self.counter           = match.group(3)
      self.pos_and_flowcell  = match.group(4)
      self.pos               = match.group(4)[0]
      self.flowcell          = match.group(4)[-9:]

      match = re.match('NS',self.machineID)

      if match:
         self.runType = "NextSeq"
      else:
         self.runType = "HiSeq"
   
