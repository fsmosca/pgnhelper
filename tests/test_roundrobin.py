"""Run round-robin test.

1. pip install pgnhelper
2. copy tests and pgn folders from github repo

Example dir structure:
c:/mypgnhelper
c:/mypgnhelper/pgn/norway_chess_2022_classical.pgn
c:/mypgnhelper/pgn/norway_chess_2022_armageddon.pgn
c:/mypgnhelper/tests/test_roundrobin.py

Python version should be >= 3.7

Command line:

   c:/pgnhelper> python -m pytest ./tests/test_roundrobin.py
"""


from pathlib import Path
import pgnhelper


fn_classical = Path('./pgn/norway_chess_2022_classical.pgn')
fn_armageddon = Path('./pgn/norway_chess_2022_armageddon.pgn')


df = pgnhelper.roundrobin.round_robin(
    fn_classical,
    armageddonfile=fn_armageddon,
    winpoint=3.0, 
    winpointarm=1.5,
    losspointarm=1.0,
    showmaxscore=True
)


def test_num_players():
    assert(len(df.Name) == 10)


def test_player_rating(name='Anand, Viswanathan', rating=2751):
    df_player = df.loc[df.Name == name]
    assert int(df_player.iloc[0]['Rating']) == rating


def test_player_score(name='So, Wesley'):
    df_player = df.loc[df.Name == name]
    assert df_player.iloc[0]['Score'] == 12.5


def test_player_rank(name='Carlsen, Magnus', rank=1):
    df_player = df.loc[df.Name == name]
    assert df_player.iloc[0]['Rank'] == rank


def test_tb_direct_encounter(name='Topalov, Veselin', de=1.5):
    df_player = df.loc[df.Name == name]
    assert df_player.iloc[0]['DE'] == de


def test_tb_num_wins(name='Tari, Aryan', num_win=1):
    df_player = df.loc[df.Name == name]
    assert df_player.iloc[0]['Wins'] == num_win
