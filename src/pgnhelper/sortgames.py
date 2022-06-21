"""Sort games by game tags.
"""


from operator import attrgetter


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


def read_games(inpgnfn, encoding='utf-8'):
    games, current = [], None
    with open(inpgnfn, 'r', encoding=encoding) as f:
        for line in f:
            if line.startswith('[Event '):
                if current:
                    games.append(current)
                current = Game()
            current.add_line(line)
        if current:
            games.append(current)
    return games


def save_games(games, outpgnfn):
    with open(outpgnfn, 'w', encoding='utf-8') as f:
        for game in games:
            for line in game.lines:
                f.write(line)


def sort_games(inpgnfn, outpgnfn, sort_tag, sort_direction):
    games = read_games(inpgnfn, encoding='utf-8')
    sort_value = False if sort_direction == 'lowtohigh' else True
    sort_tag = sort_tag.lower()
    if sort_tag == 'ecot':
        s = sorted(games, key=attrgetter('eco'), reverse=sort_value)
        games = sorted(s, key=attrgetter(sort_tag), reverse=sort_value)
    elif sort_tag == 'eco':
        s = sorted(games, key=attrgetter('ecot'), reverse=sort_value)
        games = sorted(s, key=attrgetter(sort_tag), reverse=sort_value)
    else:
        games = sorted(games, key=attrgetter(sort_tag), reverse=sort_value)
    save_games(games, outpgnfn)
