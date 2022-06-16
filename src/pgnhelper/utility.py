from typing import List, TypeVar


PandasDataFrame = TypeVar('pandas.core.frame.DataFrame')


def get_encounter_score(df: PandasDataFrame, p: str, op: str, winpoint=1.0, drawpoint=0.5) -> List[float]:
    """Calculate the scores between the two players p and op based from the given df.

    :param df: A pandas dataframe containing players match results.
    :param p: A player name.
    :param op: Opponent player name.
    :return: A list of score for p and op, score[<p score>, <op score>].
    """
    score = [0, 0]
    dfw = df[(df.White == p) & (df.Black == op)]
    dfb = df[(df.Black == p) & (df.White == op)]

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
    return score
