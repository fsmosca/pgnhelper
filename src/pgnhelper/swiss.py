"""Generates a swiss result table.

It reads the input pgn file and generates a dataframe of swiss table.
It also add columns for tie-break scores for tied players.

Typical tie-break system that can be applied to a round-robin tournament
according to FIDE.

13.16.4. Individual Swiss Tournaments where not all the ratings are consistent:
   Buchholz Cut 1
   Buchholz
   Sonneborn-Berger
   Cumulative system - Sum of Progressive Scores
   Direct encounter
   The greater number of wins including forfeits
   The greater number of wins with Black pieces

13.16.5. Individual Swiss Tournaments where all the ratings are consistent:
   Buchholz Cut 1
   Buchholz
   Direct encounter
   AROC
   The greater number of wins including forfeits
   The greater number of wins with Black pieces
   The greater number of games with Black (unplayed games shall be counted as played with White)
   Sonneborn-Berger 

https://handbook.fide.com/files/handbook/C02Standards.pdf

Other reference:
FIDE Chess.com Grand Swiss 2021

4. 8. 3. Tie-breaks
If two (2) or more players score the same points, the tie is to be decided by the following criteria, in order of priority:
a) Buchholz Cut 1;
b) Buchholz;
c) Sonneborn-Berger;
d) Direct encounter between the players in tie;
e) Drawing of lots.

All tie-breaks are calculated as described in C.02.13 of the FIDE Handbook.
"""


from pathlib import Path
from typing import Optional

import pandas as pd
from pretty_html_table import build_table

import pgnhelper.tiebreak
import pgnhelper.utility
import pgnhelper.elo
import pgnhelper.record


# Define the tie-break ordering.
swiss_tiebreak = {
    0: {'name': 'Buchholz Cut 1', 'label': 'TB1', 'cut': 1},
    1: {'name': 'Buchholz', 'label': 'TB2', 'cut': 0}
}


class Swiss:
    """Manages swiss result table generation.

    Attributes:
      infn: The input pgn file.
      infnarm: The input pgn file with armageddon games.
      winpoint: The point for the winner.
      drawpoint: The point when player draws.
      winpointarm: The point for the winner in armageddon game.
      losspointarm: The point for the loser in armageddon game.
    """
    def __init__(self, infn: str):
        self.infn = infn
        self.record = pd.DataFrame()
        self.rank = pd.DataFrame()
        self.winpoint = 1.0
        self.drawpoint = 0.5
        self.israting = False

    def player_ranking(self) -> pd.DataFrame:
        """Generates a dataframe of player ranking.

        Returns:
          A pandas dataframe of players ranking.
        """
        data_p = []
        for p in self.players:
            df_w = self.record[self.record.White == p]
            df_b = self.record[self.record.Black == p]
            score_w = len(df_w[df_w.Result == '1-0']) * self.winpoint
            score_w += len(df_w[df_w.Result == '1/2-1/2']) * self.drawpoint
            score_b = len(df_b[df_b.Result == '0-1']) * self.winpoint
            score_b += len(df_b[df_b.Result == '1/2-1/2']) * self.drawpoint
            final_score = score_w + score_b

            if self.israting:
                rating = pgnhelper.elo.get_rating(self.record, p)
                if rating == '?':
                    print(f'Warning player {p} has a rating of {rating}! Rating is disabled.')
                    data_p.append([p, len(df_w) + len(df_b), final_score])
                else:
                    data_p.append([p, rating, len(df_w) + len(df_b), final_score])
            else:
                data_p.append([p, len(df_w) + len(df_b), final_score])
        if self.israting:
            self.rank = pd.DataFrame(data_p,
                    columns=['Name', 'Rating', 'Games', 'Score'])
        else:
            self.rank = pd.DataFrame(data_p, columns=['Name', 'Games', 'Score'])
        self.rank = self.rank.sort_values(by=['Score', 'Name'],
                ascending=[False, True])
        self.rank = self.rank.reset_index(drop=True)
        return self.rank


    def table(self) -> pd.DataFrame:
        """Generates a swiss result table.

        The table is sorted by [score, buchholz cut 1, buchholz, sonneborn-berger, direct encounter].

        Returns:
          A pandas dataframe of swiss table.
        """
        self.record, self.players, self.israting = pgnhelper.record.get_pgn_data(self.infn)
        # self.israting = False

        # 1. Create a dataframe of player ranking.
        self.rank = self.player_ranking()

        # 1.1 Apply buchholz tie-break. [buchholz cut 1, buchholz]
        tb_label = []

        cut = swiss_tiebreak[0]['cut']
        label = swiss_tiebreak[0]['label']
        tb_label.append(label)
        df_tb1 = pgnhelper.tiebreak.tb_buchholz(self.record, self.rank, cut=cut, label=label)

        cut = swiss_tiebreak[1]['cut']
        label = swiss_tiebreak[1]['label']
        tb_label.append(label)
        df_tb2 = pgnhelper.tiebreak.tb_buchholz(self.record, df_tb1, cut=cut, label=label)

        # 1.2 Apply Sonneborn-Berger.
        df_tb3 = pgnhelper.tiebreak.sonneborn_berger(self.record, df_tb2, label='TB3')
        df_tb3 = df_tb3.sort_values(
            by=['Score', 'TB1', 'TB2', 'TB3', 'Name'],
            ascending=[False, False, False, False, True]
        )
        tb_label.append('TB3')
        df_tb3 = df_tb3.reset_index(drop=True)

        # 1.3 Apply Direct Encounter tie-break
        df_tb4 = pgnhelper.tiebreak.direct_encounter(self.record, df_tb3, label='TB4')
        df_tb4 = df_tb4.sort_values(
            by=['Score', 'TB1', 'TB2', 'TB3', 'TB4', 'Name'],
            ascending=[False, False, False, False, False, True]
        )
        tb_label.append('TB4')
        df_tb4 = df_tb4.reset_index(drop=True)

        df_final = df_tb4.copy()

        # 2. Build a swiss standing dataframe.
        if self.israting:
            # Add rating change.
            rc = []
            for p in list(df_final.Name):
                r = pgnhelper.elo.get_rating_change(self.record, p, k=10)
                rc.append(round(r, 2))
            data_swiss = {'Name': df_final.Name, 'Rating': df_final.Rating, 'RChg': rc}
        else:
            data_swiss = {'Name': df_final.Name.unique()}
        data_swiss = pd.DataFrame(data_swiss)

        # 3. Add other columns at the end.
        data_swiss['Games'] = df_final['Games']
        data_swiss['Score'] = df_final['Score']
        data_swiss['Score%'] = 100 * df_final['Score'] / df_final['Games']
        data_swiss['Score%'] = data_swiss['Score%'].round(2)
        data_swiss[tb_label[0]] = df_tb1[tb_label[0]].round(2)
        data_swiss[tb_label[1]] = df_tb2[tb_label[1]].round(2)
        data_swiss[tb_label[2]] = df_tb3[tb_label[2]].round(2)
        data_swiss[tb_label[3]] = df_tb4[tb_label[3]].round(2)

        # 4. Insert rank column at first column.
        data_swiss.insert(loc=0, column='Rank', value=range(1, len(data_swiss) + 1))
        return data_swiss
