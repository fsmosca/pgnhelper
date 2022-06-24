"""Manages job requests from user through the command line.
"""


from typing import Optional

import pgnhelper.eco
import pgnhelper.sort
import pgnhelper.roundrobin


class PgnHelper:
    """Manages user options to execute the job.

    Attributes:
      job: The kind of job to be done, sort, addeco and roundrobin.
      inpgnfn: The input pgn file or path and filename.
      outpgnfn: The output pgn file or path and filename.
      inecopgnfn: The eco.pgn that will be used in addeco job.
      sort_tag: Used in sorting games. 
      sort_direction: The output sorting ordering, lowtohigh or hightolow.       
    """

    def __init__(self, job: str, inpgnfn: Optional[str]=None,
            outpgnfn: Optional[str]=None, inecopgnfn: Optional[str]=None,
            sort_tag: str='eco', sort_direction: str='lowtohigh',
            output: Optional[str]=None, winpoint: float=1.0,
            drawpoint: float=0.5, tablecolor: str='blue_light',
            encoding: str='utf-8', armageddonfile: Optional[str]=None,
            winpointarm: float=1.0, losspointarm: float=0.0,
            showmaxscore: bool=False):
        self.job = job
        self.inpgnfn = inpgnfn
        self.inecopgnfn = inecopgnfn
        self.outpgnfn = outpgnfn
        self.sort_tag = sort_tag
        self.sort_direction = sort_direction
        self.output = output
        self.winpoint = winpoint
        self.drawpoint = drawpoint
        self.tablecolor = tablecolor
        self.encoding = encoding
        self.armageddonfile = armageddonfile
        self.winpointarm = winpointarm
        self.losspointarm = losspointarm
        self.showmaxscore = showmaxscore

    def start(self):
        """Run the type of job to be done.

        It will sort the games, add eco, opening and variation names to
        the games or generate a round-robin result table.
        """
        if self.job == 'sort':
            pgnhelper.sort.sort_games(self.inpgnfn, self.outpgnfn,
                    self.sort_tag, self.sort_direction)
        elif self.job == 'addeco':
            pgnhelper.eco.add_eco(self.inpgnfn, self.outpgnfn,
                    self.inecopgnfn, ply=4, maxply=24)
        elif self.job == 'roundrobin':
            rr = pgnhelper.roundrobin.RoundRobin(self.inpgnfn,
                self.armageddonfile, self.winpoint, self.drawpoint,
                self.winpointarm, self.losspointarm, self.showmaxscore)
            df = rr.table()
            rr.save_table(df, self.output, self.tablecolor)
        elif self.job == 'standing':
            rr = pgnhelper.roundrobin.RoundRobin(self.inpgnfn,
                self.armageddonfile, self.winpoint, self.drawpoint,
                self.winpointarm, self.losspointarm, self.showmaxscore)
            df = rr.standing()
            rr.save_table(df, self.output, self.tablecolor)
