"""Generates a round-robin result table.

It reads the input pgn file and generates a dataframe of round-robin table.
It also add columns for tie-break scores for tied players.

Typical tie-break system that can be applied to a round-robin tournament
according to FIDE.

13.16.2. Individual Round-Robin Tournaments:
    * Direct encounter
    * The greater number of wins, including forfeits
    * Sonneborn-Berger
    * Koya System (to be implemented in pgnhelper)

https://handbook.fide.com/files/handbook/C02Standards.pdf
"""


from pathlib import Path
from typing import List

import chess.pgn
import pandas as pd
from pretty_html_table import build_table

import pgnhelper.tiebreak
import pgnhelper.utility


def get_pgn_data(fn: str, is_arm: bool=False):
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
            data.append([round, white, black, welo, belo, result, 1 if is_arm else 0])
    df = pd.DataFrame(data,
            columns=['Round', 'White', 'Black', 'WElo', 'BElo', 'Result', 'Arm'])
    return df, list(set(players)), rating_cnt > 0


def games_per_encounter(result_df: pd.DataFrame, ranking_df: pd.DataFrame):
    """Count number of games per encounter excluding armageddon.
    """
    players = list(ranking_df.Name)
    for p in players:
        for m in players:
            if p == m:
                continue
            dfw = result_df.loc[(result_df.White == p) & (result_df.Black == m)
                    & (result_df.Arm == 0)]
            dfb = result_df.loc[(result_df.Black == p) & (result_df.White == m)
                    & (result_df.Arm == 0)]
            return len(dfw) + len(dfb)
    return 0


def player_ranking(df: pd.DataFrame, players: List, is_rating: bool,
        winpoint: float, drawpoint: float, winpointarm:float=1.5,
        losspointarm: float=1.0) -> pd.DataFrame:
    """Generates a dataframe of player ranking.

    Args:
      df: A dataframe of player match records.
      players: A list of unique players names.
      is_rating: If players have rating.
    """
    is_arm = True if 1 in df['Arm'].unique() else False
    data_p = []
    for p in players:       
        if not is_arm:
            df_w = df[df.White == p]
            df_b = df[df.Black == p]
            score_w = len(df_w[df_w.Result == '1-0']) * winpoint
            score_w += len(df_w[df_w.Result == '1/2-1/2']) * drawpoint
            score_b = len(df_b[df_b.Result == '0-1']) * winpoint
            score_b += len(df_b[df_b.Result == '1/2-1/2']) * drawpoint
            final_score = score_w + score_b
        else:
            # Used to get the number of games for normal games.
            df_w = df[(df.White == p) & (df.Arm == 0)]
            df_b = df[(df.Black == p) & (df.Arm == 0)]

            # Get the score for normal games without draws.
            df_w_normal = df.loc[(df.White == p) & (df.Arm == 0) & (df.Result != '1/2-1/2')]
            df_b_normal = df.loc[(df.Black == p) & (df.Arm == 0) & (df.Result != '1/2-1/2')]
            score_w_n = len(df_w_normal.loc[df_w_normal.Result == '1-0']) * winpoint
            score_b_n = len(df_b_normal.loc[df_b_normal.Result == '0-1']) * winpoint

            # Get score for arm games.
            df_w_arm = df.loc[(df.White == p) & (df.Arm == 1)]
            df_b_arm = df.loc[(df.Black == p) & (df.Arm == 1)]

            # wins
            score_w_aw = len(df_w_arm.loc[df_w_arm.Result == '1-0']) * winpointarm
            score_b_aw = len(df_b_arm.loc[df_b_arm.Result == '0-1']) * winpointarm
            score_b_aw += len(df_b_arm.loc[df_b_arm.Result == '1/2-1/2']) * winpointarm

            # loses
            score_w_al = len(df_w_arm.loc[df_w_arm.Result == '0-1']) * losspointarm
            score_w_al += len(df_w_arm.loc[df_w_arm.Result == '1/2-1/2']) * losspointarm
            score_b_al = len(df_b_arm.loc[(df_b_arm.Result == '1-0')]) * losspointarm

            final_score = (score_w_n + score_b_n + score_w_aw + score_b_aw
                    + score_w_al + score_b_al)

        if is_rating:
            rating = df_w.WElo.iloc[0]  # all players have at least played a game with white
            data_p.append([p, rating, len(df_w) + len(df_b), final_score])
        else:
            data_p.append([p, len(df_w) + len(df_b), final_score])
    if is_rating:
        df_score = pd.DataFrame(data_p,
                columns=['Name', 'Rating', 'Games', 'Score'])
    else:
        df_score = pd.DataFrame(data_p, columns=['Name', 'Games', 'Score'])
    df_score = df_score.sort_values(by=['Score', 'Name'],
            ascending=[False, True])
    df_score = df_score.reset_index(drop=True)
    return df_score


def save_roundrobin_table(df: pd.DataFrame,
        outputfn: str, tablecolor: str='blue_light'):
    """Save the round-robin result table.

    Args:
      df: A dataframe of players match records.
      outputfn: The output file.
      tablecolor: The round-robin table color.
    """
    ext = Path(outputfn).suffix
    if ext == '.html':
        html_table = build_table(df, tablecolor,
            font_size='medium',
            text_align='center',
            font_family='Calibri, Verdana, Tahoma, Georgia, serif, arial')
        with open(outputfn, 'w') as f:
            f.write(html_table)
    elif ext == '.csv':
        df.to_csv(outputfn, index=False)
    else:
        df.to_string(outputfn, index=False)


def round_robin(fn: str, winpoint=1.0, drawpoint=0.5, armageddonfile=None,
                winpointarm=1.0, losspointarm=0.0, showmaxscore=False):
    dfall = []
    dfn, players, is_rating = get_pgn_data(fn, is_arm=False)
    dfall.append(dfn)
    if armageddonfile is not None:
        dfa, _, _ = get_pgn_data(armageddonfile, is_arm=True)
        dfall.append(dfa)
    df = pd.concat(dfall, ignore_index=False)
    is_arm = True if 1 in df.Arm.unique() else False

    # 1. Create a dataframe of player ranking.
    df_score = player_ranking(df, players, is_rating, winpoint,
            drawpoint, winpointarm, losspointarm)
    gpe = games_per_encounter(df, df_score)

    # 1.1 Apply Direct Encounter tie-break
    df_de = pgnhelper.tiebreak.direct_encounter(df, df_score, winpoint,
            drawpoint, winpointarm, losspointarm)
    df_de = df_de.sort_values(by=['Score', 'DE', 'Name'],
            ascending=[False, False, True])
    df_de = df_de.reset_index(drop=True)

    # 1.2 Apply Number of Wins tie-break
    df_wins = pgnhelper.tiebreak.num_wins(df, df_de)
    df_wins = df_wins.sort_values(by=['Score', 'DE', 'Wins', 'Name'],
            ascending=[False, False, False, True])
    df_wins = df_wins.reset_index(drop=True)  

    # 1.3 Apply Sonneborn-Berger tie-break
    if not is_arm:
        df_sb = pgnhelper.tiebreak.sonneborn_berger(df, df_wins, gpe=gpe,
                winpoint=1.0, drawpoint=0.5)
        df_sb = df_sb.sort_values(by=['Score', 'DE', 'Wins', 'SB', 'Name'],
                ascending=[False, False, False, False, True])
        df_sb = df_sb.reset_index(drop=True)
    else:
        df_sb = df_wins.copy()

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
                score = pgnhelper.utility.get_encounter_score(df, p, op,
                        winpoint, drawpoint, winpointarm, losspointarm)
                v = score[1]  # use the score of op only
            data_v.append(v)
        data_rr.update({cnt: data_v})
        cnt += 1
    df_rr = pd.DataFrame(data_rr)

    # 3. Add other columns at the end.
    df_rr['Games'] = df_sb['Games']
    df_rr['Score'] = df_sb['Score']
    max_score = df_sb['Games'] * winpoint
    if showmaxscore:
        df_rr['MaxScore'] = max_score
    df_rr['Score%'] = 100 * df_sb['Score'] / max_score
    df_rr['Score%'] = df_rr['Score%'].round(2)
    df_rr['DE'] = df_sb['DE'].round(2)
    df_rr['Wins'] = df_sb['Wins'].round(0)
    if not is_arm:
        df_rr['SB'] = df_sb['SB'].round(2)

    # 4. Insert rank column at first column.
    df_rr.insert(loc=0, column='Rank', value=range(1, len(df_rr) + 1))
    return df_rr
