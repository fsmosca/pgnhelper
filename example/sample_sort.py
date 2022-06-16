"""
sample_sort.py

pip install pgnhelper
"""

import pgnhelper

a = pgnhelper.PgnHelper(
    'sort',
    inpgnfn='mygames.pgn',
    outpgnfn='out.pgn',
    sort_tag='eco',
    sort_direction='hightolow')
a.start()