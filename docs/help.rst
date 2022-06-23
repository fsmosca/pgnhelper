.. _Help Overview:

Help
=====

**General help**::

   pgnhelper --help


::

    usage: pgnhelper [-h] [-v] {sort,addeco,roundrobin} ...

    positional arguments:
      {sort,addeco,roundrobin}
        sort                Sort the games from the given pgn file based on the given game tags. e.g. pgnhelper sort mygames.pgn --outpgnfn out.pgn --sort-tag opening --sort-
                            direction hightolow
        addeco              Add eco and ecot codes, opening and variation names to the input pgn file. The eco, opening etc. are from the given input file eco.pgn. e.g.
                            pgnhelper addeco --inpgnfn mygames.pgn --inecopgnfn eco.pgn --outpgnfn out.pgn
        roundrobin          Generate round-robin table results from the input pgn file. The output can be html, csv and txt. e.g. pgnhelper roundrobin --inpgnfn candidates.pgn
                            --output candidates.html
    
    options:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit


**Sort help**::

    pgnhelper sort --help

::

    usage: pgnhelper sort [-h] --inpgnfn INPGNFN --outpgnfn OUTPGNFN [--sort-tag SORT_TAG] [--sort-direction SORT_DIRECTION] [--encoding ENCODING]

    options:
      -h, --help            show this help message and exit
      --inpgnfn INPGNFN     Write the input pgn filename, required.
      --outpgnfn OUTPGNFN   Write the output pgn filename, required, mode=overwrite.
      --sort-tag SORT_TAG   Sort the games by tag. [default=eco, value=(eco | ecot | event | date | round | white | black | site | plycount)]. e.g. --sort-tag event
      --sort-direction SORT_DIRECTION
                            Write the direction to sort the games. [default=lowtohigh, value=(lowtohigh | hightolow)].
      --encoding ENCODING   Encoding used in reading pgn file when sorting, not required. [default=utf-8, value=(utf-8 | ISO-8859-1)]. If you encounter an error like
                            "UnicodeDecodeError: utf-8 codec cannot decode ..." you can try, --encoding ISO-8859-1

**Add eco help**::

    pgnhelper addeco --help

::

    usage: pgnhelper addeco [-h] --inpgnfn INPGNFN --outpgnfn OUTPGNFN --inecopgnfn INECOPGNFN

    options:
      -h, --help            show this help message and exit
      --inpgnfn INPGNFN     Write the input pgn filename, required.
      --outpgnfn OUTPGNFN   Write the output pgn filename, required, mode=overwrite.
      --inecopgnfn INECOPGNFN
                            Write the reference eco.pgn filename, required.


**Round-robin help**::

    pgnhelper roundrobin --help

::

    usage: pgnhelper roundrobin [-h] --inpgnfn INPGNFN --output OUTPUT [--win-point WIN_POINT] [--draw-point DRAW_POINT] [--armageddon-file ARMAGEDDON_FILE]
                            [--win-point-arm WIN_POINT_ARM] [--loss-point-arm LOSS_POINT_ARM] [--show-max-score] [--table-color TABLE_COLOR]

    options:
      -h, --help            show this help message and exit
      --inpgnfn INPGNFN     Write the input pgn filename, required.
      --output OUTPUT       Write the output filename, required, can be .html, .csv or .txt. e.g --output tata_steel.html
      --win-point WIN_POINT
                            The point when the player wins, default=1.0
      --draw-point DRAW_POINT
                            The point when the player draws, default=0.5
      --armageddon-file ARMAGEDDON_FILE
                            The armageddon pgn file, not required, default=None, if the tournament is governed by armageddon tie-break system, you need to intput the
                            armageddon pgn file.
      --win-point-arm WIN_POINT_ARM
                            The point when one player wins the armageddon match, not required, default=1.0
      --loss-point-arm LOSS_POINT_ARM
                            The point when one player loses the armageddon match, not required, default=0.0
      --show-max-score      A flag to show MaxScore column in the table, can be useful when scoring is not standard.
      --table-color TABLE_COLOR
                            Write table color not required. [default="blue_light" value=("yellow_light", "grey_light", "orange_light", "green_light", "red_light",
                            "yellow_dark", "grey_dark", "blue_dark", "orange_dark", "green_dark", "red_dark")]

