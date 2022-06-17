import argparse
import pgnhelper


def main():
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(dest='command')
    sort = subparser.add_parser('sort',
        help='Sort the games from the given pgn file based on the given game tags. e.g. '
        'pgnhelper sort mygames.pgn --outpgnfn out.pgn --sort-tag opening --sort-direction hightolow')
    addeco = subparser.add_parser('addeco',
        help='Add eco and ecot codes, opening and variation names to the input pgn file. '
        'The eco, opening etc. are from the given input file eco.pgn. e.g. '
        'pgnhelper addeco --inpgnfn mygames.pgn --inecopgnfn eco.pgn --outpgnfn out.pgn')
    roundrobin = subparser.add_parser('roundrobin',
        help='Generate round-robin table results from the input pgn file. '
        'The output can be html, csv and txt. e.g. '
        'pgnhelper roundrobin --inpgnfn candidates.pgn --output candidates.html')

    sort.add_argument('--inpgnfn', type=str, required=True,
        help='Write the input pgn filename, required.')
    sort.add_argument('--outpgnfn', type=str, required=True,
        help='Write the output pgn filename, required, mode=overwrite.')
    sort.add_argument('--sort-tag', type=str, required=False, default='eco',
        help='Sort the games by tag. [default=eco, value=(eco | ecot | event | date | round | white | black | site | plycount)].'
        ' e.g. --sort-tag event')
    sort.add_argument('--sort-direction', type=str, required=False, default='lowtohigh',
        help='Write the direction to sort the games. [default=lowtohigh, value=(lowtohigh | hightolow)].')
    sort.add_argument('--encoding', type=str, required=False, default='utf-8',
        help='Encoding used in reading pgn file when sorting, not required. [default=utf-8, value=(utf-8 | ISO-8859-1)]. '
        'If you encounter an error like "UnicodeDecodeError: utf-8 codec cannot decode ..." you can try, '
        '--encoding ISO-8859-1')

    addeco.add_argument('--inpgnfn', type=str, required=True,
        help='Write the input pgn filename, required.')
    addeco.add_argument('--outpgnfn', type=str, required=True,
        help='Write the output pgn filename, required, mode=overwrite.')
    addeco.add_argument('--inecopgnfn', type=str, required=True,
        help='Write the reference eco.pgn filename, required.')

    roundrobin.add_argument('--inpgnfn', type=str, required=True,
        help='Write the input pgn filename, required.')
    roundrobin.add_argument('--output', type=str, required=True,
        help='Write the output filename, required, can be .html, .csv or .txt. e.g '
        '--output tata_steel.html')
    roundrobin.add_argument('--win-point', type=float,  required=False, default=1.0,
        help='The point when the players wins, default=1.0')
    roundrobin.add_argument('--draw-point', type=float, required=False, default=0.5,
        help='The point when the players draws, default=0.5')
    roundrobin.add_argument('--table-color', type=str, required=False, default='blue_light',
        help='Write table color not required. [default="blue_light" value=("yellow_light", '
        '"grey_light", "orange_light", "green_light", "red_light", "yellow_dark", '
        '"grey_dark", "blue_dark", "orange_dark", "green_dark", "red_dark")]')

    parser.add_argument('-v', '--version', action='version', version=f'{pgnhelper.__version__}')

    args = parser.parse_args()

    g = None
    if args.command == 'sort':
        g = pgnhelper.PgnHelper(
            args.command,
            inpgnfn=args.inpgnfn,
            outpgnfn=args.outpgnfn,
            sort_tag=args.sort_tag,
            sort_direction=args.sort_direction,
            encoding=args.encoding
        )
    elif args.command == 'addeco':
        g = pgnhelper.PgnHelper(
            args.command,
            inpgnfn=args.inpgnfn,
            outpgnfn=args.outpgnfn,
            inecopgnfn=args.inecopgnfn            
        )
    elif args.command == 'roundrobin':
        g = pgnhelper.PgnHelper(
            args.command,
            inpgnfn=args.inpgnfn,
            output=args.output,
            winpoint = args.win_point,
            drawpoint = args.draw_point,
            tablecolor = args.table_color
        )
    
    if g is not None:
        g.start()


if __name__ == '__main__':
    main()
