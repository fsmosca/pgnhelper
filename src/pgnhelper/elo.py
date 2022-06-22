from typing import Union

import pandas as pd


def expected_score(rating_a: int, rating_b: int) -> float:
    """Calculates the expected score of player_a against player_b.

    Args:
      rating_a: Rating of player_a
      rating_b: Rating of player_b
    
    Returns:
      expected score of player_a

    Example::

      >>> import pgnhelper.elo
      >>> white_elo = 2600
      >>> black_elo = 2500
      >>> score = pgnhelper.elo.expected_score(white_elo, black_elo)
      >>> score
      0.6400649998028851
    """
    rd = rating_b - rating_a
    return 1 / (1+10**(rd/400))


def add_rating_change(df: pd.DataFrame, is_rating: bool, k: int=10) -> pd.DataFrame:
    """Adds rating change columns to existing df.

    Args:
      df: A dataframe of players match records.
      is_rating: True if players have rating.
      k: The k factor.

    Returns:
      A dataframe of game records with elo rating change columns.
      [Round, White, Black, WElo, BElo, Result, Wpt, Bpt, Arm, WRChg, BRChg]
    """
    if not is_rating:
        df['WRChg'] = 0
        df['BRChg'] = 0
    else:
        df['WRChg'] = k * (df.Wpt - expected_score(df.WElo, df.BElo))
        df['BRChg'] = k * (df.Bpt - expected_score(df.BElo, df.WElo))
    return df


def get_rating(df: pd.DataFrame, p: str) -> Union[int, str]:
    """Gets the rating of player p.

    Args:
      df: A dataframe of players match records.
      p: A player name.

    Returns:
      rating of player p
    """
    dfr = df.loc[df.White == p]
    if len(dfr):
        return dfr.iloc[0]['WElo']
    dfr = df.loc[df.Black == p]
    if len(dfr):
        return dfr.iloc[0]['BElo']
    return '?'


def get_rating_change(df: pd.DataFrame, p: str, k: int=10) -> float:
    """Gets the rating change of player p.

    The given df has a rating change column for each side. This rating
    change column was calculated using a k factor with value 10. The
    k parameter if not 10 will be used to recalculate the rating change
    for the given player.

    Armageddon games are not included in the returned rating change value.

    Args:
      df: A dataframe of players match records.
      p: A player named p.
      k: The rating change k factor.

    Returns:
      rating change

    Eample::

      >>> import pgnhelper.roundrobin
      >>> import pgnhelper.elo
      >>> df, players, is_rating = pgnhelper.roundrobin.get_pgn_data("./pgn/superbet_classic_2022_bucharest.pgn")
      >>> players
      ['Firouzja, Alireza', 'Aronian, Levon', 'So, Wesley', 'Nepomniachtchi, Ian', 'Caruana, Fabiano', 'Vachier-Lagrave, Maxime', 'Deac, Bogdan-Daniel', 'Mamedyarov, Shakhriyar', 'Dominguez Perez, Leinier', 'Rapport, Richard']
      >>> rc_levon = pgnhelper.elo.get_rating_change(df, "Aronian, Levon", k=10)
      >>> rc_levon
      9.496967974633389
    """
    dfw = df.loc[(df.White == p) & (df.Arm == 0)]
    dfb = df.loc[(df.Black == p) & (df.Arm == 0)]
    s = dfw.WRChg.sum() + dfb.BRChg.sum()
    if k != 10:
        s = s / 10
        return k * s
    return s
