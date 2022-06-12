# pgnhelper
An application to process pgn file.

## Installation
```
pip install pgnhelper
```


## Features
1. Sort games by eco tag from script.
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

2. Sort games from command line.
```
python -m pgnhelper.pgnhelper sort --inpgnfn "c:/chess/mygames.pgn" --outpgnfn "out.pgn" --sort-tag eco --sort-direction hightolow
```

3. Add ECO, ECOT, Opening, OpeningT, Variation and VariationT to the game. The T in ECOT, OpeningT and VariationT refers to Transposition. ECO code will be based on the first 4 plies of the game while ECOT will be the ECO after 4 plies of the game with a maximum of 24 plies.

```
python -m pgnhelper.pgnhelper addeco --inpgnfn mygames.pgn --inecopgnfn eco.pgn --outpgnfn eco_mygames.pgn
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

1. c4 Nf6 2. Nc3 e6 3. Nf3 d5 4. d4 c5 5. cxd5 Nxd5 6. e3 Be7 7. Bc4 cxd4 8. exd4 Nc6 9. O-O O-O 10. Re1 Qd6 1/2-1/2
```


## Help

```
python -m pgnhelper.pgnhelper --help
```

```
python -m pgnhelper.pgnhelper sort --help
```
