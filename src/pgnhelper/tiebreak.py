"""Generates tie-break points on tied players.

Tie-breaks supported:
  * Direct Encounter
  * Number of wins
  * Sonneborn-Berger
  * Koya system
"""


from typing import List, Dict

import pandas as pd
import pgnhelper.utility


def num_wins(result_df: pd.DataFrame, ranking_df: pd.DataFrame) -> pd.DataFrame:
    """Creates a dataframe with Win column.
    
    If a game has an armageddon tie-break, we will only count the number of wins
    based from the normal game only.
    """
    ret = ranking_df.copy()
    players = list(ret.Name)
    tb = {}
    for _, g in ret.groupby(['Score']):
        if len(g) > 1:
            for p in g.Name:
                df_w = result_df.loc[(result_df.White == p) & (result_df.Result == '1-0') & (result_df.Arm == 0)]
                df_b = result_df.loc[(result_df.Black == p) & (result_df.Result == '0-1') & (result_df.Arm == 0)]
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


def direct_encounter(result_df: pd.DataFrame, ranking_df: pd.DataFrame, winpoint=1.0, drawpoint=0.5, winpointarm=1.0, losspointarm=0.0) -> pd.DataFrame:
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
                    score = pgnhelper.utility.get_encounter_score(result_df, p, op, winpoint, drawpoint, winpointarm, losspointarm)
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


def sonneborn_berger(result_df: pd.DataFrame, ranking_df: pd.DataFrame,
        gpe: int=1, winpoint=1.0, drawpoint=0.5) -> pd.DataFrame:
    """Creates a dataframe with SB column for Sonneborn-Berger score.

    Armageddon games currently are excluded in the calculation.

    Args:
      result_df: A dataframe of [Round, White, Black, Result].
      ranking_df: A dataframe of standing, [Name, Games, Score].
      gpe: games per encounter

    Returns:
      A dataframe of round-robin result table.
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
                    df_ww = result_df.loc[(result_df.White == p) & (result_df.Black == m) & (result_df.Result == '1-0') & (result_df.Arm == 0)]
                    df_wd = result_df.loc[(result_df.White == p) & (result_df.Black == m) & (result_df.Result == '1/2-1/2') & (result_df.Arm == 0)]
                    df_bw = result_df.loc[(result_df.Black == p) & (result_df.White == m) & (result_df.Result == '0-1') & (result_df.Arm == 0)]
                    df_bd = result_df.loc[(result_df.Black == p) & (result_df.White == m) & (result_df.Result == '1/2-1/2') & (result_df.Arm == 0)]

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


def koya_system(result_df: pd.DataFrame, ranking_df: pd.DataFrame,
                winpoint=1.0, drawpoint=0.5) -> pd.DataFrame:
    """Creates a dataframe with Koya column for Koya system score.

    Koya system - the number of points achieved against all opponents
    who have achieved 50 % or more.

    11.5.4.3, https://handbook.fide.com/files/handbook/C02Standards.pdf

    Args:
      result_df: A dataframe of [Round, White, Black, Result ...].
      ranking_df: A dataframe of standing, [Name, Games, Score].

    Returns:
      A ranking dataframe with Koya column.
    """
    tb: Dict[str, int] = {}
    ret: pd.DataFrame = ranking_df.copy()
    players = list(ret.Name)

    # Get player dataframe who score 50% and above.
    df50 = ranking_df.copy()
    df50['Score%'] = 100 * df50['Score'] / df50['Games']
    df50 = df50.loc[df50['Score%'] >= 50.0]

    # 1. Loop thru the tied players.
    for _, g in ret.groupby(['Score']):
        if len(g) > 1:
            for p in g['Name']:
                tb_score = 0
                for m in players:
                    if p == m:
                        continue
                    if m not in df50.Name.unique():
                        continue
            
                    # 2. Get the score when player wins or draws, excluding armageddon games.
                    df_ww = result_df.loc[(result_df.White == p) & (result_df.Black == m) & (result_df.Result == '1-0') & (result_df.Arm == 0)]
                    df_wd = result_df.loc[(result_df.White == p) & (result_df.Black == m) & (result_df.Result == '1/2-1/2') & (result_df.Arm == 0)]
                    df_bw = result_df.loc[(result_df.Black == p) & (result_df.White == m) & (result_df.Result == '0-1') & (result_df.Arm == 0)]
                    df_bd = result_df.loc[(result_df.Black == p) & (result_df.White == m) & (result_df.Result == '1/2-1/2') & (result_df.Arm == 0)]

                    # 3. Get the total score.
                    tb_score += winpoint * len(df_ww) + winpoint * len(df_bw) + len(df_wd) * drawpoint + len(df_bd) * drawpoint

                tb.update({p: tb_score})

    # 4. Create new column Koya.
    tb_sb: List = []
    for p in players:
        if p not in tb:
            tb_sb.append(0)
            continue
        tb_sb.append(tb[p])
    ret['Koya'] = tb_sb
    return ret
