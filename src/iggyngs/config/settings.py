import os, logging

from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

SQLITE_FILE                    = os.path.join('data.sqlite')
LOGFILE                        = os.path.join('iggyngs'+ datetime.now().strftime("%Y-%m-%d")+'.log')

logging.basicConfig(filename=LOGFILE,level=logging.INFO)
