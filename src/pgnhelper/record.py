"""Manages conversion of pgn file into a pandas dataframe.

It will read the games in the pgn file. Each game will be
converted to a row with round, white, black, result, etc. as headers.
"""


from typing import List, Tuple

import chess.pgn
import pandas as pd
import pgnhelper.elo


def get_pgn_data(fn, is_arm: bool = False, k: int = 10) -> Tuple[pd.DataFrame, List, bool]:
    """Converts games to dataframe.

    Args:
      df: A dataframe of game records.
      is_arm: If pgn file has armageddon games.
      k: The rating change k factor.

    Returns:
      [records, players, is_rating]
    """
    data = []
    players = []
    rating_cnt = 0
    with open(fn, 'r') as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            round = game.headers['Round']
            white = game.headers['White']
            black = game.headers['Black']
            result = game.headers['Result']
            players.append(white)
            players.append(black)
            welo = game.headers.get('WhiteElo', '?')
            belo = game.headers.get('BlackElo', '?')
            welo = '?' if welo == '' else welo
            belo = '?' if belo == '' else belo
            if welo != '?':
                rating_cnt += 1
                welo = int(welo)
            if belo != '?':
                rating_cnt += 1
                belo = int(belo)
            if result == '1-0':
                wpt = 1.0
                bpt = 0.0
            elif result == '0-1':
                wpt = 0.0
                bpt = 1.0
            elif result == '1/2-1/2':
                wpt = 0.5
                bpt = 0.5 
            elif result == '*':
                wpt = 0.0
                bpt = 0.0 
            myecot = game.headers.get('ECOT', '?')
            myopeningt = game.headers.get('OpeningT', '?')
            if myecot == '?':
                myecot = game.headers.get('ECO', '?')
                myopeningt = game.headers.get('Opening', '?')                       
            data.append([round, white, black, welo, belo, result, wpt, bpt,
                         1 if is_arm else 0, myecot, myopeningt])
    df = pd.DataFrame(
        data,
        columns=['Round', 'White', 'Black', 'WElo', 'BElo', 'Result',
                 'Wpt', 'Bpt', 'Arm', 'Eco', 'Opening'])
    df = pgnhelper.elo.add_rating_change(df, rating_cnt > 1, k)
    return df, list(set(players)), rating_cnt > 0
