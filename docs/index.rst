.. PgnHelper documentation master file, created by
   sphinx-quickstart on Tue Jun 21 09:36:00 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation of PgnHelper
==========================

PgnHelper is an application that can ``sort games;`` ``add ECO codes, opening and variation
names;`` and generate a ``round-robin result table`` with rating change and tie-break
scores.

See the ``CONTENTS`` in the sidebar for other informations.

Features
^^^^^^^^

**Add ECO codes, Opening and Variation names**

Sample output::

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

The new ECOT, OpeningT and VariationT (T=Transposition) are based from the
input eco.pgn file. See the ``Usage`` section in the sidebar on how to add
it to the game.

The ``ECO`` tag is based from the first 2 moves of the game while the ``ECOT`` is
based from the first 12 moves of the game.


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:
   
   installation
   uninstallation
   usage   
   pytest
   changelog
   readthedocs
   api
