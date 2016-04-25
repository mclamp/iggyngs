from abc import ABCMeta, abstractmethod
from os import path

import re, logging

from iggyngs.IlluminaLane              import IlluminaLane
from iggyngs.io.SampleSheetFile        import SampleSheetFile


try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict # for python 2.6 and earlier, use backport

class HiSeqSampleSheetFile(SampleSheetFile):
    
    def __init__(self, file):
        SampleSheetFile.__init__(self, file)

    def parse(self):

        seenLaneIndices = list()

        # Example header line: FCID,Lane,SampleID,SampleRef,Index,Description,Control,Recipe,Operator,SampleProject

        colNames = [x.lower() for x in self.ss[0].rstrip().split(',')] 

        for i in range(1,len(self.ss)): 

            line     = self.ss[i].rstrip()
            lineVals = line.split(',')

            if not any(lineVals):                             # skip lines containing only commas
                continue   

            vDict     = OrderedDict(zip(colNames, lineVals))  # dict keys are column names

            laneName  = vDict['lane']
            index     = vDict['index']
            subID     = vDict['description']
            indexType = vDict['recipe']                       # Examples: '6' for a 6-base index; '8_8' for two indices where each is 8 bases.

            vDict['sampleproject'] = 'Fastq_Files'                              # Reset project field, as this will create uniform output directory stucture for all runs
            vDict['sampleid']      = re.sub(r'[- .)(@]','_',vDict['sampleid'])  # Replace illegal characters in sample name with underscores

            # Error checking and validation

            self.validate_indexChars(index, i)
            self.validate_indexTypeChars(indexType, i)
            self.validate_subIDChars(subID, i)

            if not re.match('[1-8]$', laneName): 
                raise Exception('Unexpected lane in samplesheet %s, line %s: %s' % (self.file, i+1, line))

            if laneName + index in seenLaneIndices:
                raise Exception('Duplicate index in samplesheet %s, line %s: %s' % (self.file, i+1, line))
            else:
                seenLaneIndices.append(laneName + index)

            # Extract index strings from index field
            iMatch = re.match('(?P<index1>[AGCTagct]+)(-(?P<index2>[AGCTagct]+))?$', index)

            if not iMatch or iMatch.group('index1') is None:
                logger = logging.getLogger("Illumina")  
                logger.info('No index found in samplesheet %s, line %s: %s' % (self.file, i+1, line))
                index1 = ''
                index2 = ''
            else:    
                index1 = iMatch.group('index1')
                if index1 is None:
                    index1 = ''

                index2 = iMatch.group('index2')
                if index2 is None:
                    index2 = ''

            if not indexType:  #make indexType label if it was not specified 
                indexType = str(len(index1))
                if len(index2) > 0:
                    indexType += '_' + str(len(index2))

            else:  #adjust index lengths according to specified indexType

                tMatch = re.match('(?P<rlen1>[0-9]+)((_|-)(?P<rlen2>[0-9]+))?$', indexType) # 'rlen' denotes 'real length'

                if tMatch:

                    rlen1 = tMatch.group('rlen1')
                    rlen2 = tMatch.group('rlen2')

                    if rlen2 is None:
                        rlen2 = 0

                    index1 = self.adjustIndexLength(index1, rlen1)  #shorten or lengthen indices
                    index2 = self.adjustIndexLength(index2, rlen2)

                    vDict['index'] = index1  #update index in vDict

                    if index2:
                        vDict['index'] += '-' + index2

            ##
            # Lane Obj
            ##

            if laneName not in [x.userLaneLabel for x in self.lanes]:
                lane = self.makeNewLane(laneName)  #start new lane

            #set lane index1 length to maximum of index1 real lengths
            if not lane.index1Length or rlen1 > lane.index1Length:
                lane.index1Length = rlen1

            #set lane index2 length to maximum of index2 real lengths
            if not lane.index2Length or rlen2 > lane.index2Length:
                lane.index2Length = rlen2

            lane.ssSampleLines.append(vDict)  #assign sample line to this lane
            lane.ssLineIndices.append(i)      #record lines in samplesheet that correspond to this lane                                                  

            if subID and subID not in lane.subIDs:
                lane.subIDs.append(subID)  #add subID to this lane

    def writeLane(self,outfile,userLaneLabel):
       with open(outfile, 'w') as fh:

            # Write the header line
            fh.write(self.ss[0] + '\n')

            for l in self.lanes:
                 #if int(l.userLaneLabel) == int(userLaneLabel):
                 if str(l.userLaneLabel) == str(userLaneLabel):
                   for line in l.ssLineIndices:
                      fh.write(self.ss[line] + '\n')
