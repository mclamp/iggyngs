import os, re, logging, shutil, time

from datetime import datetime

class AnalysisStatus(object):

    status     = []
    timestamp  = []
    
    def __init__(self,status="NEW",timestamp=None):

        self.status = []
        self.timestamp= []
        self.addStatus(status)


    def addStatus(self,status,timestamp=None):

        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%m:%S")

        self.status.append(status)
        self.timestamp.append(timestamp)

    def getCurrentStatus(self):
        return self.status[-1]

    def getCurrentTimestamp(self):
        return self.timestamp[-1]

    
                            

       
      
     
 
