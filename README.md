# PgnHelper
An application that can sort games in pgn file and add eco codes, opening and variation names.

It can sort on event, site, date, round, white, black eco, ecot and plycount tags.

There are 2 types of ECO codes that it adds first the ECO based from the first 4 plies and second the ECOT or ECO by transposition after 24 plies. The same can be said for the opening and variation, there are OpeningT and VariationT.

```
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
```

The new ECOT, OpeningT and VariationT are based from the input eco.pgn file. You can get [eco.pgn](https://github.com/fsmosca/eco) which is based from the eco.pgn from [pgn-extract.](https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/)

## Installation
```
pip install pgnhelper
```


## Features
1. Sort games by eco tag in descending order from script.
```
"""
sample.py

pip install pgnhelper
"""

from pgnhelper import pgnhelper

a = pgnhelper.PgnHelper(
    'sort',
    inpgnfn='mygames.pgn',
    outpgnfn='out.pgn',
    sort_tag='eco',
    sort_direction='hightolow')
a.start()
```

2. Sort games by date tag in ascending order from script.
```
"""
sample.py
"""

from pgnhelper import pgnhelper

a = pgnhelper.PgnHelper(
    'sort',
    inpgnfn='mygames.pgn',
    outpgnfn='out.pgn',
    sort_tag='date',
    sort_direction='lowtohigh')
a.start()
```

3. Sort games from command line.
```
python -m pgnhelper.pgnhelper sort --inpgnfn "c:/chess/mygames.pgn"  
    --outpgnfn "out.pgn" --sort-tag eco --sort-direction hightolow
```

4. Add eco, opening and variation to games from script.
```
"""
sample_addeco.py
"""

from pgnhelper import pgnhelper

a = pgnhelper.PgnHelper(
    'addeco',
    inpgnfn='mygames.pgn',
    outpgnfn='out.pgn',
    inecopgnfn='eco.pgn')
a.start()
```

5. Add ECO, ECOT, Opening, OpeningT, Variation and VariationT to the game from command line.
```
python -m pgnhelper.pgnhelper addeco --inpgnfn mygames.pgn 
    --inecopgnfn eco.pgn --outpgnfn eco_mygames.pgn
```

Example output where the game started as English and has transposed into QGD. 
```
[Event "FEOBOS, Rank 00003"]
[Site "Trier"]
[Date "2017.01.29"]
[Round "20"]
[White "FEOBOS"]
[Black "FEOBOS"]
[Result "1/2-1/2"]
[BlackElo "3000"]
[ECO "A17"]
[ECOT "D41"]
[Opening "English"]
[OpeningT "QGD"]
[PlyCount "20"]
[Source "Frank Quisinsky"]
[VariationT "Semi-Tarrasch with e3"]
[WhiteElo "3000"]

1. c4 Nf6 2. Nc3 e6 3. Nf3 d5 4. d4 c5 5. cxd5 Nxd5 6. e3 Be7 7. Bc4 cxd4 8.
exd4 Nc6 9. O-O O-O 10. Re1 Qd6 1/2-1/2
```


## Help

`python -m pgnhelper.pgnhelper --help`

```
usage: pgnhelper.py [-h] [-v] {sort,addeco} ...

positional arguments:
  {sort,addeco}
    sort         Sort the games from the given pgn file based on the given game tags. e.g. python pgnhelper.py sort
                 mygames.pgn --outpgnfn out.pgn --sort-tag opening --sort-direction hightolow
    addeco       Add eco and ecot codes, opening and variation names to the input pgn file. The eco, opening etc. are
                 from the given input file eco.pgn. e.g. python pgnhelper.py addeco --inpgnfn mygames.pgn --inecopgnfn
                 eco.pgn --outpgnfn out.pgn

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

`python -m pgnhelper.pgnhelper sort --help`
```
usage: pgnhelper.py sort [-h] --inpgnfn INPGNFN --outpgnfn OUTPGNFN [--sort-tag SORT_TAG]
                         [--sort-direction SORT_DIRECTION]

optional arguments:
  -h, --help            show this help message and exit
  --inpgnfn INPGNFN     Write the input pgn filename, required.
  --outpgnfn OUTPGNFN   Write the output pgn filename, required, mode=overwrite.
  --sort-tag SORT_TAG   Sort the games by tag. [default=eco, value=(eco | ecot | event | date | round | white | black
                        | site | plycount)]. e.g. --sort-tag event
  --sort-direction SORT_DIRECTION
                        Write the direction to sort the games. [default=lowtohigh, value=(lowtohigh | hightolow)].
```

`python -m pgnhelper.pgnhelper addeco --help`
```
usage: pgnhelper.py addeco [-h] --inpgnfn INPGNFN --outpgnfn OUTPGNFN --inecopgnfn INECOPGNFN

optional arguments:
  -h, --help            show this help message and exit
  --inpgnfn INPGNFN     Write the input pgn filename, required.
  --outpgnfn OUTPGNFN   Write the output pgn filename, required, mode=overwrite.
  --inecopgnfn INECOPGNFN
                        Write the reference eco.pgn filename, required.
```
