"""Add eco, opening and variation names to the input pgn file.

The eco codes, opening and variations names are coming from
the file eco.pgn that you have to supply to pgnhelper for this to work.

eco.pgn file sources:

  * eco.pgn from `pgn-extract <https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/>`_
  * eco.pgn from `my eco repository in github <https://github.com/fsmosca/eco>`_
  * eco.pgn from `pgnhelper repository <https://github.com/fsmosca/pgnhelper>`_

Example::

  >>> import pgnhelper.eco
  >>> pgnhelper.eco.add_eco("./pgn/candidates_zurich_1953.pgn", "eco_cz.pgn", "./eco/eco.pgn")

Example output from ``eco_cz.pgn``::

  [Event "ct"]
  [Site "Zurich"]
  [Date "1953.??.??"]
  [Round "01"]
  [White "Szabo L"]
  [Black "Geller E"]
  [Result "0-1"]
  [ECO "A15"]
  [ECOT "E02"]
  [Opening "English"]
  [OpeningT "Catalan"]
  [Variation "Anglo-Indian"]
  [VariationT "open, 5.Qa4"]

  1. c4 Nf6 2. g3 e6 3. Bg2 d5 4. d4 dxc4 5. Qa4+ Nbd7 ...

Note there are ``ECOT, OpeningT, and VariationT,`` these are new tags where
T refers to ``Transposition.`` The ECO ``A15`` is the ECO based on the first
2 moves and ECOT ``E02`` is the ECO after 12 moves.
"""


import chess.pgn
import pandas as pd
import pgnhelper.record


def create_eco_db(inecopgnfn: str):
    """Creats a dictionary of eco data.

    Args:
      inecopgnfn: The eco.pgn file to be converted to a dictionary.
    """
    eco_db = {}
    with open(inecopgnfn, 'r') as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            try:
                eco = game.headers['ECO']
            except KeyError:
                continue
            try:
                opening = game.headers['Opening']
            except KeyError:
                continue
            try:
                variation = game.headers['Variation']
            except KeyError:
                variation = None
            node = game
            node_end = node.end()
            end_board = node_end.board()
            epd = end_board.epd()
            eco_db.update({epd: {'eco': eco, 'opening': opening, 'variation': variation}})
    return eco_db


def add_eco(inpgnfn: str, outpgnfn: str, inecopgnfn: str, ply: int = 4, maxply: int = 24):
    """Add eco, opening and variation names to the pgn file.

    Args:
      inpgnfn: The input pgn file.
      outpgnfn: The output file.
      inecopgnfn: The eco.pgn file.
      ply: The game ply to start classifying the opening.
      maxply: The max game ply to stop classifying the opening.
    """
    eco_db = create_eco_db(inecopgnfn)
    mygame = None
    with open(inpgnfn, 'r') as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            if mygame is None:
                mygame = game
            first_eco, eco_t = None, None
            first_opening, opening_t = None, None
            first_variation, variation_t = None, None
            for node in game.mainline():
                board = node.board()
                gply = board.ply()
                epd = board.epd()

                # After the first move check the position if it is in eco db.
                if gply >= 1:
                    if epd in eco_db:

                        # Update first eco up to a given ply only.
                        if gply <= ply:
                            first_eco = eco_db[epd]['eco']
                            first_opening = eco_db[epd]['opening']
                            first_variation = eco_db[epd]['variation']

                        # Else update eco by transposition.
                        else:
                            eco_t = eco_db[epd]['eco']
                            opening_t = eco_db[epd]['opening']
                            variation_t = eco_db[epd]['variation']

                    if gply >= maxply:
                        break
            if first_eco is not None:
                mygame.headers['ECO'] = first_eco
                mygame.headers['Opening'] = first_opening
                if first_variation is not None:
                    mygame.headers['Variation'] = first_variation
            if eco_t is not None:
                mygame.headers['ECOT'] = eco_t
                mygame.headers['OpeningT'] = opening_t
                if variation_t is not None:
                    mygame.headers['VariationT'] = variation_t

    with open(outpgnfn, 'w') as f:
        f.write(f"{mygame}\n")


def get_opening_stats(fn: str, is_arm: bool = False):
    """Generates a dataframe of opening stats.

    Opening, counts
    Sicilian, 4
    ........, ...

    Args:
      fn: The pgn filename.

    Returns:
      A dataframe of Opening and count
    """
    df, _, _ = pgnhelper.record.get_pgn_data(fn, is_arm=is_arm)
    opening = df.Opening.unique()

    data = []

    for o in opening:
        dfo = df.loc[df.Opening == o]
        data.append([o, len(dfo)])

    dfr = pd.DataFrame(data, columns=['Opening', 'Count'])
    dfr = dfr.sort_values(by=['Count', 'Opening'], ascending=[False, True])
    dfr = dfr.reset_index(drop=True)
    dfr['Count%'] = round(100 * dfr.Count / dfr.Count.sum(), 2)
    return dfr
