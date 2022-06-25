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


def played_each_other(result_df, tie_df) -> bool:
    players = list(tie_df.Name)
    for p in players:
        for m in players:
            if p == m:
                continue
            dfw = result_df.loc[(result_df.White == p) & (result_df.Black == m)]
            dfb = result_df.loc[(result_df.Black == p) & (result_df.White == m)]
            if len(dfw) + len(dfb) == 0:
                return False
    return True


def num_wins(result_df: pd.DataFrame, ranking_df: pd.DataFrame, label='Wins') -> pd.DataFrame:
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
    ret[label] = wins
    return ret


def direct_encounter(result_df: pd.DataFrame, ranking_df: pd.DataFrame,
        winpoint=1.0, drawpoint=0.5, winpointarm=1.5, losspointarm=1.0,
        label='DE') -> pd.DataFrame:
    """Creates a dataframe with DE column or direct encounter.

    Requirement:
      It is only applied when tied players have played each other.
      In round-robin format this can be applied automatically. But for
      swiss format, the tied players have to be checked.
    """
    players = list(ranking_df.Name)
    tb = {}
    ret: pd.DataFrame = ranking_df.copy()
    for _, g in ret.groupby(['Score']):
        if len(g) > 1:
            if played_each_other(result_df, g):
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
    ret[label] = de
    return ret


def sonneborn_berger(result_df: pd.DataFrame, ranking_df: pd.DataFrame,
        gpe: int=1, winpoint=1.0, drawpoint=0.5, label='SB') -> pd.DataFrame:
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
    ret[label] = tb_sb
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


def tb_buchholz(record_df, rank_df, cut: int=0, label='TB1') -> pd.DataFrame():
    """Calculates buchholz score or sum of opponents score.

    This tie-break system is only applied for a tournament with swiss format.

    Args:
      record_df: A dataframe of tournament games records.
      rank_df: A dataframe with player ranking, initially
         at ['Name, Games, Score]. Later ['Name, Games, Score, Buchholz, ... tie-break system]
      cut: Cut the player opponent score, if cut is 0 the default then
          no one will be cut, this is the normal buchholz. If this is 1 then
          the lowest score will be cut. If this is 2 then the last two lowest
          scores will be cut. If value is -1 this is median or cut the highest
          and lowest. If value is -2 then cut the 2 highest and 2 lowest.

    Returns:
       A dataframe of name and buchholz score.
    """
    ret = rank_df.copy()
    players = ret.Name.unique()
    tb: Dict[str, int] = {}

    for _, g in ret.groupby(['Score']):
        if len(g) > 1:
            for p in g['Name']:
                opp_scores = []

                dfw = record_df.loc[record_df.White == p]
                for i in range(len(dfw)):
                    opp = dfw.iloc[i]['Black']
                    dfm = rank_df.loc[rank_df.Name == opp]
                    pts = dfm['Score'].iloc[0]
                    opp_scores.append(pts)

                dfb = record_df.loc[record_df.Black == p]
                for i in range(len(dfb)):
                    opp = dfb.iloc[i]['White']
                    dfm = rank_df.loc[rank_df.Name == opp]
                    pts = dfm['Score'].iloc[0]
                    opp_scores.append(pts)

                # Sort the opponents scores so we can determine what to cut.
                if cut != 0:
                    opp_scores.sort(reverse=True)  # high to low
                    if cut > 0:
                        # Apply Buchholz cut 1 or 2 and so on.
                        opp_scores = opp_scores[:-cut]
                    # Else apply Median Buchholz.
                    else:
                        # 1. Median Buchholz, cut the highest and lowest.
                        # 2. Median Buchholz 2, cut the 2 highest and 2 lowest.
                        opp_scores = opp_scores[-cut:cut]

                tb.update({p: sum(opp_scores)})

    # Add Buchholz column.
    tbs: List = []
    for p in players:
        if p not in tb:
            tbs.append(0)
            continue
        tbs.append(tb[p])
    ret[label] = tbs

    # Sort tie-break scores.
    sort_columns = list(ret.columns)
    if 'Rating' in sort_columns:
        sort_columns.remove('Rating')
    sort_columns.remove('Games')
    sort_columns.remove('Name')
    sort_columns.append(label)
    sort_order = [False for _ in sort_columns]

    ret = ret.sort_values(
        by=sort_columns,
        ascending=sort_order
    )
    ret = ret.reset_index(drop=True)

    return ret
