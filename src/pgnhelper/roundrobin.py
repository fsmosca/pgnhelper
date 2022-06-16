"""roundrobin.py
A round-robin result generator based from the given pgn file.

Typical tie-break system that can be applied to a round-robin tournament according to FIDE.

13.16.2. Individual Round-Robin Tournaments:
    Direct encounter
    The greater number of wins, including forfeits
    Sonneborn-Berger
    Koya System
https://handbook.fide.com/files/handbook/C02Standards.pdf

Todo:
    Implement Koya System
"""


import chess.pgn
import pandas as pd
from pgnhelper.tiebreak import direct_encounter, sonneborn_berger, num_wins
from pgnhelper.utility import get_encounter_score


def get_pgn_data(fn):
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
            if welo != '?':
                rating_cnt += 1
            if belo != '?':
                rating_cnt += 1
            data.append([round, white, black, welo, belo, result])
    df = pd.DataFrame(data, columns=['Round', 'White', 'Black', 'WElo', 'BElo', 'Result'])
    return df, list(set(players)), rating_cnt > 0


def games_per_encounter(result_df, ranking_df):
    players = list(ranking_df.Name)
    for p in players:
        for m in players:
            if p == m:
                continue
            dfw = result_df.loc[(result_df.White == p) & (result_df.Black == m)]
            dfb = result_df.loc[(result_df.Black == p) & (result_df.White == m)]
            return len(dfw) + len(dfb)
    return 0


def round_robin(fn: str, winpoint=1.0, drawpoint=0.5):
    df, players, is_rating = get_pgn_data(fn)

    # 1. Create a dataframe of player ranking.
    data_p = []
    for p in players:
        df_w = df[df.White == p]
        df_b = df[df.Black == p]
        score_w = len(df_w[df_w.Result == '1-0']) * winpoint
        score_w += len(df_w[df_w.Result == '1/2-1/2']) * drawpoint
        score_b = len(df_b[df_b.Result == '0-1']) * winpoint
        score_b += len(df_b[df_b.Result == '1/2-1/2']) * drawpoint
        if is_rating:
            rating = df_w.WElo.iloc[0]  # all players have at least played a game with white
            data_p.append([p, rating, len(df_w) + len(df_b), score_w + score_b])
        else:
            data_p.append([p, len(df_w) + len(df_b), score_w + score_b])
    if is_rating:
        df_score = pd.DataFrame(data_p, columns=['Name', 'Rating', 'Games', 'Score'])
    else:
        df_score = pd.DataFrame(data_p, columns=['Name', 'Games', 'Score'])
    df_score = df_score.sort_values(by=['Score', 'Name'], ascending=[False, True])
    df_score = df_score.reset_index(drop=True)
    gpe = games_per_encounter(df, df_score)

    # 1.1 Apply Direct Encounter tie-break
    df_de = direct_encounter(df, df_score, winpoint, drawpoint)
    df_de = df_de.sort_values(by=['Score', 'DE', 'Name'], ascending=[False, False, True])
    df_de = df_de.reset_index(drop=True)

    # 1.2 Apply Number of Wins tie-break
    df_wins = num_wins(df, df_de)
    df_wins = df_wins.sort_values(by=['Score', 'DE', 'Wins', 'Name'], ascending=[False, False, False, True])
    df_wins = df_wins.reset_index(drop=True)  

    # 1.3 Apply Sonneborn-Berger tie-break
    df_sb = sonneborn_berger(df, df_wins, gpe=gpe, winpoint=1.0, drawpoint=0.5)
    df_sb = df_sb.sort_values(by=['Score', 'DE', 'Wins', 'SB', 'Name'], ascending=[False, False, False, False, True])
    df_sb = df_sb.reset_index(drop=True)

    # 2. Build a round-robin dataframe.
    if is_rating:
        data_rr = {'Name': df_sb.Name, 'Rating': df_sb.Rating}
    else:
        data_rr = {'Name': df_sb.Name.unique()}
    cnt = 1
    for p in df_sb.Name.unique():
        data_v = []
        for op in df_sb.Name.unique():
            if p == op:
                v = 'x'
            else:
                score = get_encounter_score(df, p, op, winpoint, drawpoint)
                v = score[1]  # use the score of op only
            data_v.append(v)
        data_rr.update({cnt: data_v})
        cnt += 1
    df_rr = pd.DataFrame(data_rr)

    # 3. Add other columns at the end.
    df_rr['Games'] = df_sb['Games']
    df_rr['Score'] = df_sb['Score']
    df_rr['Score%'] = 100 * df_sb['Score'] / (df_sb['Games'] * winpoint)
    df_rr['Score%'] = df_rr['Score%'].round(1)
    df_rr['DE'] = df_sb['DE'].round(1)
    df_rr['Wins'] = df_sb['Wins'].round(0)
    df_rr['SB'] = df_sb['SB'].round(1)

    # 4. Insert rank column at first column.
    df_rr.insert(loc=0, column='Rank', value=range(1, len(df_rr) + 1))
    return df_rr
