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

**4. Generates a round-robin table with armageddon tie-break as in Norway Chess**::

   pgnhelper roundrobin --inpgnfn norwaychess.pgn --armageddon-file norwaychess_arm.pgn --output norwaychess.html --win-point 3.0 --win-point-arm 1.5 --loss-point-arm 1.0 --show-max-score

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
    df = pgnhelper.roundrobin.round_robin(
        'airthings.pgn',
        winpoint=3.0,
        drawpoint=1.0)

    # Print to console.
    print(df.to_string(index=False))

    # Save to html.
    pgnhelper.roundrobin.save_roundrobin_table(df, 'airthings.html')

    # Save to csv.
    df.to_csv('airthings.csv', index=False)

**4. Generate round-robin table with armageddon games as tie-break as in Norway Chess**::

    """
    Generate a round-robin table and save results to txt and html.
    """

    import pgnhelper.roundrobin

    df = pgnhelper.roundrobin.round_robin(
        './pgn/norway_chess_2022_classical.pgn',
        armageddonfile='./pgn/norway_chess_2022_armageddon.pgn',
        winpoint=3.0,
        winpointarm=1.5,
        losspointarm=1.0)
    df.to_string('norway_chess.txt', index=False)
    pgnhelper.roundrobin.save_roundrobin_table(df, 'norway_chess.html')

