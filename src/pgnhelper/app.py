"""
app.py

   The driver module to process requested jobs such as sort games, add eco
   and generate round-robin result table from tournament.
"""


import pgnhelper.addeco
import pgnhelper.sortgames
import pgnhelper.roundrobin


class PgnHelper:
    def __init__(self, job, inpgnfn=None, outpgnfn=None, inecopgnfn=None,
                sort_tag='eco', sort_direction='lowtohigh',
                output=None, winpoint=1.0, drawpoint=0.5, tablecolor='blue_light',
                encoding='utf-8', armageddonfile=None, winpointarm=1.0,
                losspointarm=0.0, showmaxscore=False):
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
        self.games = []
        self.eco_db = {}

    def start(self):
        if self.job == 'sort':
            pgnhelper.sortgames.sort_games(self.inpgnfn, self.outpgnfn, self.sort_tag, self.sort_direction)
        elif self.job == 'addeco':
            pgnhelper.addeco.add_eco(self.inpgnfn, self.outpgnfn, self.inecopgnfn, ply=4, maxply=24)
        elif self.job == 'roundrobin':
            df = pgnhelper.roundrobin.round_robin(
                self.inpgnfn,
                winpoint=self.winpoint,
                drawpoint=self.drawpoint,
                armageddonfile=self.armageddonfile,
                winpointarm=self.winpointarm,
                losspointarm=self.losspointarm,
                showmaxscore=self.showmaxscore)
            pgnhelper.roundrobin.save_roundrobin_table(df, self.output, self.tablecolor)
