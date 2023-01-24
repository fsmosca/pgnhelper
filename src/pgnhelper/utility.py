"""Helps build the round-robin result table.
"""


from typing import List
import pandas as pd
from pathlib import Path


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


def df_to_html(df: pd.DataFrame, fn: str) -> None:
    """Converts pandas dataframe to basic html table.

    Read the df and write html in the fn.

    Args:
      df: Pandas dataframe.
      fn: the output file, can be csv, txt or html.

    Returns:
      Nothing
    """
    dict_data = [df.to_dict(), df.to_dict('index')]

    htmldf = '<!DOCTYPE html>\n'
    htmldf += '<html lang="en">\n'
    htmldf += '  <head>\n'
    htmldf += '    <meta charset="utf-8">\n'
    htmldf += '    <meta name="viewport" content="width=device-width, initial-scale=1">\n'
    htmldf += '    <title>PGN Helper</title>\n'

    # Define style.
    htmldf += '    <style>\n'
    htmldf += '        body {margin-top: 25px;}\n'

    htmldf += '        table, th, td {\n'
    htmldf += '          border: 1px solid black;\n'
    htmldf += '          border-collapse: collapse;\n'
    htmldf += '          text-align: center;\n'
    htmldf += '        }\n\n'
        
    htmldf += '        th, td {\n'
    htmldf += '          padding: 5px;\n'
    htmldf += '        }\n\n'
        
    htmldf += '        tr:nth-child(even) {\n'
    htmldf += '          background-color: #D5DBDB;\n'
    htmldf += '        }\n'
    htmldf += '        tr:hover {background-color: #EBDEF0;}\n\n'

    htmldf += '        table.center {\n'
    htmldf += '          margin-left: auto;\n'
    htmldf += '          margin-right: auto;\n'
    htmldf += '        }\n'

    htmldf += '    </style>\n'
    htmldf += '  </head>\n\n'

    htmldf += '  <body>\n'

    # Define table.
    htmldf += '  <div style="overflow-x: auto;">\n'  # responsive
    htmldf += '    <table class="center">\n'

    # Define header row.
    htmldf += '<tr>\n'
    for key in dict_data[0].keys():
        htmldf += '<th>' + str(key) + '</th>\n'
    htmldf += '</tr>\n'

    # Define data.
    for key in dict_data[1].keys():
        htmldf += '<tr>\n'
        for subkey in dict_data[1][key]:
            htmldf += '<td>' + str(dict_data[1][key][subkey]) + '</td>\n'
        htmldf += '</tr>\n'

    htmldf += '    </table>\n'
    htmldf += '  </div>\n'

    htmldf += '  </body>\n'
    htmldf += '</html>\n'

    # Write html.
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(htmldf)


def save(df: pd.DataFrame, fn: str) -> None:
    """Save the dataframe.

    The output can be a csv, txt and html.
    Args:
      df: A pandas dataframe.
      fn: The output filename.
    """
    ext = Path(fn).suffix
    if ext == '.html':
        df_to_html(df, fn)
    elif ext == '.csv':
        df.to_csv(fn, index=False)
    else:
        df.to_string(fn, index=False)
