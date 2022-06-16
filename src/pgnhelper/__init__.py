from pkg_resources import get_distribution
from pgnhelper.__main__ import main
from pgnhelper.pgnhelper import PgnHelper
from pgnhelper.roundrobin import round_robin

__version__ = get_distribution('pgnhelper').version