"""
sample_sort.py
"""

import pgnhelper.app

a = pgnhelper.app.PgnHelper(
    'sort',
    inpgnfn='F:\Github\pgnhelper\pgn\candidates_zurich_1953.pgn',
    outpgnfn='out_sorted.pgn',
    sort_tag='white',
    sort_direction='hightolow')
a.start()
