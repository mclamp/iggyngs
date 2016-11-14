import re, os, sys, logging, sqlite3

from   datetime                           import datetime
from   iggyngs.config                     import settings
from   iggyngs.AnalysisSpecs.AnalysisSpec import AnalysisSpec

""" Class that creates/saves Analysis objects """

class AnalysisDB(object):


    def __init__(self,dbname):

        self.connect(dbname)
        
        if not self.existsAnalysisTables():
            self.createAnalysisTables()



    def saveAnalysis(self,anaobj):
        
        logging.info(" ========> AnalysisDB Saving analysis : %-30s ID %-5s : Status : %-30s" % (anaobj.name,anaobj.id,anaobj.status.getCurrentStatus()))

        with self.con:

            self.updateAnalysisTable(anaobj)                           # Update the main Analysis table

            self.deleteLinkedAnalysisData(anaobj)                      # Delete from the other tables before inserting afresh 

            self.saveLinkedAnalysisData(anaobj)                        # Aave the rest of the data to the other tables

            self.con.commit()

            
    def existsAnalysisTables(self):
        tables = self.getTables()

        if len(tables) == 0:
            return False
        else:
            return True
            
    def createAnalysisTables(self):

        try:

            with self.con:
    
                cur = self.executeQuery("DROP TABLE IF EXISTS Analysis")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisInput")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisStatus")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisCommand")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisOutput")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisSummary")
                cur = self.executeQuery("DROP TABLE IF EXISTS AnalysisOutputString")
                
                self.createAnalysisTable()                             # Stores general info about the analysis job
                
                self.createAnalysisLinkedTable("Input")                # Stores the inputs and types (usually files)
                self.createAnalysisLinkedTable("Output")               # Stores the outputs and types (usually files)
                self.createAnalysisLinkedTable("Summary")              # Stores the key/value data pairs that summarize the output from the job
                self.createAnalysisLinkedTable("OutputString")         # Stores the stdout from the commands
                self.createAnalysisLinkedTable("Command")              # Stores the commands that are run
                self.createAnalysisLinkedTable("Status")               # Stores the status and timestamps as the job progresses

        except sqlite3.Error, e:
    
            if self.con:
                self.con.rollback()
        
                raise Exception("Error creating the analysis tables [%s]"%e.args[0])

        return True

    def isNewAnalysis(self,anaobj):

        if anaobj.id == "NULL":
            return True
        else:
            return False
        

    def saveNewAnalysis(self,anaobj):
        
        anaobj.date_created = datetime.now().strftime("%Y-%m-%d %H:%m:%S")
        anaobj.last_updated = anaobj.date_created
                
        sql = "insert into Analysis(Name,CurrentStatus,LastUpdated,DateCreated) values(%s,%s,'%s','%s')" %  (name,current_status,anaobj.date_created,anaobj.date_created)
        cur = self.executeQuery(sql)
                
        anaobj.id = cur.lastrowid

    def updateAnalysis(self,anaobj):
        
        anaobj.last_updated = datetime.now().strftime("%Y-%m-%d %H:%m:%S")
        name                = self.convstr(anaobj.name)
        current_status      = self.convstr(anaobj.status.getCurrentStatus())
        
        sql = "update Analysis set Name=%s, CurrentStatus=%s, LastUpdated='%s'  where ID = %s" %   (name,current_status,anaobj.last_updated,id)
        cur = self.executeQuery(sql)


    def saveAnalysisStatus(self,anaobj):

        i = 0
        
        while i < len(anaobj.status.status):
            statusstr = anaobj.status.status[i]
            timestamp = anaobj.status.timestamp[i]
                
            sql = "insert into AnalysisStatus(AnalysisID,Status,DateCreated) values(%s,'%s','%s')" % (id,statusstr,timestamp)

            cur.execute(sql)

            i = i + 1

    def deleteLinkedAnalysisData(self,anaobj):

        id = self.convstr(anaobj.id)
        
        linkedtables = ["Input","Output","Command","Summary","Status"]

        for t in linkedtables:
            sql = "delete from Analysis"+t+" where AnalysisId = %s" % id
            cur = self.executeQuery(sql)


    def saveLinkedAnalysisData(self,anaobj):

        id            = self.convstr(anaobj.id)                   # The convstr function puts quotes round strings, converts None to 'NULL' and leaves ints alone

        inputs        = self.convstr(anaobj.inputs)
        inputtypes    = self.convstr(anaobj.inputtypes)
        
        outputs       = self.convstr(anaobj.outputs)
        outputtypes   = self.convstr(anaobj.outputtypes)
        
        commands      = self.convstr(anaobj.commands)
        summary       = self.convstr(anaobj.summary)
        
        
        self.saveAnalysisLinkedTable("Input",        id, inputs,   inputtypes)
        self.saveAnalysisLinkedTable("Output",       id, outputs,  outputtypes)
        self.saveAnalysisLinkedTable("Command",      id, commands, None)
        self.saveAnalysisLinkedTable("Summary",      id, summary,  summary.keys())
        
        self.saveAnalysisStatus(anaobj)

    def updateAnalysisTable(self,anaobj):
        
        if self.isNewAnalysis(anaobj):
            
            self.saveNewAnalysis(anaobj)
                
        else:
                
            self.updateAnalysis(anaobj)

            
 

    def existsAnalysisID(self,id):

        cur = self.executeQuery("select * from Analysis where ID = %s"%id)

        rows = cur.fetchall()

        if len(rows) == 1:
            return True
        elif len(rows) > 1:
            raise Exception("More than one analysis row exists for id %s"%id)
        else:
            return False

            
    def fetchLaunchableJobIDs(self,numjobs,analysis):

        logging.info(" ========> AnalysisDB Fetching launchable jobids : %d %s" % (numjobs,analysis))

        try:

            if analysis:

                sql = "select ID from Analysis where CurrentStatus = 'NEW' and Name = '%s' order by DateCreated limit %d"%(analysis,numjobs)

            else:

                sql = "select ID from Analysis where CurrentStatus = 'NEW' order by DateCreated limit %d"%(numjobs)


            cur = self.executeQuery(sql)
        
            rows = cur.fetchall()

            jobids = []

            for r in rows:
                
                jobids.append(int(r[0]))

            return jobids

        except sqlite3.Error, e:
                    
            if self.con:
                self.con.rollback()
                
                logging.error(" ========> AnalysisDB Error fetching %d %s analysis jobs : %s"%(numjobs,analysis,e.args[0]))
                
                raise 


    def fetchAnalysisByID(self,id):

        logging.info(" ========> AnalysisDB Fetching analysis by id : %s" % id)

        try:
            sql = "select * from Analysis where ID = %s" % id

            cur = self.executeQuery(sql)
        
            rows = cur.fetchall()

            if (len(rows) == 1):

                row  = rows[0]
                name = row[1]

                ana = AnalysisSpec()

                ana.id            = id

                ana.name          = row[1]
                ana.current_status= row[2]
                ana.last_updated  = row[3]
                ana.date_created  = row[4]

                ana.status.status    = []
                ana.status.timestamp = []
                
                # Get the data from the linked tables

                tables = ['Input','Output','Command','Summary','Status']
                
                for t in tables:
                    
                    tmpstr = "Analysis"+t
                    query  = "select * from %s where AnalysisID=%d" % (tmpstr,id)

                    cur  = self.executeQuery(query)
                    rows = cur.fetchall()

                    for r in rows:

                        if t == "Command":

                            ana.commands.append(r[2])

                        if t == "Input":

                            ana.inputs.append(r[2])
                            ana.inputtypes.append(r[3])
                            
                        if t == "Output":

                            ana.outputs.append(r[2])
                            ana.outputtypes.append(r[3])
                            
                        if t == "Summary":

                            ana.summary[r[2]] = r[3]

                        if t == "Status":
                            ana.status.status.append(r[2])
                            ana.status.timestamp.append(r[5])
                            
            elif (len(rows) == 0):
                return None

            elif len(rows) > 1:
                logging.error(" ========> AnalysisDB Error fetching analysis. Non unique id %d : %s"%(id,e.args[0]))
                raise Exception("ERROR: analysis id should be unique - multiple rows returned. id is [%d]" % id)


            return ana

        except sqlite3.Error, e:
                    
            if self.con:
                self.con.rollback()
                
                logging.error(" ========> AnalysisDB Error fetching analysis id %d : %s"%(id,e.args[0]))
                
                raise

    """ 

    Helper function to save data to one of the tables linked to analysis (Input,Output,Command,Status,OutputString,Summary)

    """

    def saveAnalysisLinkedTable(self,name,id,data,types):

        rank = 1
        i    = 0

        if name == "Summary" :

            for key,value in data.iteritems():
                key   = self.convstr(key)

                sql = "insert into Analysis"+name+"(AnalysisID,"+name+","+name+"Type,"+name+"Rank) values(%s,%s,%s,%d)" % (id,value,key,rank)

                cur = self.executeQuery(sql)
                self.con.commit()

                rank = rank + 1
        else:
            for dat in data:

                # Set the type to NULL if we don't have a types array

                dattype = "NULL"
                tmpdat  = dat

                if types and len(types) > i:
                    dattype = types[i]

                sql = "insert into Analysis"+name+"(AnalysisID,"+name+","+name+"Type,"+name+"Rank) values(%s,%s,%s,%d)" % (id,tmpdat,dattype,rank)
            
                cur = self.executeQuery(sql)
                self.con.commit()

                rank = rank + 1
                i    = i    + 1


    def createAnalysisTable(self):

        tmpstr = """CREATE TABLE Analysis(ID            INTEGER primary key,
                                          Name          TEXT, 
                                                    
                                          CurrentStatus TEXT default "NEW",

                                          LastUpdated   DATETIME default current_timestamp,
                                          DateCreated   DATETIME default current_timestamp)"""

        cur = self.executeQuery(tmpstr.strip('\n'))

                      
    def createAnalysisLinkedTable(self,name):
        tmpstr = """CREATE TABLE Analysis"""+name+"""(  ID          INTEGER primary key,
                                                       AnalysisID  INT,
                                                       """+name+"""       TEXT,
                                                       """+name+"""Type   TEXT,
                                                       """+name+"""Rank   INT,
                                                       DateCreated DATETIME default current_timestamp)"""

        cur = self.executeQuery(tmpstr.strip('\n'))


    """

    Utility function to execute some sql and rollback with an error if it fails.
    It returns a cursor so rows can be retrieved.


    """
        
    def executeQuery(self,sql):
        logging.info(" ========> AnalysisDBSQL Query string %s"%(sql))

        try:
            cur = self.con.cursor()
            cur.execute(sql)

            return cur
            
        except sqlite3.Error, e:
                    
            if self.con:
                self.con.rollback()
                
                raise

    """ 

    This utility function is to convert None into 'NULL' strings into 'mysql' and leave ints alone 

    """

    def convstr(self,tmpstr):

        if isinstance(tmpstr,dict):

            newstr = {}

            for key,val in tmpstr.iteritems():

                if val is None:
                  newstr[key] = "NULL"
                elif isinstance(val,int):
                    newstr[key] = val
                else:
                    newstr[key] = "'"+val+"'"

            return newstr

        elif isinstance(tmpstr,list):

            newstr = []

            for i,t in enumerate(tmpstr):
                if t is None:
                    newstr.append('NULL')
                elif isinstance(t,int):
                    newstr.append(t)
                else:
                    newstr.append("'"+t+"'")

            return newstr

        else:
            if tmpstr is None:
                return "NULL"
            elif isinstance(tmpstr,int):
                return tmpstr
            else:
                return "'"+tmpstr+"'"


    """

    Connect to the db and fetch the sqlite version

    """

    def connect(self,dbname):
        self.dbname = dbname

        logging.info("========> Trying to connect to %s"%dbname)

        try:
            con = sqlite3.connect(dbname)
            
            cur = con.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
    
            data = cur.fetchone()
    
            logging.info(" ========> AnalysisDBSQL SQLite version %s" % data)
    
        except sqlite3.Error, e:
            
            
            raise
    
        self.con = con

    """

    Fetch all tables in the DB

    """

    def getTables(self):
        try:

            with self.con:

                cur = self.executeQuery('SELECT name FROM sqlite_master WHERE type = "table"')

                rows    = cur.fetchall()

                return rows

        except sqlite3.Error, e:
    
            print "Error %s:" % e.args[0]
            raise Exception("Error executing sql %s" % e.args[0])

        return True

