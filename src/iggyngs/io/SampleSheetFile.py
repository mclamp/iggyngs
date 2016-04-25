from abc import ABCMeta, abstractmethod
from os import path
from iggyngs.IlluminaLane import IlluminaLane

import re

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict # for python 2.6 and earlier, use backport                                                                                                   

class SampleSheetFile:

    __metaclass__ = ABCMeta

    def __init__(self, file):

        self.file                     = file 

        self.nonIndexRead1_numCycles  = None  # Non-index read lengths are not provided in samplesheet format A.
        self.nonIndexRead2_numCycles  = None

        self.lanes                    = list()
        self.lanelabels               = {}

        with open(self.file,'r') as fh:
            ss = fh.readlines()

        ss = [ re.sub('\s', '', x) for x in ss if x.rstrip()]         # delete blank lines and other whitespace
        ss = [ re.sub(r'[)(]', '_', x) for x in ss ]                  # replace illegal characters with underscores

        self.ss = [ re.sub(r'(?<=[^AGCTNagtcn]{2})-(?=[^AGCTNagtcn]{2})', '_', x) for x in ss]  #replace dashes with underscores unless they may be in a dual index


    @abstractmethod
    def parse(self):
        pass


    def validate_indexChars(self, index, lineIndex):
        if not re.match('[AGCT-]*$', index):
            raise Exception('Unexpected index in samplesheet %s, line %s: %s' % (self.file, lineIndex+1, index))


    def validate_indexTypeChars(self, indexType, lineIndex):
        if not re.match('[0-9]+([-_][0-9]+)?$', indexType):
            raise Exception('Unexpected indexType in samplesheet [%s], line [%s]: [%s]' % (self.file, lineIndex+1, indexType))


    def validate_subIDChars(self, subID, lineIndex):
        if not re.match('SUB[A-Za-z0-9]+$', subID):
            raise Exception('Unexpected subID in samplesheet %s, line %s: %s' % (self.file, lineIndex+1, subID))


    def adjustIndexLength(self, index, rlen):
        rlen = int(rlen)
        if len(index) < rlen: #then lengthen index
            index += 'A' * (rlen - len(index))
        elif len(index) > rlen: #then shorten index
            index = index[:rlen]
        return index


    def makeNewLane(self, userLaneLabel):
        
        lane = IlluminaLane()
        lane.userLaneLabel = userLaneLabel

        self.lanes.append(lane)
        self.lanelabels[userLaneLabel] = lane

        return lane

    @abstractmethod
    def writeLane(self,outfile,userLaneLabel):
        pass 
