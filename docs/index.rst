.. PgnHelper documentation master file, created by
   sphinx-quickstart on Tue Jun 21 09:36:00 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation of PgnHelper
==========================

PgnHelper is an application that can ``sort games;`` ``add ECO codes, opening and variation
names;`` and generate a ``round-robin result table`` with rating change and tie-break
scores.

First install the pgnhelper package see the :ref:`Installation Overview` guide.

Features
--------

1. Add ECO codes, Opening and Variation names
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Command line::

   pgnhelper addeco --inpgnfn manila1974.pgn --outpgnfn out_manila1974.pgn --inecopgnfn eco.pgn

Sample output::

   [Event "Manila"]
   [Site "Manila"]
   [Date "1974.??.??"]
   [Round "10"]
   [White "Naranja, Renato"]
   [Black "Petrosian, Tigran V"]
   [Result "1/2-1/2"]
   [BlackElo "2640"]
   [ECO "A15"]
   [ECOT "D90"]
   [Opening "English"]
   [OpeningT "Gruenfeld"]
   [VariationT "Three knights variation"]
   [WhiteElo "2395"]
   
   1. c4 Nf6 2. Nf3 g6 3. d4 Bg7 4. Nc3 d5 5. cxd5 Nxd5 6. Bd2 Nb6 7. Qc2 Nc6
   8. Rd1 O-O 9. e3 Bf5 10. Qc1 a5 11. Be2 a4 12. O-O Qc8 13. d5 Nb8 14. e4 Bg4
   15. Bh6 c6 16. Bxg7 Kxg7 17. Qe3 N8d7 1/2-1/2

The new ECOT, OpeningT and VariationT (T=Transposition) are based from the
input eco.pgn file. See the :ref:`Usage Overview` section further informations.

The ``ECO`` tag is based from the first 2 moves of the game while the ``ECOT`` is
based from the first 12 moves of the game.


2. Sort games
^^^^^^^^^^^^^

.. code-block:: python
   :caption: Sort games by eco tag.

   pgnhelper sort --inpgnfn airthings.pgn --outpgnfn sorted_airthings.pgn --sort-tag eco --sort-direction hightolow

.. code-block:: python
   :caption: Sort games by white tag.

   pgnhelper sort --inpgnfn airthings.pgn --outpgnfn sorted_airthings.pgn --sort-tag white --sort-direction hightolow

Available sort tags::

   event, site , date, round, white, black, eco, ecot, plycount

3. Generate round-robin table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
   :caption: Round-robin with normal scoring

   pgnhelper roundrobin --inpgnfn superbet_classic_2022_bucharest.pgn --output scb2022.txt

Sample output with ``rating change`` and ``tie-break scores DE, Wins and SB``::

 Rank                     Name  Rating   RChg    1    2    3    4    5    6    7    8    9   10  Games  Score  Score%  DE  Wins    SB
    1           Aronian, Levon    2765   9.50    x  0.5  1.0  1.0  0.5  0.5  0.5  0.5  0.5  0.5      9    5.5   61.11 1.5     2 24.75
    2               So, Wesley    2776   7.93  0.5    x  0.5  0.5  0.5  0.5  1.0  0.5  1.0  0.5      9    5.5   61.11 1.0     2 23.50
    3  Vachier-Lagrave, Maxime    2750  11.64  0.0  0.5    x  0.5  1.0  0.5  0.5  1.0  0.5  1.0      9    5.5   61.11 0.5     3 23.00
    4 Dominguez Perez, Leinier    2753   1.21  0.0  0.5  0.5    x  0.5  1.0  0.5  0.0  1.0  0.5      9    4.5   50.00 1.5     2 19.50
    5         Caruana, Fabiano    2786  -3.49  0.5  0.5  0.0  0.5    x  0.5  0.5  0.5  1.0  0.5      9    4.5   50.00 1.0     1 19.25
    6      Deac, Bogdan-Daniel    2671  12.62  0.5  0.5  0.5  0.0  0.5    x  0.5  0.5  0.5  1.0      9    4.5   50.00 0.5     1 19.75
    7      Nepomniachtchi, Ian    2773  -6.64  0.5  0.0  0.5  0.5  0.5  0.5    x  1.0  0.0  0.5      9    4.0   44.44 1.0     1 18.00
    8        Firouzja, Alireza    2804 -11.04  0.5  0.5  0.0  1.0  0.5  0.5  0.0    x  0.5  0.5      9    4.0   44.44 0.0     1 18.00
    9   Mamedyarov, Shakhriyar    2759  -9.65  0.5  0.0  0.5  0.0  0.0  0.5  1.0  0.5    x  0.5      9    3.5   38.89 0.5     1 15.50
   10         Rapport, Richard    2776 -12.07  0.5  0.5  0.0  0.5  0.5  0.0  0.5  0.5  0.5    x      9    3.5   38.89 0.5     0 15.75


.. code-block:: python
   :caption: Round-robin with armageddon tie-break

   gnhelper roundrobin --inpgnfn norwaychess.pgn --armageddon-file norwaychess_arm.pgn --output norwaychess.html --win-point 3.0 --win-point-arm 1.5 --loss-point-arm 1.0 --show-max-score

Sample output::

 Rank                    Name  Rating   RChg    1    2    3    4    5    6    7    8    9   10  Games  Score  MaxScore  Score%  DE  Wins
    1         Carlsen, Magnus    2864  -0.05    x  3.0  1.0  1.5  1.0  3.0  1.5  1.0  3.0  1.5      9   16.5      27.0   61.11 0.0     0
    2  Mamedyarov, Shakhriyar    2759   9.31  0.0    x  3.0  1.0  1.5  3.0  1.5  1.5  1.0  3.0      9   15.5      27.0   57.41 0.0     0
    3      Anand, Viswanathan    2751   5.44  1.5  0.0    x  3.0  1.0  1.5  3.0  1.5  1.5  1.5      9   14.5      27.0   53.70 0.0     0
    4 Vachier-Lagrave, Maxime    2750   5.58  1.0  1.5  0.0    x  3.0  1.5  1.5  3.0  1.0  1.5      9   14.0      27.0   51.85 0.0     0
    5              So, Wesley    2776  -3.09  1.5  1.0  1.5  0.0    x  1.5  1.0  1.5  3.0  1.5      9   12.5      27.0   46.30 0.0     0
    6             Giri, Anish    2761  -0.97  0.0  0.0  1.0  1.0  1.0    x  1.5  3.0  3.0  1.5      9   12.0      27.0   44.44 0.0     0
    7        Topalov, Veselin    2730  -1.60  1.0  1.0  0.0  1.0  1.5  1.0    x  1.5  1.5  1.0      9    9.5      27.0   35.19 1.5     0
    8             Tari, Aryan    2654   8.79  1.5  1.0  1.0  0.0  1.0  0.0  1.0    x  1.0  3.0      9    9.5      27.0   35.19 1.0     1
    9       Radjabov, Teimour    2753 -14.84  0.0  1.5  1.0  1.5  0.0  0.0  1.0  1.5    x  1.5      9    8.0      27.0   29.63 0.0     0
   10               Wang, Hao    2744  -8.57  1.0  0.0  1.0  1.0  1.0  1.0  1.5  0.0  1.0    x      9    7.5      27.0   27.78 0.0     0


4. Calculate the Elo rating change of a player
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Game result::

   [Event "FIDE Candidates 2022"]
   [Site "Madrid ESP"]
   [Date "2022.06.17"]
   [Round "1"]
   [White "Ding Liren"]
   [Black "Nepomniachtchi,I"]
   [Result "0-1"]
   [WhiteElo "2806"]
   [BlackElo "2766"]
   [EventDate "2022.06.16"]
   [ECO "A20"]


.. code-block:: python
   :caption: Calculate the rating change of Nepomniachtchi.
   :linenos:
   :emphasize-lines: 7,9

   import pgnhelper.elo

   white_rating = 2806
   black_rating = 2766
   white_point = 0
   black_point = 1   
   expected_score = pgnhelper.elo.expected_score(black_rating, white_rating)
   k = 10
   rating_change = k * (black_point - expected_score)
   print(rating_change)  # 5.573116337622928


.. code-block:: python
   :caption: Calculate the rating change of Ding Liren.
   :linenos:
   :emphasize-lines: 7,9

   import pgnhelper.elo

   white_rating = 2806
   black_rating = 2766
   white_point = 0
   black_point = 1   
   expected_score = pgnhelper.elo.expected_score(white_rating, black_rating)
   k = 10
   rating_change = k * (white_point - expected_score)
   print(rating_change)  # -5.573116337622928

5. Generate opening stats
^^^^^^^^^^^^^^^^^^^^^^^^^

* Generate opening stats

::

   >>> import pgnhelper.eco
   >>> import pgnhelper.record
   >>> df = pgnhelper.eco.get_opening_stats("./pgn/candidates_zurich_1953.pgn")
   >>> df

::

                       Opening  Count  Count%
   0     King's Indian Defence     44   20.95
   1              Nimzo-Indian     41   19.52
   2                  Sicilian     23   10.95
   3                   English     18    8.57
   4   Queen's Gambit Declined     16    7.62
   5    Queen's Indian Defence     12    5.71
   6                 Ruy Lopez     10    4.76
   7                Old Indian      7    3.33
   8                    French      6    2.86
   9                   Catalan      4    1.90
   10            King's Indian      4    1.90
   11                 QGD Slav      4    1.90
   12                   Benoni      3    1.43
   13                    Dutch      3    1.43
   14                Gruenfeld      3    1.43
   15                      QGA      3    1.43
   16                Zukertort      3    1.43
   17                Caro-Kann      2    0.95
   18            Neo-Gruenfeld      2    0.95
   19        Queen's pawn game      2    0.95

.. Note::

   Your game must have an opening info in the header.


Links
-----


* `Github pgnhelper <https://github.com/fsmosca/pgnhelper>`_
* `Pypi pgnhelper <https://pypi.org/project/pgnhelper/>`_


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:
   
   installation
   uninstallation
   help
   usage   
   pytest
   changelog
   readthedocs
   api
