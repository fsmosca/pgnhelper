"""Manages job requests from suer through the command line.
"""


from typing import Optional

import pgnhelper.addeco
import pgnhelper.sortgames
import pgnhelper.roundrobin


class PgnHelper:
    """Manages user options to execute the job.

    Attributes:
      job: Kind of job to be done.
      inpgnfn: The input pgn file or path and filename.
      outpgnfn: The output pgn file or path and filename.
      inecopgnfn: The eco.pgn that will be used in addeco job.
      sort_tag: Used in sorting games.        
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
            pgnhelper.sortgames.sort_games(self.inpgnfn, self.outpgnfn,
                    self.sort_tag, self.sort_direction)
        elif self.job == 'addeco':
            pgnhelper.addeco.add_eco(self.inpgnfn, self.outpgnfn,
                    self.inecopgnfn, ply=4, maxply=24)
        elif self.job == 'roundrobin':
            df = pgnhelper.roundrobin.round_robin(
                self.inpgnfn,
                winpoint=self.winpoint,
                drawpoint=self.drawpoint,
                armageddonfile=self.armageddonfile,
                winpointarm=self.winpointarm,
                losspointarm=self.losspointarm,
                showmaxscore=self.showmaxscore)
            pgnhelper.roundrobin.save_roundrobin_table(df,
                    self.output, self.tablecolor)
