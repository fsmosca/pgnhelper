"""Helps build the round-robin result table.
"""


from typing import List
import pandas as pd
from pathlib import Path
from pretty_html_table import build_table


def get_encounter_score(df: pd.DataFrame, p: str, op: str,
                        winpoint: float = 1.0, drawpoint: float = 0.5,
                        winpointarm: float = 1.0,
                        losspointarm: float = 0.0) -> List[float]:
    """Calculates the scores between the player p and op.

    Args:
      df: A pandas dataframe containing players match results.
      p: A player name.
      op: Opponent of player p.
      winpoint: The point when player wins.
      drawpoint: The point when player draws.
      winpointarm: The point when player wins in armageddon game.
      losspointarm: The point when player loses in armageddon game.

    Returns:
      A list of score for p and op, score[<p score>, <op score>].
    """
    is_arm = True if 1 in df.Arm.unique() else False
    score = [0, 0]
    dfw = df[(df.White == p) & (df.Black == op)]
    dfb = df[(df.Black == p) & (df.White == op)]

    # If a game is normal or no tie-break points involved.
    if not is_arm:
        # Update the score when p is white.    
        for i in range(len(dfw)):
            v = dfw.iloc[i]['Result']
            if v == '1-0':
                score[0] += 1.0 * winpoint
                score[1] += 0.0
            elif v == '0-1':
                score[0] += 0.0
                score[1] += 1.0 * winpoint
            elif v == '1/2-1/2':
                score[0] += drawpoint
                score[1] += drawpoint

        # Update the score when p is black.
        for i in range(len(dfb)):
            v = dfb.iloc[i]['Result']
            if v == '1-0':
                score[0] += 0.0
                score[1] += 1.0 * winpoint
            elif v == '0-1':
                score[0] += 1.0 * winpoint
                score[1] += 0.0
            elif v == '1/2-1/2':
                score[0] += drawpoint
                score[1] += drawpoint

    # Else if a game has armageddon tie-break.
    else:
        # A. In norway chess, in normal game, the winner will get 3.0 points,
        # the loser will get 0.0 point.

        # 1. Get the score from normal game with 1-0 and 0-1 result where
        # the first player is white. We don't include the draw results
        # because we will use the armageddon tie-break system.
        dfw_normal = df[
            (df.White == p) & (df.Black == op) & (df.Arm == 0) &
            ((df.Result == '1-0') | (df.Result == '0-1'))]
        for i in range(len(dfw_normal)):
            r = dfw_normal.iloc[i]['Result']
            if r == '1-0':
                score[0] += 1.0 * winpoint
                score[1] += 0.0
            elif r == '0-1':
                score[0] += 0.0
                score[1] += 1.0 * winpoint

        # 2. Get the score from normal game with 1-0 and 0-1 result where
        # the first player is black. We don't include the draw results
        # because we will use the armageddon tie-break system.
        dfb_normal = df[
            (df.Black == p) & (df.White == op) & (df.Arm == 0) &
            ((df.Result == '1-0') | (df.Result == '0-1'))]
        for i in range(len(dfb_normal)):
            r = dfb_normal.iloc[i]['Result']
            if r == '0-1':
                score[0] += 1.0 * winpoint
                score[1] += 0.0
            elif r == '1-0':
                score[0] += 0.0
                score[1] += 1.0 * winpoint

        # B. In norway chess, in armageddon game, the winner will get
        # 1.5 points, the loser will get 1.0 point. The armageddon game
        # is done if the normal game resulted in a draw. The point in a
        # normal game that resulted in a draw is discarded.

        # 1. Get the score from armageddon game where the first player is white.
        dfw_arm = df[(df.White == p) & (df.Black == op) & (df.Arm == 1)]
        for i in range(len(dfw_arm)):
            r = dfw_arm.iloc[i]['Result']
            if r == '1-0':
                score[0] += 1.0 * winpointarm
                score[1] += 1.0 * losspointarm
            elif r == '0-1':
                score[0] += 1.0 * losspointarm
                score[1] += 1.0 * winpointarm
            elif r == '1/2-1/2':
                score[0] += 1.0 * losspointarm
                score[1] += 1.0 * winpointarm  # black wins
        # 2. Get the score from armageddon game where the first player is black.
        dfb_arm = df[(df.Black == p) & (df.White == op) & (df.Arm == 1)]
        for i in range(len(dfb_arm)):
            r = dfb_arm.iloc[i]['Result']
            if r == '0-1':
                score[0] += 1.0 * winpointarm
                score[1] += 1.0 * losspointarm
            elif r == '1-0':
                score[0] += 1.0 * losspointarm
                score[1] += 1.0 * winpointarm
            elif r == '1/2-1/2':
                score[0] += 1.0 * winpointarm  # black wins
                score[1] += 1.0 * losspointarm
    return score


def save(df: pd.DataFrame, fn: str, tablecolor: str = 'blue_light') -> None:
    """Save the dataframe.

    The output can be a csv, txt and html.
    Args:
      df: A pandas dataframe.
      fn: The output filename.
      tablecolor: The table color for html output.
    """
    ext = Path(fn).suffix
    if ext == '.html':
        html_table = build_table(
            df,
            tablecolor,
            font_size='medium',
            text_align='center',
            font_family='Calibri, Verdana, Tahoma, Georgia, serif, arial')
        with open(fn, 'w') as f:
            f.write(html_table)
    elif ext == '.csv':
        df.to_csv(fn, index=False)
    else:
        df.to_string(fn, index=False)
