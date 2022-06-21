Usage
=====

Command line
^^^^^^^^^^^^

Add ECO::

   pgnhelper addeco --inpgnfn airthings.pgn --outpgnfn out_airthings.pgn
                    --inecopgnfn eco.pgn

Sort::

   pgnhelper sort --inpgnfn airthings.pgn --outpgnfn sorted_airthings.pgn
                  --sort-tag eco --sort-direction hightolow


Script
^^^^^^

Add ECO::

    import pgnhelper.run

    a = pgnhelper.run.PgnHelper(
        'addeco',
        inpgnfn='mygames.pgn',
        outpgnfn='out_eco.pgn',
        inecopgnfn='eco.pgn')
    a.start()

Sort games::

    import pgnhelper.run

    a = pgnhelper.run.PgnHelper(
        'sort',
        inpgnfn='mygames.pgn',
        outpgnfn='out_sorted.pgn',
        sort_tag='eco',
        sort_direction='hightolow')
    a.start()

Generate round-robin table::

    import pgnhelper.roundrobin

    df = pgnhelper.roundrobin.round_robin(
        'airthings.pgn',
        winpoint=1.0,
        drawpoint=0.5)

    # Print to console.
    print(df.to_string(index=False))

    # Save to html 
    pgnhelper.roundrobin.save_roundrobin_table(df, 'airthings.html')
