import os, re, logging

class FastQCDataFile(object):
 
    def __init__(self,file):

        self.file = file
   
        if not os.path.exists(file):
           raise Exception("FastQC data file [%s] doesn't exist.  Can't parse"%file)

        self.parse()
        self.postProcessOutput()
 
    def postProcessOutput(self):

        encoding  = None
        readlen   = None
        numseqs   = None
        filename  = None
        percentgc = None

        status    = self.data['Basic Statistics']['status']

        for row in self.data['Basic Statistics']['moddata']:
            key   = row[0]
            value = row[1]

            if key == "Encoding":
                encoding = value
            elif key == "Sequence length":
                readlen = value
            elif key == "Total Sequences":
                numseqs = value
            elif key == "Filename":
                filename = value
            elif key == "%GC":
                percentgc = value

        tmpdat = {}
        
        tmpdat['Encoding']        = encoding
        tmpdat['Sequence Length'] = readlen
        tmpdat['Filename']        = filename
        tmpdat['%GC']             = percentgc
        tmpdat['Total Sequences'] = numseqs
        
        self.summary_data  = tmpdat
        self.output_status = status

        status = self.data['Basic Statistics']['status']

    def parse(self):

        """ Data format looks like sets of
        >>Basic Statistics      pass
        #Measure        Value   
        Filename        sample_1.fq     
        File type       Conventional base calls 
        Encoding        Illumina 1.5    
        Total Sequences 750000  
        Filtered Sequences      0       
        Sequence length 36      
        %GC     43      
        >>END_MODULE
        """

        file   = self.file
        data   = {}
        name   = None

        in_data_section = False

        with open(file) as fp:

            for line in fp:

                line = line.rstrip('\n')

                match1 = re.match('\>\>(.*)',line)               # Look for an end line

                if match1:

                    tmpstr = match1.group(1)

                    if tmpstr == "END_MODULE":                   
                    
                        in_data_section = False

                        name   = None
                        status = None

                match2 = re.match('\>\>(.*)\t(.*)',line)        # Look for a start line

                if match2:                                       
                    name    = match2.group(1)
                    status  = match2.group(2)
                    
                    in_data_section = True
                    
                    data[name] = {}
                    data[name]['status'] = status
                    data[name]['moddata']   = []

                else:
                    if in_data_section:                         # Read data line otherwise

                        # If we start with hash then we have a header
                    
                        match3 = re.match('^#(.*)',line)

                        if match3:

                            tmpstr = match3.group(1)
                            header = tmpstr.split('\t')
                            
                            data[name]['header'] = header
                            
                        else :      
                            moddata = line.split('\t')
                            data[name]['moddata'].append(moddata)

        self.data = data
                    
