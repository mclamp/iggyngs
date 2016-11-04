import os, re, logging, json

from iggyngs.Analysis           import Analysis
from illuminate                 import InteropDataset

class IlluminateAnalysis(Analysis):

    def __init__(self,rundir,outdir,test=True,verbose=False):

       Analysis.__init__(self)

       self.rundir      = rundir
       self.outdir      = outdir
       self.test        = test
       self.verbose     = verbose

    def makeCommands(self):

        self.runname = os.path.basename(self.rundir)

        if not os.path.isabs(self.rundir):
           self.rundir = os.path.join(os.getcwd(),self.rundir)

        if not os.path.isabs(self.outdir):
           self.outdir = os.path.join(os.getcwd(),self.outdir)

        if not os.path.exists(self.rundir):
           raise Exception("Run directory [%s] doesn't exist. Can't run Illuminate"%self.rundir)

        if not os.path.isdir(self.outdir):
           os.makedirs(self.outdir)

        self.outfile = os.path.join(self.outdir,self.runname + ".illuminate.log")

        print "Rundir %s"%self.rundir
        print "Outdir %s"%self.outdir
        print "Outfile %s"%self.outfile

    def run(self):

       data      = {}

       runstats     = InteropDataset(self.rundir)
       tilemetrics  = runstats.TileMetrics()

       tiledict     = tilemetrics.to_dict()

       data['cluster_density']    = int(tiledict['cluster_density'])
       data['cluster_density_pf'] = int(tiledict['cluster_density_pf'])
       data['num_clusters']       = int(tiledict['num_clusters'])
       data['num_clusters_pf']    = int(tiledict['num_clusters_pf'])
 
       # Qualmetrics keys ['apparent_file_version', 'flowcell_layout', 'num_reads', 'df', 'data', 'num_tiles', 'qcol_sequence', 'read_qscore_results', 'bs', 'idf', 'read_config', 'read_tiers']

       # flowcell_layout {'tilecount': 12, 'lanecount': 4, 'surfacecount': 2, 'swathcount': 3}

       # read_config     [{'is_index': False, 'cycles': 35, 'read_num': 'Read1'}, 
       #                  {'is_index': False, 'cycles': 51, 'read_num': 'Read2'}, 
       #                  {'is_index': True, 'cycles': 6, 'read_num': 'Index1Read'}, 
       #                  {'is_index': True, 'cycles': 0, 'read_num': 'Index2Read'}]

       qualmetrics  = runstats.QualityMetrics()
       qualdict     = qualmetrics.__dict__

       data['num_reads']    = qualdict['num_reads']
       data['read_config'] = qualdict['read_config']

       #self.assertEqual(qualdict['read_config'][0]['is_index'], False,"Read 0 is not sequence read")
       #self.assertEqual(qualdict['read_config'][0]['cycles'], 35,     "Read 0 doesn't have 35 cycles")

       # Qualsummary dict {'q20': [97.1786397395114, 98.31368553586876, 97.82261759016959, 0], 'q30': [95.83418246308082, 97.16680373968876, 96.49838147843126, 0], 'readnum': [1, 2, 3, 4]}
       qual_summary = qualmetrics.read_qscore_results

       data['qual_summary'] = qual_summary

       self.data = data


       fh = open(self.outfile, "w")
       fh.write(json.dumps(data, ensure_ascii=False))
       fh.close()
