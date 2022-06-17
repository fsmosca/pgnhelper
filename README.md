# PgnHelper
An application that can sort games in pgn file, add eco codes, opening and variation names and generate round-robin result table based from the given tournament pgn file.

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
Python Package Index: https://pypi.org/project/pgnhelper/

A. Virtual environment installation (recommended)

1. Open command prompt or powershell.  
`PS C:\Users\ferdi>`  
2. cd to C drive or other drive if you want to install in other drive.  
`PS C:\Users\ferdi> cd c:\`  
3. Check if you have python.  
`PS C:\> python --version`  
4. Create a folder.  
`PS C:\> mkdir mypgnhelper`  
5. cd to this folder.  
`PS C:\> cd mypgnhelper`
6. Create venv folder for virtual environment.   
`PS C:\mypgnhelper> python -m venv venv`  
7. Activate the virtual enviromnent.  
`PS C:\mypgnhelper> ./venv/scripts/activate`  
8. Update pip.  
`(venv) PS C:\mypgnhelper> python -m pip install -U pip`  
9. Install the pgnhelper.  
`(venv) PS C:\mypgnhelper> pip install pgnhelper`  
10. Check the installation by checking its version.  
`(venv) PS C:\mypgnhelper> pgnhelper -v`  
You should see 0.2.0 or other version number.  
11. When you work with pgn file you need to activate the virtual environment as in step 7 if it is not activated yet like when you comeback after computer restart.

B. Global installation  

1. Open command prompt or powershell and run as administrator  
`PS C:\Users\ferdi>`   
2. Check if you have python.  
`PS C:\> python --version`  
3. Install the package.  
`PS C:\> pip install pgnhelper`  
4. Test it.  
`PS C:\> pgnhelper -v`  
`PS C:\> pgnhelper -h`  

## Dependency
pgnhelper is dependent on the following packages.

* [chess==1.9.1](https://github.com/niklasf/python-chess)
* [pandas](https://pypi.org/project/pandas/)
* [pretty-html-table](https://pypi.org/project/pretty-html-table/)

These are automatically installed when pgnhelper is installed. 

## Uninstallation
`pip uninstall pgnhelper`  
`pip uninstall chess`  
`pip uninstall pandas`  
`pip uninstall pretty-html-table`

## eco.pgn
This file is needed when adding eco, opening and variation names to the games in pgn file. You can get this from eco folder in this repo or you can use other eco.pgn from other sources.

## Features
**1. Sort games by eco tag in descending order from script**
```
"""
sample.py

pip install pgnhelper
"""

import pgnhelper

a = pgnhelper.PgnHelper(
    'sort',
    inpgnfn='mygames.pgn',
    outpgnfn='out.pgn',
    sort_tag='eco',
    sort_direction='hightolow')
a.start()
```

**2. Sort games by date tag in ascending order from script**
```
"""
sample.py
"""

import pgnhelper

a = pgnhelper.PgnHelper(
    'sort',
    inpgnfn='mygames.pgn',
    outpgnfn='out.pgn',
    sort_tag='date',
    sort_direction='lowtohigh')
a.start()
```

**3. Sort games from command line**
```
pgnhelper sort --inpgnfn "c:/chess/mygames.pgn" --outpgnfn "out.pgn" --sort-tag eco --sort-direction hightolow
```

**4. Add eco, opening and variation to games from script**  
```
"""
sample_addeco.py
"""

import pgnhelper

a = pgnhelper.PgnHelper(
    'addeco',
    inpgnfn='mygames.pgn',
    outpgnfn='out.pgn',
    inecopgnfn='eco.pgn')
a.start()
```

**5. Add ECO, ECOT, Opening, OpeningT, Variation and VariationT to the game from command line**  
```
pgnhelper addeco --inpgnfn mygames.pgn --inecopgnfn eco.pgn --outpgnfn eco_mygames.pgn
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

**6. Generate round-robin table from command line**  

Tie-break points supported:  
DE = Direct encounter  
Wins = Number of wins  
SB = [Sonneborn-Berger](https://en.wikipedia.org/wiki/Sonneborn%E2%80%93Berger_score)

Reference:  
https://handbook.fide.com/files/handbook/C02Standards.pdf  

13.16.2. Individual Round-Robin Tournaments:  
* Direct encounter  
* The greater number of wins, including forfeits  
* Sonneborn-Berger  
* Koya System  


```
pgnhelper roundrobin --inpgnfn "./pgn/airthings_masters_prelim_2022.pgn" --output airthings.html --win-point 3.0 --draw-point 1.0 --table-color green_light
```

![image](https://user-images.githubusercontent.com/22366935/174115420-8e72e449-7a32-4f21-80f8-7ad09614fc24.png)

```
pgnhelper roundrobin --inpgnfn "./pgn/candidates_zurich_1953.pgn" --output zurich1953.txt --win-point 1.0 --draw-point 0.5
```
```
 Rank          Name    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15  Games  Score  Score%  DE  Wins    SB
    1     Smyslov V    x  1.0  2.0  1.5  1.0  2.0  1.0  0.5  1.0  1.0  1.0  1.0  1.5  2.0  1.5     28   18.0    64.3 0.0     0   0.0
    2   Bronstein D  1.0    x  1.5  2.0  1.0  0.5  1.0  1.0  1.5  1.0  1.0  1.0  1.5  1.0  1.0     28   16.0    57.1 3.5     6 119.0
    3       Keres P  0.0  0.5    x  1.0  1.5  1.5  1.0  1.0  1.0  0.5  2.0  1.5  1.5  1.0  2.0     28   16.0    57.1 1.5     8 111.5
    4   Reshevsky S  0.5  0.0  1.0    x  1.0  1.0  1.0  1.0  1.0  1.5  1.5  1.5  1.5  2.0  1.5     28   16.0    57.1 1.0     8 116.0
    5   Petrosian T  1.0  1.0  0.5  1.0    x  1.0  0.5  1.0  0.0  1.0  1.0  2.0  1.5  1.5  2.0     28   15.0    53.6 0.0     0   0.0
    6      Geller E  0.0  1.5  0.5  1.0  1.0    x  2.0  0.5  1.0  1.0  1.0  1.5  1.5  1.0  1.0     28   14.5    51.8 2.0     8 101.8
    7     Najdorf M  1.0  1.0  1.0  1.0  1.5  0.0    x  1.5  1.5  0.5  1.0  1.0  1.0  0.5  2.0     28   14.5    51.8 0.0     5 103.5
    8       Kotov A  1.5  1.0  1.0  1.0  1.0  1.5  0.5    x  1.0  1.5  0.0  1.0  1.5  0.5  1.0     28   14.0    50.0 1.0     8 107.5
    9    Taimanov M  1.0  0.5  1.0  1.0  2.0  1.0  0.5  1.0    x  1.0  1.0  1.0  0.5  0.5  2.0     28   14.0    50.0 1.0     7  82.2
   10    Averbakh Y  1.0  1.0  1.5  0.5  1.0  1.0  1.5  0.5  1.0    x  1.0  1.0  0.5  2.0  0.0     28   13.5    48.2 1.0     5  94.0
   11 Boleslavsky I  1.0  1.0  0.0  0.5  1.0  1.0  1.0  2.0  1.0  1.0    x  0.5  1.0  1.5  1.0     28   13.5    48.2 1.0     4  88.5
   12       Szabo L  1.0  1.0  0.5  0.5  0.0  0.5  1.0  1.0  1.0  1.0  1.5    x  1.5  1.0  1.5     28   13.0    46.4 0.0     0   0.0
   13    Gligoric S  0.5  0.5  0.5  0.5  0.5  0.5  1.0  0.5  1.5  1.5  1.0  0.5    x  1.5  2.0     28   12.5    44.6 0.0     0   0.0
   14        Euwe M  0.0  1.0  1.0  0.0  0.5  1.0  1.5  1.5  1.5  0.0  0.5  1.0  0.5    x  1.5     28   11.5    41.1 0.0     0   0.0
   15   Stahlberg A  0.5  1.0  0.0  0.5  0.0  1.0  0.0  1.0  0.0  2.0  1.0  0.5  0.0  0.5    x     28    8.0    28.6 0.0     0   0.0
```



## Help

`pgnhelper --help`

```
usage: pgnhelper [-h] [-v] {sort,addeco,roundrobin} ...

positional arguments:
  {sort,addeco,roundrobin}
    sort                Sort the games from the given pgn file based on the given game tags. e.g. pgnhelper sort mygames.pgn --outpgnfn out.pgn --sort-tag opening --sort-direction hightolow
    addeco              Add eco and ecot codes, opening and variation names to the input pgn file. The eco, opening etc. are from the given input file eco.pgn. e.g. pgnhelper addeco --inpgnfn       
                        mygames.pgn --inecopgnfn eco.pgn --outpgnfn out.pgn
    roundrobin          Generate round-robin table results from the input pgn file. The output can be html, csv and txt. e.g. pgnhelper roundrobin --inpgnfn candidates.pgn --output candidates.html  

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```

`pgnhelper sort --help`
```
usage: pgnhelper sort [-h] --inpgnfn INPGNFN --outpgnfn OUTPGNFN [--sort-tag SORT_TAG]
                      [--sort-direction SORT_DIRECTION] [--encoding ENCODING]

optional arguments:
  -h, --help            show this help message and exit
  --inpgnfn INPGNFN     Write the input pgn filename, required.
  --outpgnfn OUTPGNFN   Write the output pgn filename, required, mode=overwrite.
  --sort-tag SORT_TAG   Sort the games by tag. [default=eco, value=(eco | ecot | event | date | round | white | black
                        | site | plycount)]. e.g. --sort-tag event
  --sort-direction SORT_DIRECTION
                        Write the direction to sort the games. [default=lowtohigh, value=(lowtohigh | hightolow)].
  --encoding ENCODING   Encoding used in reading pgn file when sorting, not required. [default=utf-8, value=(utf-8 |
                        ISO-8859-1)]. If you encounter an error like "UnicodeDecodeError: utf-8 codec cannot decode
                        ..." you can try, --encoding ISO-8859-1
```

`pgnhelper addeco -h`
```
usage: pgnhelper addeco [-h] --inpgnfn INPGNFN --outpgnfn OUTPGNFN --inecopgnfn INECOPGNFN

options:
  -h, --help            show this help message and exit
  --inpgnfn INPGNFN     Write the input pgn filename, required.
  --outpgnfn OUTPGNFN   Write the output pgn filename, required, mode=overwrite.
  --inecopgnfn INECOPGNFN
                        Write the reference eco.pgn filename, required.
```

`pgnhelper roundrobin -h`
```
usage: pgnhelper roundrobin [-h] --inpgnfn INPGNFN --output OUTPUT [--win-point WIN_POINT] [--draw-point DRAW_POINT] [--table-color TABLE_COLOR]

options:
  -h, --help            show this help message and exit
  --inpgnfn INPGNFN     Write the input pgn filename, required.
  --output OUTPUT       Write the output filename, required, can be .html, .csv or .txt. e.g --output tata_steel.html
  --win-point WIN_POINT
                        The point when the players wins, default=1.0
  --draw-point DRAW_POINT
                        The point when the players draws, default=0.5
  --table-color TABLE_COLOR
                        Write table color not required. [default="blue_light" value=("yellow_light", "grey_light", "orange_light", "green_light", "red_light", "yellow_dark", "grey_dark",
                        "blue_dark", "orange_dark", "green_dark", "red_dark")]
```

## Credits
* Python chess  
  site: https://python-chess.readthedocs.io/en/latest/  
  usage:
    * adding eco
    * round-robin result table generation  
* pgn-extract  
  site: https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/  
  usage:
    * The eco.pgn in eco folder is based from the eco.pgn from pgn-extract.
    * cleaning pgn files  
* weekinchess  
  site: https://theweekinchess.com/  
  usage:
    * game collections  
* pgn mentor  
  site: https://www.pgnmentor.com/files.html  
  usage:
    * game collections  
* pretty-html-table  
  site: https://pypi.org/project/pretty-html-table/  
  usage:
    * pretty html round-robin result table generation
* mark weeks  
  site: https://www.mark-weeks.com/chess/wcc-indx.htm  
  usage:  
    * game collections  
* pandas  
  site: https://pandas.pydata.org/  
  usage:
    * round-robin result table generation

## Change log
version 0.4.0

```
* Add encoding option when sorting games.   

  By default when reading pgn file to be sorted, it uses encoding utf-8. If you encounter an error like
  "UnicodeDecodeError" for example, you can try to use another encoding like the example below.
  
  pgnhelper sort ... --encoding ISO-8859-1
```
