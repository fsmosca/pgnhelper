# pgnhelper
An application to process pgn file.

### Features
1. Sort games by eco tag

a) Script

`sample.py`
```
"""
pip install pgnhelper
"""

from pgnhelper import pgnhelper

a = pgnhelper.PgnHelper('sort', inpgnfn='mygames.pgn', outpgnfn='out.pgn',
                sort_tag='eco', sort_direction='hightolow')
a.start()
```

b) Command line

`
python -m pgnhelper.pgnhelper sort --inpgnfn "mygames.pgn" --outpgnfn "out.pgn"
`

### Access help

```
python -m pgnhelper.pgnhelper --help
```

```
python -m pgnhelper.pgnhelper sort --help
```