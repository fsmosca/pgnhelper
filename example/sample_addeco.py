"""
sample_addeco.py
"""

from pgnhelper import pgnhelper

a = pgnhelper.PgnHelper(
    'addeco',
    inpgnfn='mygames.pgn',
    outpgnfn='out.pgn',
    inecopgnfn='eco.pgn')
a.start()