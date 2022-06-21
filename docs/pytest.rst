Pytest
======

**Setup Guide**

Copy the tests and pgn folders from the `pgnhelper <https://github.com/fsmosca/pgnhelper>`_ github repository.
These folders have files that we can use to run pytest.

Example directory structure::

   c:/mypgnhelper
   c:/mypgnhelper/pgn/norway_chess_2022_classical.pgn
   c:/mypgnhelper/pgn/norway_chess_2022_armageddon.pgn
   c:/mypgnhelper/tests/test_roundrobin.py

You need to have Python version >= 3.7.

Command line::

   c:/pgnhelper> python -m pytest ./tests/test_roundrobin.py