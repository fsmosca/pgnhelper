"""
pgnhelper.py
"""


import argparse
from operator import attrgetter

import chess.pgn


__version__ = '0.1.0'


class Game:
    def __init__(self):
        self.lines = []
        self.event = ''
        self.site = ''
        self.date = ''
        self.round = ''
        self.white = ''
        self.black = ''
        self.eco = ''
        self.ecot = ''
        self.plycount = ''

    def add_line(self, line):
        self.lines.append(line)
        if line.startswith('[ECO '):
            self.eco = line
        elif line.startswith('[ECOT '):
            self.ecot = line
        elif line.startswith('[Event '):
            self.event = line
        elif line.startswith('[Site '):
            self.site = line
        elif line.startswith('[Date '):
            self.date = line
        elif line.startswith('[Round '):
            self.round = line
        elif line.startswith('[White '):
            self.white = line
        elif line.startswith('[Black '):
            self.black = line
        elif line.startswith('[PlyCount '):
            self.plycount = line


class PgnHelper:
    def __init__(self, job, inpgnfn=None, outpgnfn=None, inecopgnfn=None,
            sort_tag='eco', sort_direction='lowtohigh'):
        self.job = job
        self.inpgnfn = inpgnfn
        self.inecopgnfn = inecopgnfn
        self.outpgnfn = outpgnfn
        self.sort_tag = sort_tag
        self.sort_direction = sort_direction
        self.games = []
        self.eco_db = {}

    def create_eco_db(self):
        with open(self.inecopgnfn, 'r') as f:
            while True:
                game = chess.pgn.read_game(f)
                if game is None:
                    break
                try:
                    eco = game.headers['ECO']
                except KeyError:
                    continue
                try:
                    opening = game.headers['Opening']
                except KeyError:
                    continue
                try:
                    variation = game.headers['Variation']
                except KeyError:
                    variation = None
                node = game
                node_end = node.end()
                end_board = node_end.board()
                epd = end_board.epd()
                self.eco_db.update({epd: {'eco': eco, 'opening': opening, 'variation': variation}})

    def add_eco(self, ply=4, maxply=24):
        with open(self.outpgnfn, 'w') as w:
            with open(self.inpgnfn, 'r') as f:
                while True:
                    game = chess.pgn.read_game(f)
                    if game is None:
                        break

                    first_eco, eco_t = None, None
                    first_opening, opening_t = None, None
                    first_variation, variation_t = None, None
                    is_first_eco = False
                    first_eco_ply = 1

                    for node in game.mainline():
                        board = node.board()
                        gply = board.ply()
                        epd = board.epd()

                        if gply >= ply:
                            if epd in self.eco_db:
                                if not is_first_eco:
                                    is_first_eco = True
                                    first_eco = self.eco_db[epd]['eco']
                                    first_opening = self.eco_db[epd]['opening']
                                    first_variation = self.eco_db[epd]['variation']
                                    first_eco_ply = board.ply()
                                else:
                                    eco_t = self.eco_db[epd]['eco']
                                    opening_t = self.eco_db[epd]['opening']
                                    variation_t = self.eco_db[epd]['variation']

                                if gply >= maxply:
                                    break

                            # For first eco, if pos is not in db we will takeback 1 ply until we find it or hit ply 1.
                            elif not is_first_eco:
                                new_board = board.copy()
                                while True:
                                    new_board.pop()
                                    new_epd = new_board.epd()
                                    if new_epd in self.eco_db:
                                        is_first_eco = True
                                        first_eco = self.eco_db[new_epd]['eco']
                                        first_opening = self.eco_db[new_epd]['opening']
                                        first_variation = self.eco_db[new_epd]['variation']
                                        first_eco_ply = new_board.ply()
                                        break
                                    if new_board.ply() <= 1:
                                        break
                                    if new_board.ply() <= first_eco_ply:
                                        break
                    mygame = game
                    if first_eco is not None:
                        mygame.headers['ECO'] = first_eco
                        mygame.headers['Opening'] = first_opening
                        if first_variation is not None:
                            mygame.headers['Variation'] = first_variation
                    if eco_t is not None:
                        mygame.headers['ECOT'] = eco_t
                        mygame.headers['OpeningT'] = opening_t
                        if variation_t is not None:
                            mygame.headers['VariationT'] = variation_t
                    w.write(f'{mygame}\n\n')

    def read_games(self):
        current = None
        with open(self.inpgnfn, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('[Event '):
                    if current:
                        self.games.append(current)
                    current = Game()
                current.add_line(line)
            if current:
                self.games.append(current)

    def sort_games(self):
        sort_value = False if self.sort_direction == 'lowtohigh' else True
        sort_tag = self.sort_tag.lower()
        if sort_tag == 'ecot':
            s = sorted(self.games, key=attrgetter('eco'), reverse=sort_value)
            self.games = sorted(s, key=attrgetter(sort_tag), reverse=sort_value)
        elif sort_tag == 'eco':
            s = sorted(self.games, key=attrgetter('ecot'), reverse=sort_value)
            self.games = sorted(s, key=attrgetter(sort_tag), reverse=sort_value)
        else:
            self.games = sorted(self.games, key=attrgetter(sort_tag), reverse=sort_value)

    def save_games(self):
        with open(self.outpgnfn, 'w', encoding='utf-8') as f:
            for game in self.games:
                for line in game.lines:
                    f.write(line)

    def start(self):
        if self.job == 'sort':
            self.read_games()
            self.sort_games()
            self.save_games()
        elif self.job == 'addeco':
            self.create_eco_db()
            self.add_eco(ply=4, maxply=24)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(dest='command')
    sort = subparser.add_parser('sort',
        help='Sort the games from the given pgn file based on the given game tags. e.g. '
        'python pgnhelper.py sort mygames.pgn --outpgnfn out.pgn --sort-tag opening --sort-direction hightolow')
    addeco = subparser.add_parser('addeco',
        help='Add eco and ecot codes, opening and variation names to the input pgn file. '
        'The eco, opening etc. are from the given input file eco.pgn. e.g. '
        'python pgnhelper.py addeco --inpgnfn mygames.pgn --inecopgnfn eco.pgn --outpgnfn out.pgn')

    sort.add_argument('--inpgnfn', type=str, required=True,
        help='Write the input pgn filename, required.')
    sort.add_argument('--outpgnfn', type=str, required=True,
        help='Write the output pgn filename, required, mode=overwrite.')
    sort.add_argument('--sort-tag', type=str, required=False, default='eco',
        help='Sort the games by tag. [default=eco, value=(eco | ecot | event | date | round | white | black | site | plycount)].'
        ' e.g. --sort-tag event')
    sort.add_argument('--sort-direction', type=str, required=False, default='lowtohigh',
        help='Write the direction to sort the games. [default=lowtohigh, value=(lowtohigh | hightolow)].')

    addeco.add_argument('--inpgnfn', type=str, required=True,
        help='Write the input pgn filename, required.')
    addeco.add_argument('--outpgnfn', type=str, required=True,
        help='Write the output pgn filename, required, mode=overwrite.')
    addeco.add_argument('--inecopgnfn', type=str, required=True,
        help='Write the reference eco.pgn filename, required.')

    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')

    args = parser.parse_args()

    g = None
    if args.command == 'sort':
        g = PgnHelper(
            args.command,
            inpgnfn=args.inpgnfn,
            outpgnfn=args.outpgnfn,
            sort_tag=args.sort_tag,
            sort_direction=args.sort_direction
        )
    elif args.command == 'addeco':
        g = PgnHelper(
            args.command,
            inpgnfn=args.inpgnfn,
            outpgnfn=args.outpgnfn,
            inecopgnfn=args.inecopgnfn            
        )
    
    if g is not None:
        g.start()
