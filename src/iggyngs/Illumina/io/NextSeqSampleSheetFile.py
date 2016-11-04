from abc import ABCMeta, abstractmethod
from os import path

import re

from iggyngs.IlluminaLane              import IlluminaLane
from iggyngs.io.SampleSheetFile        import SampleSheetFile

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict # for python 2.6 and earlier, use backport

#[Header],,,,,,,,,
#IEMFileVersion,4,,,,,,,,
#InvestigatorName,caseydulong@gmail.com,,,,,,,,
#ExperimentName,SUB03914,,,,,,,,
#Date,4/15/2016,,,,,,,,
#Workflow,GenerateFASTQ,,,,,,,,
#Application,NextSeqFASTQOnly,,,,,,,,
#Assay,TruSeqLT,,,,,,,,
#Description,SUB03914,,,,,,,,
#Chemistry,Amplicon,,,,,,,,
#,,,,,,,,,
#,,,,,,,,,
#[Reads],,,,,,,,,
#151,,,,,,,,,
#151,,,,,,,,,
#,,,,,,,,,
#,,,,,,,,,
#[Settings],,,,,,,,,
#Adapter,AGATCGGAAGAGCACACGTCTGAACTCCAGTCA,,,,,,,,
#AdapterRead2,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT,,,,,,,,
#,,,,,,,,,
#[Data],,,,,,,,,
#Sample_ID,Sample_Name,Sample_Plate,Sample_Well,I7_Index_ID,index,I5_Index_ID,index2,Sample_Project,Description
#1-1,1_1,,,,TAAGGCGA,,GCGATCTA,,
#1-2,1_2,,,,CGTACTAG,,GCGATCTA,,
#1-3,1_3,,,,AGGCAGAA,,GCGATCTA,,
#1-4,1_4,,,,TCCTGAGC,,GCGATCTA,,
#1-5,1_5,,,,GGACTCCT,,GCGATCTA,,

class NextSeqSampleSheetFile(SampleSheetFile):
    
    def __init__(self, file):
        SampleSheetFile.__init__(self, file)

    def parse(self):

        self.sections = {}
        self.headerIndex = None
        self.headers     = None
 
        section = None
        ssdata  = None

        for i in range(len(self.ss)):

            line = self.ss[i]
            vals = line.split(',')

            # print "LINE %s"%line

            if not any(vals):                                # Skip empty lines with only commas
                continue              

            match1 = re.match('\[(.*)\]',vals[0])            # Test for section header

            if match1:
               section = match1.group(1)
               self.sections[section] = {}
            else:                                            # Else we have section data
               if section == "Data":
                  if self.headers is None:
                    self.headers                      = vals 
                    self.sections[section]['samples'] = []
                    self.headerIndex                  = i
                  else:
                    vDict = OrderedDict(zip(self.headers, vals))  #convert list of values to dict where keys are column names
                    self.sections[section]['samples'].append(vDict)
               elif section == "Reads":
                  if "Readlen" not in self.sections[section]:
                     self.sections[section]['Readlen'] = []

                  self.sections[section]['Readlen'].append(vals[0])
               else:
                  self.sections[section][vals[0]] = vals[1]

        # Now we have the data - Extract read lengths 
        try:
           lenarr = self.sections['Reads']['Readlen']

           if len(lenarr) >= 1:
              self.rlen1 = self.sections['Reads']['Readlen'][0]

           if len(lenarr) >= 2:
              self.rlen2 = self.sections['Reads']['Readlen'][1]
        except Exception as e:
           raise e

        # Get Submissions from hdear
        try:
           self.headerSubIDs = self.sections['Header']['ExperimentName']
       
        except Exception as e:
           raise e

        # Loop over all the data lines and make lanes
        try:

           headers = self.headers
           data    = self.sections['Data']['samples']

           i = self.headerIndex+1

           for d in data:
                lane = 'NoLane'

                if 'lane' in headers:
                    lane = d['lane']
                    if self.selectedLanes and lane not in self.selectedLanes:
                        continue

                if 'index' in headers:
                    index1 = d['index']
                    self.validate_indexChars(index1, i)
                else:
                    index1 = ''
                    self.warnings.append('No index1 found in samplesheet %s, Line %s: %s' % (self.file, i+1, line))

                if 'index2' in headers:
                    index2 = d['index2']
                    self.validate_indexChars(index2, i)
                else:
                    index2 = ''

                if lane == 'NoLane':
                    userLaneLabel = '1'
                else:
                    userLaneLabel = lane

                if userLaneLabel not in self.lanelabels:
                    laneobj = self.makeNewLane(userLaneLabel) #start new Lane
                else:
                    laneobj = self.lanelabels[userLaneLabel]

                rlen1 = len(index1)  #initialize "real" index lengths to index lengths before adjustment
                rlen2 = len(index2)

                #get real index lengths and submission IDs from description column, if present
                lineSubID = ''
                if 'description' in headers and d['description']:
                    elems = re.split('_|-', d['description'])

                    for j in range(len(elems)):
                        if re.match('SUB', elems[j], re.IGNORECASE):
                            subID = elems[j]
                            elems.remove(subID)
                            lineSubID = subID.upper()

                    if len(elems) > 2:
                        self.warnings.append('Too many values in description field in samplesheet %s, Line %s: %s' % (self.file, i+1, line))
                    elif len(elems) > 0 and elems[0].isdigit():
                        rlen1 = elems[0]

                        if len(elems) == 2 and elems[1].isdigit():
                            rlen2 = elems[1]

                        #shorten or lengthen indices according to rlen1 and rlen2
                        if rlen1 != len(index1):
                            index1 = self.adjustIndexLength(index1, rlen1)
                        if rlen2 != len(index2):
                            index2 = self.adjustIndexLength(index2, rlen2)

                #set lane index1 length to maximum of index1 real lengths
                if not laneobj.index1Length or rlen1 > laneobj.index1Length:
                    laneobj.index1Length = rlen1

                #set lane index2 length to maximum of index2 real lengths
                if not laneobj.index2Length or rlen2 > laneobj.index2Length:
                    laneobj.index2Length = rlen2

                indexType = str(rlen1)  #make index type label

                if rlen2 > 0:
                    indexType += '_' + str(rlen2)
                self.indexType = indexType

                laneobj.ssSampleLines.append(d)   #assign sample line to this lane
                laneobj.ssLineIndices.append(i)       #record lines in samplesheet that correspond to this lane

                #assign this line's subID to lane and analysis
                if lineSubID:
                    if lineSubID not in laneobj.subIDs:
                        laneobj.subIDs.append(lineSubID)

                    if lineSubID not in analysis.subIDs:
                        analysis.subIDs.append(lineSubID)

                else:
                    #use header's subID(s) if no others were provided on this line
                    laneobj.subIDs     = self.headerSubIDs

                # Build validated samplesheet line
                if d:
                  self.ss[i] = ','.join( [d[x] for x in self.headers] )
                else:
                  self.ss[i] = ','.join( vals )

                i = i + 1

        except Exception as e:
           raise
        

    def writeLane(self,outfile,userLaneLabel):
       with open(outfile, 'w') as fh:
            # Write all samplesheet lines up to and including the Data section headers
            i = 0
            while i < self.headerIndex:
              fh.write(self.ss[i] + '\n')
              i = i+1

            for l in self.lanes:
                 #if int(l.userLaneLabel) == int(userLaneLabel):
                 if str(l.userLaneLabel) == str(userLaneLabel):
                   for line in l.ssLineIndices:
                      fh.write(self.ss[line] + '\n')
