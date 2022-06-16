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

    parser.add_argument('-v', '--version', action='version', version=f'{pgnhelper.__version__}')

    args = parser.parse_args()

    g = None
    if args.command == 'sort':
        g = pgnhelper.PgnHelper(
            args.command,
            inpgnfn=args.inpgnfn,
            outpgnfn=args.outpgnfn,
            sort_tag=args.sort_tag,
            sort_direction=args.sort_direction
        )
    elif args.command == 'addeco':
        g = pgnhelper.PgnHelper(
            args.command,
            inpgnfn=args.inpgnfn,
            outpgnfn=args.outpgnfn,
            inecopgnfn=args.inecopgnfn            
        )
    
    if g is not None:
        g.start()


if __name__ == '__main__':
    main()
