"""Run sort games test.

1. pip install pgnhelper
2. Copy the tests folder in the github repository.

Example structure when mypgnhelper is the working dirtory:

   c:/mypgnhelper
   c:/mypgnhelper/tests/test_addeco.py

Command line:

   c:/pgnhelper> python -m pytest ./tests/test_addeco.py
"""


from pathlib import Path

import chess.pgn
import pgnhelper.eco


fn = Path('./tests/data/norway_chess_2022_classical.pgn')
outfn = Path('./tests/data/out_eco_norway_chess_2022_classical.pgn')
ecofn = Path('./tests/data/eco.pgn')


def test_addeco():
    """Add or replace the eco, opening and variation names to the pgn file.

    The output will be written in the output file. The original input pgn
    file will not be revised.
    """
    pgnhelper.eco.add_eco(fn, outfn, ecofn)
    eco, ecot, opening, openingt, variationt = '?', '?', '?', '?', '?'
    cnt = 0
    with open(outfn, 'r') as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            cnt += 1
            if cnt > 5:
                break
            if cnt != 5:
                continue
            eco = game.headers['ECO']
            ecot = game.headers.get('ECOT', '?')
            opening = game.headers['Opening']
            openingt = game.headers.get('OpeningT', '?')
            variationt = game.headers.get('VariationT', '?')
    outfn.unlink(missing_ok=True)
    assert (eco == 'E00' and ecot == 'E21' and
            opening == "Queen's pawn game" and openingt == 'Nimzo-Indian' and
            variationt == 'three knights variation')
