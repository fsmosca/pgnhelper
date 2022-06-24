.. _Usage Overview:

Usage
=====

Command line
^^^^^^^^^^^^

**1. Add ECO**::

   pgnhelper addeco --inpgnfn airthings.pgn --outpgnfn out_airthings.pgn --inecopgnfn eco.pgn

.. note::
   You can get the `eco.pgn <https://github.com/fsmosca/pgnhelper/tree/main/eco>`_ from the pgnhelper github repository.

**2. Sort**::

   pgnhelper sort --inpgnfn airthings.pgn --outpgnfn sorted_airthings.pgn --sort-tag eco --sort-direction hightolow

**3. Generates a round-robin result table**::

   pgnhelper roundrobin --inpgnfn superbet_classic_2022_bucharest.pgn --output scb2022.txt

Output with ``rating change`` and ``tie-break scores DE, Wins and SB``::

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

**4. Generates a round-robin table with armageddon tie-break as in Norway Chess**::

   pgnhelper roundrobin --inpgnfn norwaychess.pgn --armageddon-file norwaychess_arm.pgn --output norwaychess.html --win-point 3.0 --win-point-arm 1.5 --loss-point-arm 1.0 --show-max-score

::

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

**5. Generates standing table**::

   pgnhelper standing --inpgnfn "./pgn/interzonal_1970_palma_de_mallorca.pgn" --output palma.txt

::
    
   Rank               Name  Games  Score  Score%  DE  Wins     SB
      1          Fischer R     23   18.5   80.43 0.0     0   0.00
      2           Geller E     23   15.0   65.22 1.5     8 167.00
      3           Larsen B     23   15.0   65.22 1.0     9 167.50
      4          Huebner R     23   15.0   65.22 0.5    10 155.25
      5          Uhlmann W     23   14.0   60.87 0.5    10 141.50
      6         Taimanov M     23   14.0   60.87 0.5     8 146.50
      7         Portisch L     23   13.5   58.70 0.5     7 149.75
      8          Smyslov V     23   13.5   58.70 0.5     7 141.00
      9         Gligoric S     23   13.0   56.52 0.5     7 135.50
     10      Polugaevsky L     23   13.0   56.52 0.5     5 146.75
     11          Mecking H     23   12.5   54.35 0.5     7 130.00
     12            Panno O     23   12.5   54.35 0.5     6 130.75
     13             Hort V     23   11.5   50.00 0.0     0   0.00
     14            Ivkov B     23   10.5   45.65 0.0     0   0.00
     15            Minic D     23   10.0   43.48 1.0     5  96.00
     16          Suttles D     23   10.0   43.48 0.0     4 105.75
     17        Reshevsky S     23    9.5   41.30 0.0     0   0.00
     18          Addison W     23    9.0   39.13 0.5     3  95.25
     19        Matulovic M     23    9.0   39.13 0.5     2  98.50
     20            Filip M     23    8.5   36.96 1.5     1  91.50
     21          Ujtumen T     23    8.5   36.96 1.0     5  85.25
     22          Naranja R     23    8.5   36.96 0.5     5  88.75
     23        Rubinetti J     23    6.0   26.09 0.0     0   0.00
     24 Jimenez Zerquera E     23    5.5   23.91 0.0     0   0.00


Script
^^^^^^

**1. Add ECO**::

    import pgnhelper.app

    a = pgnhelper.app.PgnHelper(
        'addeco',
        inpgnfn='mygames.pgn',
        outpgnfn='out_eco.pgn',
        inecopgnfn='eco.pgn')
    a.start()

**2. Sort games**::

    import pgnhelper.app

    a = pgnhelper.app.PgnHelper(
        'sort',
        inpgnfn='mygames.pgn',
        outpgnfn='out_sorted.pgn',
        sort_tag='eco',
        sort_direction='hightolow')
    a.start()

**3. Generate round-robin table**::

    """
    The output can be a pandas dataframe, txt, csv and html.
    """

    import pgnhelper.roundrobin

    # Get the dataframe output.
    rr = pgnhelper.roundrobin.RoundRobin(
        "airthings.pgn",
        winpoint=3.0, drawpoint=1.0)
    df = rr.table()

    # Print to console.
    print(df.to_string(index=False))

    # Save to html.
    rr.save_table(df, "airthings.html")

    # Save to csv.
    df.to_csv("airthings.csv", index=False)

**4. Generate round-robin table with armageddon games as tie-break as in Norway Chess**::

    """
    Generate a round-robin table and save results and html.
    """

    import pgnhelper.roundrobin

    rr = pgnhelper.roundrobin.RoundRobin(
        "./pgn/norway_chess_2022_classical.pgn",
        infnarm="./pgn/norway_chess_2022_armageddon.pgn",
        winpoint=3.0,
        winpointarm=1.5,
        losspointarm=1.0)
    df = rr.table()
    rr.save_table(df, "norway_chess.html")
