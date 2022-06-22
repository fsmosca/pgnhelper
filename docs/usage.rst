Usage
=====

Command line
^^^^^^^^^^^^

**1. Add ECO**::

   pgnhelper addeco --inpgnfn airthings.pgn --outpgnfn out_airthings.pgn
                    --inecopgnfn eco.pgn

.. note::
   You can get the `eco.pgn <https://github.com/fsmosca/pgnhelper/tree/main/eco>`_ from the pgnhelper github repository.

**2. Sort**::

   pgnhelper sort --inpgnfn airthings.pgn --outpgnfn sorted_airthings.pgn
                  --sort-tag eco --sort-direction hightolow

**3. Normal round-robin table**::

   pgnhelper roundrobin --inpgnfn airthings.pgn --output airthings.html

**4. Round-robin with armageddon tie-break as in Norway Chess**::

   pgnhelper roundrobin --inpgnfn norwaychess.pgn --armageddon-file norwaychess_arm.pgn
                        --output norwaychess.html --win-point 3.0
                        --win-point-arm 1.5 --loss-point-arm 1.0


Script
^^^^^^

**1. Add ECO**::

    import pgnhelper.run

    a = pgnhelper.run.PgnHelper(
        'addeco',
        inpgnfn='mygames.pgn',
        outpgnfn='out_eco.pgn',
        inecopgnfn='eco.pgn')
    a.start()

**2. Sort games**::

    import pgnhelper.run

    a = pgnhelper.run.PgnHelper(
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
        winpoint=1.0,
        drawpoint=0.5)

    # Print to console.
    print(df.to_string(index=False))

    # Save to html.
    pgnhelper.roundrobin.save_roundrobin_table(df, 'airthings.html')

    # Save to csv.
    df.to_csv('airthings.csv', index=False)
