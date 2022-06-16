from typing import List, Dict

import pandas as pd
from pgnhelper.utility import get_encounter_score


def num_wins(result_df: pd.DataFrame, ranking_df: pd.DataFrame) -> pd.DataFrame:
    """Creates a dataframe with Win column.
    """
    ret = ranking_df.copy()
    players = list(ret.Name)
    tb = {}
    for _, g in ret.groupby(['Score']):
        if len(g) > 1:
            for p in g.Name:
                df_w = result_df.loc[(result_df.White == p) & (result_df.Result == '1-0')]
                df_b = result_df.loc[(result_df.Black == p) & (result_df.Result == '0-1')]
                num_wins = len(df_w) + len(df_b)
                tb.update({p: num_wins})

    # Create new column Wins.
    wins = []
    for p in players:
        if p in tb:
            wins.append(tb[p])
        else:
            wins.append(0)
    ret['Wins'] = wins
    return ret


def direct_encounter(result_df: pd.DataFrame, ranking_df: pd.DataFrame, winpoint=1.0, drawpoint=0.5) -> pd.DataFrame:
    """Creates a dataframe with DE column or direct encounter.
    """
    players = list(ranking_df.Name)
    tb = {}
    ret: pd.DataFrame = ranking_df.copy()
    for _, g in ret.groupby(['Score']):
        if len(g) > 1:
            for p in g.Name:
                s = 0
                for op in g.Name:
                    if p == op:
                        continue
                    score = get_encounter_score(result_df, p, op, winpoint, drawpoint)
                    s += score[0]
                    tb.update({p: {op: s}})

    # Create new column DE.
    de = []
    for p in players:
        if p in tb:
            s = 0
            for k, v in tb.items():
                if k == p:
                    for _, v1 in v.items():
                        s += v1
            de.append(s)
        else:
            de.append(0)
    ret['DE'] = de
    return ret


def sonneborn_berger(result_df: pd.DataFrame, ranking_df: pd.DataFrame, gpe: int=1, winpoint=1.0, drawpoint=0.5) -> pd.DataFrame:
    """Returns a dataframe with SB column for Sonneborn-Berger score.
    1. Add all the scores of opponents that the player has defeated.
    2. Add all the scores of opponents that the player has drawn, then divide it by 2.
    3. Add the scores in step 1 and step 2, it will become the Sonneborn-Berger score.

    :param result_df: A dataframe of [Round, White, Black, Result]
    :param ranking_df: A dataframe of standing, [Name, Games, Score]
    :param gpe: games per encounter
    """
    tb: Dict[str, int] = {}
    ret: pd.DataFrame = ranking_df.copy()
    players = list(ret.Name)

    # 1. Loop thru the tied players.
    for _, g in ret.groupby(['Score']):
        if len(g) > 1:
            for p in g['Name']:
                tb_score = 0
                for m in players:
                    if p == m:
                        continue
                    match_score = 0
                    
                    # 2. Get the score when player wins or draws.
                    df_ww = result_df.loc[(result_df.White == p) & (result_df.Black == m) & (result_df.Result == '1-0')]
                    df_wd = result_df.loc[(result_df.White == p) & (result_df.Black == m) & (result_df.Result == '1/2-1/2')]
                    df_bw = result_df.loc[(result_df.Black == p) & (result_df.White == m) & (result_df.Result == '0-1')]
                    df_bd = result_df.loc[(result_df.Black == p) & (result_df.White == m) & (result_df.Result == '1/2-1/2')]

                    # 3. Calculate the scores.
                    match_score += winpoint * len(df_ww) + winpoint * len(df_bw) + len(df_wd) * drawpoint + len(df_bd) * drawpoint

                    if match_score > drawpoint * gpe:
                        tb_score += ret.loc[ret.Name == m].Score.iloc[0]
                    elif match_score == drawpoint * gpe:
                        tb_score += ret.loc[ret.Name == m].Score.iloc[0] / 2

                tb.update({p: tb_score})

    # 4. Create new column SB.
    tb_sb: List = []
    for p in players:
        if p not in tb:
            tb_sb.append(0)
            continue
        tb_sb.append(tb[p])
    ret['SB'] = tb_sb
    return ret
