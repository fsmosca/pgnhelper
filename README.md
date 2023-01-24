# PgnHelper
An application that can sort games in pgn file; add eco codes, opening and variation names; generates round-robin, swiss and standing tables based from the given pgn file. It supports calculation of rating change and tie-break systems (Direct encounter, Number of wins, Sonneborn-Berger and Koya system) for round-robin and Buchholz cut 1, Buchholz, Sonneborn-Berger, and Direct Encounter for swiss. See the documentation for more informations.

#### 85th Tata Steel Masters, 2023

```python
pgnhelper roundrobin --inpgnfn tatamast23.pgn --output tatamast23_my.html
```

![image](https://user-images.githubusercontent.com/22366935/214319855-f8b65c02-83a5-4cd6-93ea-e71b68afd325.png)


## Installation

```
pip install pgnhelper -U
```

## Documentation

[Read the Docs documentation of pgnhelper](https://pgnhelper.readthedocs.io/en/latest/index.html) contains installation guide, features and others.

## Links

* [Pypi pgnhelper](https://pypi.org/project/pgnhelper/)
* [Readthedocs pgnhelper](https://pgnhelper.readthedocs.io/en/latest/index.html)

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
