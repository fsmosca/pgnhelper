.. _Installation Overview:

Installation
============

Virtual environment
^^^^^^^^^^^^^^^^^^^

I would recommend this kind of installation as opposed to ``global`` because
the clash of library versions installed are avoided. Also it is easy to cleanup
the installation, you just have to delete the virtual environment folder.

Typical setup on ``windows 10.``

1. Open command prompt or powershell::

    PS C:\Users\ferdi>

2. cd to C drive or other drive if you want to install in other drive::

    PS C:\Users\ferdi> cd c:\

3. Check if you have python::

    PS C:\> python --version

.. Note::
    Be sure you use Python ``version 3.7,  3.8 ...`` or later.

4. Create a folder in this example I will name it ``mypgnhelper``::

    PS C:\> mkdir mypgnhelper

5. cd to this folder::

    PS C:\> cd mypgnhelper

6. Create venv folder for virtual environment::

    PS C:\mypgnhelper> python -m venv venv

.. Note::
    The folder ``venv`` is now under the ``mypgnhelper`` folder. There is python
    installed under ``venv``. You may delete this folder if you no longer need it.

7. Activate the virtual enviromnent::

    PS C:\mypgnhelper> ./venv/scripts/activate

8. Update pip::

    (venv) PS C:\mypgnhelper> python -m pip install -U pip

9. Install the pgnhelper::

    (venv) PS C:\mypgnhelper> pip install pgnhelper

.. Note::
    All the depdendent modules of pgnhelper are also installed. See
    the dependent libraties section below.

10. Check the installation by checking its version::

    (venv) PS C:\mypgnhelper> pgnhelper -v

When you work with pgn file you need to activate the virtual environment
as in step 7 if it is not activated yet like when you comeback after computer restart.

If you no longer need the pgnhelper, just delete the ``mypgnhelper`` folder.


Global
^^^^^^

1. Open command prompt or powershell and run as administrator::

    PS C:\WINDOWS\system32>

2. cd to c drive::

    PS C:\WINDOWS\system32> cd c:\

3. Check if you have python::

    PS C:\> python --version

4. Install the package::

    PS C:\> pip install pgnhelper

5. Test it::

    PS C:\> pgnhelper -h


Dependent libraries
^^^^^^^^^^^^^^^^^^^

pgnhelper is dependent on the following libraries::

    python chess
    pandas
    pytest

They are installed automatically when pgnhelper is installed.
