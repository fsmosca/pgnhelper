"""Run sort games test.

1. pip install pgnhelper
2. Copy the tests folder in the github repository.

Example structure when mypgnhelper is the working dirtory:

   c:/mypgnhelper
   c:/mypgnhelper/tests/test_sortgames.py

Command line:

   c:/pgnhelper> python -m pytest ./tests/test_sortgames.py
"""


from pathlib import Path

import chess.pgn
import pgnhelper.sortgames


fn = Path('./tests/data/norway_chess_2022_classical.pgn')
outfn = Path('./tests/data/out_norway_chess_2022_classical.pgn')


def test_sortgames_white_lowtohigh():
    """Sort the games on white player from low to high.
    """
    pgnhelper.sortgames.sort_games(fn, outfn, 'white', 'lowtohigh')
    white, black = '?', '?'
    with open(outfn, 'r') as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            white = game.headers['White']
            black = game.headers['Black']
            break
    outfn.unlink(missing_ok=True)
    assert white == 'Anand, Viswanathan' and black == 'Vachier-Lagrave, Maxime'


def test_sortgames_white_hightolow():
    """Sort the games on white player from high to low.
    """
    pgnhelper.sortgames.sort_games(fn, outfn, 'white', 'hightolow')
    white, black = '?', '?'
    with open(outfn, 'r') as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            white = game.headers['White']
            black = game.headers['Black']
            break
    outfn.unlink(missing_ok=True)
    assert white == 'Wang, Hao' and black == 'Giri, Anish'


def test_sortgames_black_lowtohigh():
    """Sort the games on black player from low to high.
    """
    pgnhelper.sortgames.sort_games(fn, outfn, 'black', 'lowtohigh')
    white, black = '?', '?'
    with open(outfn, 'r') as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            white = game.headers['White']
            black = game.headers['Black']
            break
    outfn.unlink(missing_ok=True)
    assert white == 'Topalov, Veselin' and black == 'Anand, Viswanathan'


def test_sortgames_event():
    """Sort the games on event.
    """
    pgnhelper.sortgames.sort_games(fn, outfn, 'event', 'lowtohigh')
    event = '?',
    with open(outfn, 'r') as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            event = game.headers['Event']
            break
    outfn.unlink(missing_ok=True)
    assert event == '10th Norway Chess 2022'


def test_sortgames_site(sort_tag='site', sort_direction='lowtohigh', tag_value='Stavanger NOR'):
    """Sort the games on sort_tag.
    """
    pgnhelper.sortgames.sort_games(fn, outfn, sort_tag, sort_direction)
    value = '?',
    with open(outfn, 'r') as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            value = game.headers[sort_tag.title()]
            break
    outfn.unlink(missing_ok=True)
    assert value == tag_value


def test_sortgames_date(sort_tag='date', sort_direction='lowtohigh', tag_value='2022.05.31'):
    """Sort the games on sort_tag.
    """
    pgnhelper.sortgames.sort_games(fn, outfn, sort_tag, sort_direction)
    value = '?',
    with open(outfn, 'r') as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            value = game.headers[sort_tag.title()]
            break
    outfn.unlink(missing_ok=True)
    assert value == tag_value


def test_sortgames_eco(sort_tag='eco', sort_direction='lowtohigh', tag_value='A07'):
    """Sort the games on sort_tag.
    """
    pgnhelper.sortgames.sort_games(fn, outfn, sort_tag, sort_direction)
    value = '?',
    with open(outfn, 'r') as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            value = game.headers[sort_tag.upper()]
            break
    outfn.unlink(missing_ok=True)
    assert value == tag_value


def test_sortgames_eco_hightolow(sort_tag='eco', sort_direction='hightolow', tag_value='E94'):
    """Sort the games on sort_tag.
    """
    pgnhelper.sortgames.sort_games(fn, outfn, sort_tag, sort_direction)
    value = '?',
    with open(outfn, 'r') as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            value = game.headers[sort_tag.upper()]
            break
    outfn.unlink(missing_ok=True)
    assert value == tag_value
    