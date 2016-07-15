import sys, os, select, filecmp, traceback
import shutil, errno, re, stat, platform
 
from subprocess import Popen, PIPE, STDOUT

class Command(object):
    
    outstr = []
    errstr = []

    def __init__(self, cmd):

        if not cmd or type(cmd) != str:
            raise Exception('Invalid command: %s' % cmd)


        self.command = cmd

        self.p = Popen( ['/bin/bash', '-c', cmd],
                        shell=False,   # Is this cos we're using bash above?
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE,
                        close_fds = True)



        self.pid     = self.p.pid


    def run(self):

        p = self.p

        while p.poll() == None:

            (out,err) = p.communicate()

            if out != '':
                self.outstr.append(out)


            if err != '':
                self.errstr.append(err)


            sys.stdout.flush()
            sys.stderr.flush()

