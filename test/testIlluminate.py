'''
Created on Apr 26, 2016

@author: mclamp
'''


import unittest
import os, shutil

from illuminate import InteropDataset

class Test(unittest.TestCase):

    def __init__(self,*args,**kwargs):
        super(Test,self).__init__(*args,**kwargs)
        
    def testIlluminate(self):


       # Tilemetrics keys ['apparent_file_version', 'total_cluster_density', 'flowcell_layout', 'num_reads', 'df', 'mean_prephasing', 'mean_phasing', 
       #                   'num_tiles', 'codemap', 'num_clusters_pf', 'percent_pf_clusters', 'mean_cluster_density_pf', 'bs', 'mean_cluster_density', 
       #                   'read_config', 'data', 'num_clusters', 'total_cluster_density_pf']



       rundir       = 'data/160425_NS500422_0317_AH3NMLBGXY/'
       runstats     = InteropDataset(rundir)
       print "Made Interop Dataset from %s"%rundir

       tilemetrics  = runstats.TileMetrics()
       tiledict     = tilemetrics.to_dict()

       self.assertEqual(int(tiledict['cluster_density']),136131,          "Tile metrics cluster density incorrect")
       self.assertTrue(tiledict['mean_phasing'][0]           == 0,        "Tile metrics mean phasing incorrect")
       self.assertTrue(tiledict['mean_prephasing'][0]        == 0,        "Tile metrics mean prephasing incorrect")
       self.assertTrue(int(tiledict['cluster_density_pf'])   == 126958,   "Tile metrics cluster density pf incorrect")
       self.assertTrue(int(tiledict['num_clusters'])         == 353581319,"Tile metrics num clusters incorrect")
       self.assertTrue(int(tiledict['num_clusters_pf'])      == 330099219,"Tile metrics num clusters pf incorrect")


       # Qualmetrics keys ['apparent_file_version', 'flowcell_layout', 'num_reads', 'df', 'data', 'num_tiles', 'qcol_sequence', 'read_qscore_results', 'bs', 'idf', 'read_config', 'read_tiers']

       # flowcell_layout {'tilecount': 12, 'lanecount': 4, 'surfacecount': 2, 'swathcount': 3}
       # read_config     [{'is_index': False, 'cycles': 35, 'read_num': 'Read1'}, {'is_index': False, 'cycles': 51, 'read_num': 'Read2'}, {'is_index': True, 'cycles': 6, 'read_num': 'Index1Read'}, {'is_index': True, 'cycles': 0, 'read_num': 'Index2Read'}]
       # num_reads       4

       qualmetrics  = runstats.QualityMetrics()
       qualdict     = qualmetrics.__dict__

       self.assertEqual(qualdict['num_reads'],4,                      "Number of reads incorrect")
       self.assertEqual(qualdict['num_reads'],4,                      "Number of reads incorrect")
       self.assertEqual(qualdict['flowcell_layout']['lanecount'],4,   "Lane count incorrect")
       self.assertEqual(len(qualdict['read_config']),4,               "Read count incorrect")
       self.assertEqual(qualdict['read_config'][0]['is_index'], False,"Read 0 is not sequence read")
       self.assertEqual(qualdict['read_config'][0]['cycles'], 35,     "Read 0 doesn't have 35 cycles")

       # Qualsummary dict {'q20': [97.1786397395114, 98.31368553586876, 97.82261759016959, 0], 'q30': [95.83418246308082, 97.16680373968876, 96.49838147843126, 0], 'readnum': [1, 2, 3, 4]}
       qual_summary = qualmetrics.read_qscore_results

       self.assertEqual(int(qual_summary['q20'][0]),97, "Read1 q20 % incorrect")
       self.assertEqual(int(qual_summary['q30'][2]),96, "Read3 q20 % incorrect")

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
