"""
sample_addeco.py
"""

import pgnhelper.app

a = pgnhelper.app.PgnHelper(
    'addeco',
    inpgnfn='F:\Github\pgnhelper\pgn\candidates_zurich_1953.pgn',
    outpgnfn='out_eco.pgn',
    inecopgnfn='F:\Github\pgnhelper\eco\eco.pgn')
a.start()
