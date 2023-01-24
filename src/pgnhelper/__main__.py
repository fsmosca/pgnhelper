"""Manages command line processes.
"""


import argparse
import pgnhelper.app


def main():
    parser = argparse.ArgumentParser()

    # Common parsers
    input_pgn_parser = argparse.ArgumentParser(add_help=False)
    input_pgn_parser.add_argument(
        '--inpgnfn', type=str, required=True,
        help='Write the input pgn filename, required.')

    output_pgn_parser = argparse.ArgumentParser(add_help=False)
    output_pgn_parser.add_argument(
        '--outpgnfn', type=str, required=True,
        help='Write the output pgn filename, required, mode=overwrite.')

    output_parser = argparse.ArgumentParser(add_help=False)
    output_parser.add_argument(
        '--output', type=str, required=True,
        help='Write the output filename, required, can be .html, .csv or .txt, like out.txt')
  
    table_parser = argparse.ArgumentParser(add_help=False)
    table_parser.add_argument(
        '--win-point', type=float, required=False, default=1.0,
        help='The point when the player wins, default=1.0')
    table_parser.add_argument(
        '--draw-point', type=float, required=False, default=0.5,
        help='The point when the player draws, default=0.5')
    table_parser.add_argument(
        '--armageddon-file', type=str, required=False, default=None,
        help='The armageddon pgn file, not required, default=None, if the '
        'tournament is governed by armageddon tie-break system, you need to '
        'intput the armageddon pgn file.')
    table_parser.add_argument(
        '--win-point-arm', type=float, required=False, default=1.0,
        help='The point when one player wins the armageddon match, not required, default=1.0')
    table_parser.add_argument(
        '--loss-point-arm', type=float, required=False, default=0.0,
        help='The point when one player loses the armageddon match, not required, default=0.0')
    table_parser.add_argument(
        '--show-max-score', action='store_true',
        help='A flag to show MaxScore column in the table, can be useful when scoring is not standard.')

    # Sub parsers
    subparser = parser.add_subparsers(dest='command')

    sort = subparser.add_parser(
        'sort', parents=[input_pgn_parser, output_pgn_parser],
        help='Sort the games from the given pgn file based on the given game tags. e.g. '
        'pgnhelper sort mygames.pgn --outpgnfn out.pgn --sort-tag opening --sort-direction hightolow')
    addeco = subparser.add_parser(
        'addeco', parents=[input_pgn_parser, output_pgn_parser],
        help='Add eco and ecot codes, opening and variation names to the input pgn file. '
        'The eco, opening etc. are from the given input file eco.pgn. e.g. '
        'pgnhelper addeco --inpgnfn mygames.pgn --inecopgnfn eco.pgn --outpgnfn out.pgn')

    roundrobin = subparser.add_parser(
        'roundrobin', parents=[input_pgn_parser, output_parser, table_parser],
        help='Generate round-robin table results from the input pgn file. '
        'The output can be html, csv and txt. e.g. '
        'pgnhelper roundrobin --inpgnfn candidates.pgn --output candidates.html')

    standing = subparser.add_parser(
        'standing', parents=[input_pgn_parser, output_parser, table_parser],
        help='Generates a standings from the input pgn file. '
        'The output can be html, csv and txt. e.g. '
        'pgnhelper standing --inpgnfn candidates.pgn --output candidates.html')

    opening_stats = subparser.add_parser(
        'opening-stats', parents=[input_pgn_parser, output_parser],
        help='Generates and save opening name table, can be saved in txt, csv or html file.')

    swiss = subparser.add_parser(
        'swiss', parents=[input_pgn_parser, output_parser],
        help='Generates swiss result table from the input pgn file. '
        'The output can be html, csv and txt.')

    # Sort
    sort.add_argument(
        '--sort-tag', type=str, required=False, default='eco',
        help='Sort the games by tag. [default=eco, value=(eco | ecot | event | date | round | white | black | site | plycount)].'
        ' e.g. --sort-tag event')
    sort.add_argument(
        '--sort-direction', type=str, required=False, default='lowtohigh',
        help='Write the direction to sort the games. [default=lowtohigh, value=(lowtohigh | hightolow)].')
    sort.add_argument(
        '--encoding', type=str, required=False, default='utf-8',
        help='Encoding used in reading pgn file when sorting, not required. [default=utf-8, value=(utf-8 | ISO-8859-1)]. '
        'If you encounter an error like "UnicodeDecodeError: utf-8 codec cannot decode ..." you can try, '
        '--encoding ISO-8859-1')

    # Add ECO
    addeco.add_argument(
        '--inecopgnfn', type=str, required=True,
        help='Write the reference eco.pgn filename, required.')

    # Swiss
    swiss.add_argument(
        '--round', type=int, required=False, default=20,
        help='Number of rounds, default=20.')

    parser.add_argument('-v', '--version', action='version', version=f'{pgnhelper.__version__}')

    args = parser.parse_args()

    g = None
    if args.command == 'sort':
        if args.inpgnfn == args.outpgnfn:
            raise ValueError('Input and output filenames should not be the same!')
        g = pgnhelper.app.PgnHelper(
            args.command,
            inpgnfn=args.inpgnfn,
            outpgnfn=args.outpgnfn,
            sort_tag=args.sort_tag,
            sort_direction=args.sort_direction,
            encoding=args.encoding
        )
    elif args.command == 'addeco':
        if args.inpgnfn == args.outpgnfn:
            raise ValueError('Input and output filenames should not be the same!')
        g = pgnhelper.app.PgnHelper(
            args.command,
            inpgnfn=args.inpgnfn,
            outpgnfn=args.outpgnfn,
            inecopgnfn=args.inecopgnfn            
        )
    elif args.command == 'roundrobin':
        if args.inpgnfn == args.output:
            raise ValueError('Input and output filenames should not be the same!')
        g = pgnhelper.app.PgnHelper(
            args.command,
            inpgnfn=args.inpgnfn,
            output=args.output,
            winpoint=args.win_point,
            drawpoint=args.draw_point,
            armageddonfile=args.armageddon_file,
            winpointarm=args.win_point_arm,
            losspointarm=args.loss_point_arm,
            showmaxscore=args.show_max_score
        )
    elif args.command == 'standing':
        if args.inpgnfn == args.output:
            raise ValueError('Input and output filenames should not be the same!')
        g = pgnhelper.app.PgnHelper(
            args.command,
            inpgnfn=args.inpgnfn,
            output=args.output,
            winpoint=args.win_point,
            drawpoint=args.draw_point,
            armageddonfile=args.armageddon_file,
            winpointarm=args.win_point_arm,
            losspointarm=args.loss_point_arm,
            showmaxscore=args.show_max_score
        )
    elif args.command == 'opening-stats':
        if args.inpgnfn == args.output:
            raise ValueError('Input and output filenames should not be the same!')
        g = pgnhelper.app.PgnHelper(
            args.command,
            inpgnfn=args.inpgnfn,
            output=args.output
        )
    elif args.command == 'swiss':
        if args.inpgnfn == args.output:
            raise ValueError('Input and output filenames should not be the same!')
        g = pgnhelper.app.PgnHelper(
            args.command,
            inpgnfn=args.inpgnfn,
            output=args.output,
            round=args.round
        )
    
    if g is not None:
        g.start()


if __name__ == '__main__':
    main()
