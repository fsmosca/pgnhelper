Pytest
======

**Setup Guide**

Copy the tests folders from the `pgnhelper <https://github.com/fsmosca/pgnhelper>`_ github repository.
These folders have files that we can use to run pytest.

Typical directory structure::

   c:/mypgnhelper
   c:/mypgnhelper/tests/test_roundrobin.py

You need to have Python version >= 3.7.

Command line::

   c:/pgnhelper> python -m pytest ./tests/test_roundrobin.py
   c:/pgnhelper> python -m pytest ./tests/test_addeco.py
   c:/pgnhelper> python -m pytest ./tests/test_sortgames.py
