import subprocess, sys, os, select, filecmp, traceback
import shutil, errno, re, stat, platform
 
class Command(object):

    def __init__(self, cmd):

        if not cmd or type(cmd) != str:
            raise Exception('Invalid command: %s' % cmd)

        self.p = subprocess.Popen( ['/bin/bash', '-c', cmd],
                                   shell=False,
                                   stdin=open('/dev/null', 'r'),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE )
        self.command = cmd
        self.pid     = self.p.pid


    def run(self):

        p = self.p

        BLOCK_SIZE = 4096

        stdoutDone = False
        stderrDone = False
        out        = ''

        while not (stdoutDone and stderrDone):  # Be sure to fully iterate this or you will probably leave orphans.
            rfds, ignored, ignored2 = select.select([p.stdout.fileno(), p.stderr.fileno()], [], [])

            if p.stdout.fileno() in rfds:

                s = os.read(p.stdout.fileno(), BLOCK_SIZE)

                if s=='': stdoutDone = True

                if s:
                    print s 
                    i = 0
                    j = s.find('\n')

                    while j!=-1:
                        yield out + s[i:j+1]
                        out = ''
                        i = j+1
                        j = s.find('\n',i)
                    out += s[i:]

            if p.stderr.fileno() in rfds:
                s = os.read(p.stderr.fileno(), BLOCK_SIZE)
                if s=='': stderrDone = True
                if s:
                    i = 0
                    j = s.find('\n')
                    while j!=-1:
                        yield out + s[i:j+1]
                        out = ''
                        i = j+1
                        j = s.find('\n',i)
                    out += s[i:]
        if out!='':
           yield out

        p.wait() 
