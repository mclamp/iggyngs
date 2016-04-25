import logging

class IlluminaLane(object):

    def __init__(self):

        self.index1Length = None
        self.index2Length = None

        self.subIDs = list()

        self.ssSampleLines = list()
        self.ssLineIndices = list()
        
        self.userLaneName = None
        self.machineLaneName = None

    def makeIndexString(self):
     indexstring = ""

     if self.index1Length is not None:
        indexstring = self.index1Length

     if self.index2Length is not None and self.index2Length != 0:
        indexstring = str(indexstring) + "_" + str(self.index2Length)

     return indexstring

    def makeBasesMask(self,runinfodict):
        logger = logging.getLogger("Illumina")

        index1Length = int(self.index1Length)
        index2Length = int(self.index2Length)

        #print "Index lengths %d %d"%(index1Length,index2Length)

        runinfo_index_numcycles = list()

        basesMask = 'Y' + str( int(runinfodict['Read1']['num_cycles']) - 1 ) + 'N'  #Read1 is never an index

        if 'Read2' in runinfodict.keys():

            if runinfodict['Read2']['is_index'] == 'Y': #then Read2 is an index

                read2_numcycles = int(runinfodict['Read2']['num_cycles'])

                if index1Length > 0:
                    basesMask += ',I' + str(index1Length) + 'N' * (read2_numcycles - index1Length)
                else:
                    basesMask += ',' + 'N' * read2_numcycles

                #print "Appending %d"%read2_numcycles
                runinfo_index_numcycles.append(read2_numcycles)

            else: #then Read2 is not an index
                basesMask += ',Y' + str( int(r['Read2']['num_cycles']) - 1 ) + 'N'

            if 'Read3' in runinfodict.keys():

                if runinfodict['Read3']['is_index'] == 'Y': #then Read3 is an index
                    read3_numcycles = int(runinfodict['Read3']['num_cycles'])

                    if index2Length > 0:
                        basesMask += ',I' + str(index2Length) + 'N' * (read3_numcycles - index2Length)

                    else:
                        basesMask += ',' + 'N' * read3_numcycles

                    runinfo_index_numcycles.append(read3_numcycles)

                else: #then Read3 is not an index
                    basesMask += ',Y' + str( int(runinfodict['Read3']['num_cycles']) - 1 ) + 'N'

                if 'Read4' in runinfodict.keys(): #Read4 is never an index
                    basesMask += ',Y' + str( int(runinfodict['Read4']['num_cycles']) - 1 ) + 'N'

        # Check if index lengths in samplesheet and runinfo file agree
        #print "Index 1 length %d"%index1Length
        #for i in runinfo_index_numcycles:
        #    print ("%d %s"%(i,runinfo_index_numcycles[0]))


        #print "Done"
        #if (index1Length > 0 or len(runinfo_index_numcycles) > 0) \
        #        and index1Length not in [ runinfo_index_numcycles[0], runinfo_index_numcycles[0] - 1 ]:
        #    self.warnings.append('In analysis %s: Unusual combination of samplesheet index length and runinfo num cycles for 1st index. Index length: %s. RunInfo num cycles: %s'
        #                    % (self.name, index1Length, runinfo_index_numcycles[0]))

        if (index2Length > 0 or len(runinfo_index_numcycles) > 1) \
                and index2Length not in [ runinfo_index_numcycles[1], runinfo_index_numcycles[1] - 1 ]:

            logger.info('Unusual combination of samplesheet index length and runinfo num cycles for 2nd index. Index length: %s. RunInfo num cycles: %s'
                            % (index2Length, runinfo_index_numcycles[1]))
            logger.info('Unusual combination of samplesheet index length and runinfo num cycles for 2nd index. Index length: %s. RunInfo num cycles: %s'
                            % (index2Length, runinfo_index_numcycles[1]))

        return basesMask


