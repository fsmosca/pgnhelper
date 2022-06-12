# pgnhelper
An application to process pgn file.

## Installation
```
pip install pgnhelper
```

## Features
Sort games by eco tag from script.
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

Sort games from command line.
```
python -m pgnhelper.pgnhelper sort --inpgnfn "c:/chess/mygames.pgn" --outpgnfn "out.pgn" --sort-tag eco --sort-direction hightolow
```

## Help

```
python -m pgnhelper.pgnhelper --help
```

```
python -m pgnhelper.pgnhelper sort --help
```
