# pgnhelper
An application to process pgn file.

### Features

##### Sort games by eco tag

a) Script

```
"""
sample.py

pip install pgnhelper
"""

from pgnhelper import pgnhelper

a = pgnhelper.PgnHelper('sort', inpgnfn='mygames.pgn', outpgnfn='out.pgn',
                sort_tag='eco', sort_direction='hightolow')
a.start()
```

b) Command line

```
python -m pgnhelper.pgnhelper sort --inpgnfn "c:/chess/mygames.pgn" --outpgnfn "out.pgn" --sort-tag eco --sort-direction hightolow
```

### Access help

```
python -m pgnhelper.pgnhelper --help
```

```
python -m pgnhelper.pgnhelper sort --help

usage: pgnhelper.py sort [-h] --inpgnfn INPGNFN --outpgnfn OUTPGNFN [--sort-tag SORT_TAG]
                         [--sort-direction SORT_DIRECTION]

optional arguments:
  -h, --help            show this help message and exit
  --inpgnfn INPGNFN     Write the input pgn filename, required.
  --outpgnfn OUTPGNFN   Write the output pgn filename, required, mode=overwrite.
  --sort-tag SORT_TAG   Sort the games by tag. [default=eco, value=(eco | ecot | event | date | round | white |
                        black)]. e.g. --sort-tag event
  --sort-direction SORT_DIRECTION
                        Write the direction to sort the games. [default=lowtohigh, value=(lowtohigh | hightolow)].
```
