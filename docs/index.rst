.. PgnHelper documentation master file, created by
   sphinx-quickstart on Tue Jun 21 09:36:00 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation of PgnHelper
==========================

PgnHelper is an application that can ``sort games;`` ``add ECO codes, opening and variation
names;`` generates a ``round-robin``, ``swiss`` and ``standing`` tables with rating change
and tie-break scores; and ``opening stats.``

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
input eco.pgn file. See the :ref:`Usage Overview` section for further informations.

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


5. Generate swiss table
^^^^^^^^^^^^^^^^^^^^^^^

::
  
     pgnhelper swiss --inpgnfn "./pgn/fide_grand_swiss_2021_riga.pgn" --output "fide_swiss.txt"
  
     # pgnhelper swiss --inpgnfn "./pgn/fide_grand_swiss_2021_riga.pgn" --output "fide_swiss.html"
     # pgnhelper swiss --inpgnfn "./pgn/fide_grand_swiss_2021_riga.pgn" --output "fide_swiss.csv"
  
::
  
   Rank                          Name  Rating   RChg    R1    R2    R3    R4    R5    R6    R7    R8    R9   R10   R11  Games  Score  Score%  TB1  TB2   TB3  TB4  TB5  TB6
      1             Firouzja, Alireza    2770  11.31  93W1  35B1   7W1   4B=   6W=   8B=  33W1  31W1   2B0   9W1   3B=     11    8.0   72.73  0.0  0.0  0.00  0.0    0    0
      2              Caruana, Fabiano    2800   1.06  55W1  18B=  36W=  35B=   9W1  33B=  13W=  24B1   1W1   6B=   7W=     11    7.5   68.18 67.0 72.5 49.75  0.0    4    1
      3              Oparin, Grigoriy    2654  21.62  62W=  78B1  17W=  70B=  26W=   5B=  73W1  19B1   7W=  23B1   1W=     11    7.5   68.18 63.5 68.5 45.75  0.0    4    3
      4                    Yu, Yangyi    2704   9.20   5W=  63B1  61W1   1W=  49B=  13B=  15W=  28B=  33W1   8B=   6W=     11    7.0   63.64 66.5 72.0 44.50  0.0    3    1
      5               Keymer, Vincent    2630  22.06   4B=  27W1  25B=  10W=  59B=   3W=  24B0  82W1  53B1  29W1   9B=     11    7.0   63.64 65.5 70.0 43.25  0.0    4    1
      6       Vachier-Lagrave, Maxime    2763   2.12  52B=  51W1  71B=  60W1   1B=  32W1  31B=   8W=  11B=   2W=   4B=     11    7.0   63.64 65.0 70.0 43.50  0.0    3    0
      7              Predke, Alexandr    2666  14.22  46B1  54W1   1B0  47W=  42B1  31W0  57B1  49W1   3B=  11W=   2B=     11    7.0   63.64 64.5 70.0 42.25  0.0    5    3
      8                Shirov, Alexei    2659  16.99  43B=  87W1  50B=  92W1  36B1   1W=  14B=   6B=  23W=   4W=  10B=     11    7.0   63.64 64.5 68.5 41.50  0.0    3    1
      9             Howell, David W L    2658  15.43  82B1  92W=  72B=  50W=   2B0  54W1  47B1  14W1  12W1   1B0   5W=     11    7.0   63.64 62.5 66.5 40.25  0.0    5    2
     10           Sargissian, Gabriel    2664  10.56  72W=  83B=  94W1   5B=  70W1  15B=  18W=  34B=  28W1  13B=   8W=     11    7.0   63.64 61.5 65.5 40.50  0.0    3    0
     11         Anton Guijarro, David    2658  13.25  37W=  70B=  62W1  17B0  98W1  91B1  19W=  21B1   6W=   7B=  13W=     11    7.0   63.64 61.0 65.0 39.25  0.0    4    2
     12                Korobov, Anton    2690   6.07  48B=  20W1  47B=  42W=  50B1  49W=  17B=  41W1   9B0  34W=  31B1     11    7.0   63.64 60.5 66.0 41.50  0.0    4    2
     13                Sevian, Samuel    2654  15.89  80B=  84W1  92B=  72W1  32B=   4W=   2B=  53W1  30B=  10W=  11B=     11    7.0   63.64 60.5 64.5 39.75  0.0    3    0
     14              Esipenko, Andrey    2720   3.08  58B=  42W=  81B=  63W1  71B=  56W1   8W=   9B0  64B1  31W1  15B=     11    7.0   63.64 60.0 64.5 40.00  0.0    4    1
     15           Deac, Bogdan-Daniel    2643  15.05  89B= 104W= 106B1  53W=  29B1  10W=   4B=  25W=  18B=  38B1  14W=     11    7.0   63.64 60.0 63.0 39.25  0.0    3    3
     16           Artemiev, Vladislav    2699   4.40  76B1  50W=  75B=  31W=  51B=  47W=  48B=  52W=  49B1  17W=  34B1     11    7.0   63.64 56.5 61.5 39.00  0.0    3    3
  
     ...

Tie-breaks::

   TB1 = Buchholz Cut 1
   TB2 = Buchholz
   TB3 = Sonneborn-Berger
   TB4 = Direct Encounter
   TB5 = Number of wins
   TB6 = Number of wins as black


6. Generate opening stats
^^^^^^^^^^^^^^^^^^^^^^^^^

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
   credits
   links
   api
