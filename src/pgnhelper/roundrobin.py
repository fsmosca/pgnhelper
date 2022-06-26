"""Generates a round-robin result table.

It reads the input pgn file and generates a dataframe of round-robin table.
It also add columns for tie-break scores for tied players.

Typical tie-break system that can be applied to a round-robin tournament
according to FIDE.

13.16.2. Individual Round-Robin Tournaments:
    * Direct encounter
    * The greater number of wins, including forfeits
    * Sonneborn-Berger
    * Koya System (to be implemented in pgnhelper)

https://handbook.fide.com/files/handbook/C02Standards.pdf
"""


from pathlib import Path
from typing import Optional

import pandas as pd
from pretty_html_table import build_table

import pgnhelper.tiebreak
import pgnhelper.utility
import pgnhelper.elo
import pgnhelper.record


class RoundRobin:
    """Manages round-robin result table generation.

    Attributes:
      infn: The input pgn file.
      infnarm: The input pgn file with armageddon games.
      winpoint: The point for the winner.
      drawpoint: The point when player draws.
      winpointarm: The point for the winner in armageddon game.
      losspointarm: The point for the loser in armageddon game.
    """
    def __init__(self, infn: str, infnarm: Optional[str] = None,
                 winpoint: float = 1.0, drawpoint: float = 0.5,
                 winpointarm: float = 1.0, losspointarm: float = 0.0,
                 showmaxscore: bool = False):
        self.infn = infn
        self.infnarm = infnarm
        self.winpoint = winpoint
        self.drawpoint = drawpoint
        self.winpointarm = winpointarm
        self.losspointarm = losspointarm
        self.showmaxscore = showmaxscore
        self.record = pd.DataFrame()
        self.rank = pd.DataFrame()
        self.players = []
        self.israting = False

    def games_per_encounter(self) -> int:
        """Counts the number of games per encounter excluding armageddon.

        Returns:
          The number of games per encounter.
        """
        for p in self.players:
            for m in self.players:
                if p == m:
                    continue
                dfw = self.record.loc[
                    (self.record.White == p) &
                    (self.record.Black == m) &
                    (self.record.Arm == 0)]
                dfb = self.record.loc[
                    (self.record.Black == p) &
                    (self.record.White == m) &
                    (self.record.Arm == 0)]
                return len(dfw) + len(dfb)
        return 0

    def player_ranking(self) -> pd.DataFrame:
        """Generates a dataframe of player ranking.

        Returns:
          A pandas dataframe of players ranking.
        """
        is_arm = True if 1 in self.record['Arm'].unique() else False
        data_p = []
        for p in self.players:       
            if not is_arm:
                df_w = self.record[self.record.White == p]
                df_b = self.record[self.record.Black == p]
                score_w = len(df_w[df_w.Result == '1-0']) * self.winpoint
                score_w += len(df_w[df_w.Result == '1/2-1/2']) * self.drawpoint
                score_b = len(df_b[df_b.Result == '0-1']) * self.winpoint
                score_b += len(df_b[df_b.Result == '1/2-1/2']) * self.drawpoint
                final_score = score_w + score_b
            else:
                # Used to get the number of games for normal games.
                df_w = self.record[(self.record.White == p) & (self.record.Arm == 0)]
                df_b = self.record[(self.record.Black == p) & (self.record.Arm == 0)]

                # Get the score for normal games without draws.
                df_w_normal = self.record.loc[
                    (self.record.White == p) &
                    (self.record.Arm == 0) &
                    (self.record.Result != '1/2-1/2')]
                df_b_normal = self.record.loc[
                    (self.record.Black == p) &
                    (self.record.Arm == 0) &
                    (self.record.Result != '1/2-1/2')]
                score_w_n = len(df_w_normal.loc[df_w_normal.Result == '1-0']) * self.winpoint
                score_b_n = len(df_b_normal.loc[df_b_normal.Result == '0-1']) * self.winpoint

                # Get score for arm games.
                df_w_arm = self.record.loc[(self.record.White == p) & (self.record.Arm == 1)]
                df_b_arm = self.record.loc[(self.record.Black == p) & (self.record.Arm == 1)]

                # wins
                score_w_aw = len(df_w_arm.loc[df_w_arm.Result == '1-0']) * self.winpointarm
                score_b_aw = len(df_b_arm.loc[df_b_arm.Result == '0-1']) * self.winpointarm
                score_b_aw += len(df_b_arm.loc[df_b_arm.Result == '1/2-1/2']) * self.winpointarm

                # loses
                score_w_al = len(df_w_arm.loc[df_w_arm.Result == '0-1']) * self.losspointarm
                score_w_al += len(df_w_arm.loc[df_w_arm.Result == '1/2-1/2']) * self.losspointarm
                score_b_al = len(df_b_arm.loc[(df_b_arm.Result == '1-0')]) * self.losspointarm

                final_score = (score_w_n + score_b_n + score_w_aw + score_b_aw
                                         + score_w_al + score_b_al)

            if self.israting:
                rating = df_w.WElo.iloc[0]  # all players have at least played a game with white
                data_p.append([p, rating, len(df_w) + len(df_b), final_score])
            else:
                data_p.append([p, len(df_w) + len(df_b), final_score])
        if self.israting:
            self.rank = pd.DataFrame(
                data_p,
                columns=['Name', 'Rating', 'Games', 'Score'])
        else:
            self.rank = pd.DataFrame(data_p, columns=['Name', 'Games', 'Score'])
        self.rank = self.rank.sort_values(by=['Score', 'Name'],
                                          ascending=[False, True])
        self.rank = self.rank.reset_index(drop=True)
        return self.rank

    def table(self) -> pd.DataFrame:
        """Generates a round-robin result table.

        The table is sorted by DE or Direct Encounter, Number of Wins
        and SB (sonneborn-Berger)

        Returns:
          A pandas dataframe of round-robin table.
        """
        dfall = []
        dfn, self.players, self.israting = pgnhelper.record.get_pgn_data(self.infn, is_arm=False)
        dfall.append(dfn)
        if self.infnarm is not None:
            dfa, _, _ = pgnhelper.record.get_pgn_data(self.infnarm, is_arm=True)
            dfall.append(dfa)
        self.record = pd.concat(dfall, ignore_index=False)
        is_arm = True if 1 in self.record.Arm.unique() else False

        # 1. Create a dataframe of player ranking.
        self.rank = self.player_ranking()
        gpe = self.games_per_encounter()

        # 1.1 Apply Direct Encounter tie-break
        df_de = pgnhelper.tiebreak.direct_encounter(
            self.record, self.rank, self.winpoint, self.drawpoint,
            self.winpointarm, self.losspointarm)
        df_de = df_de.sort_values(by=['Score', 'DE', 'Name'],
                                  ascending=[False, False, True])
        df_de = df_de.reset_index(drop=True)

        # 1.2 Apply Number of Wins tie-break
        df_wins = pgnhelper.tiebreak.num_wins(self.record, df_de)
        df_wins = df_wins.sort_values(by=['Score', 'DE', 'Wins', 'Name'],
                                      ascending=[False, False, False, True])
        df_wins = df_wins.reset_index(drop=True)  

        # 1.3 Apply Sonneborn-Berger tie-break
        df_sb = pgnhelper.tiebreak.sonneborn_berger(
            self.record, df_wins, gpe=gpe, winpoint=1.0, drawpoint=0.5)
        df_sb = df_sb.sort_values(
            by=['Score', 'DE', 'Wins', 'SB', 'Name'],
            ascending=[False, False, False, False, True])
        df_sb = df_sb.reset_index(drop=True)

        # 1.4 Apply the Koya system.
        df_koya = pgnhelper.tiebreak.koya_system(
            self.record, df_sb, winpoint=1.0, drawpoint=0.5)
        df_koya = df_koya.sort_values(
            by=['Score', 'DE', 'Wins', 'SB', 'Koya', 'Name'],
            ascending=[False, False, False, False, False, True])
        df_koya = df_koya.reset_index(drop=True)
        df_final = df_koya.copy()

        # 2. Build a round-robin dataframe.
        if self.israting:
            # Add rating change.
            rc = []
            for p in list(df_final.Name):
                r = pgnhelper.elo.get_rating_change(self.record, p, k=10)
                rc.append(round(r, 2))
            data_rr = {'Name': df_final.Name, 'Rating': df_final.Rating, 'RChg': rc}
        else:
            data_rr = {'Name': df_final.Name.unique()}
        cnt = 1
        for p in df_final.Name.unique():
            data_v = []
            for op in df_final.Name.unique():
                if p == op:
                    v = 'x'
                else:
                    score = pgnhelper.utility.get_encounter_score(
                        self.record, p, op, self.winpoint, self.drawpoint,
                        self.winpointarm, self.losspointarm)
                    v = score[1]  # use the score of op only
                data_v.append(v)
            data_rr.update({cnt: data_v})
            cnt += 1
        df_rr = pd.DataFrame(data_rr)

        # 3. Add other columns at the end.
        df_rr['Games'] = df_final['Games']
        df_rr['Score'] = df_final['Score']
        max_score = df_final['Games'] * self.winpoint
        if self.showmaxscore:
            df_rr['MaxScore'] = max_score
        df_rr['Score%'] = 100 * df_final['Score'] / max_score
        df_rr['Score%'] = df_rr['Score%'].round(2)
        df_rr['DE'] = df_final['DE'].round(2)
        df_rr['Wins'] = df_final['Wins'].round(0)
        df_rr['SB'] = df_final['SB'].round(2)
        df_rr['Koya'] = df_final['Koya'].round(2)

        # 4. Insert rank column at first column.
        df_rr.insert(loc=0, column='Rank', value=range(1, len(df_rr) + 1))
        return df_rr

    def standing(self) -> pd.DataFrame:
        """Returns a dataframe of player standing.

        The standing is sorted by score, with tie-breaks DE, Wins and SB.
        """
        df = self.table()
        if 'Rating' in df.columns:
            dfs = df[['Rank', 'Name', 'Rating', 'RChg', 'Games', 'Score', 'Score%', 'DE', 'Wins', 'SB', 'Koya']]
        else:
            dfs = df[['Rank', 'Name', 'Games', 'Score', 'Score%', 'DE', 'Wins', 'SB', 'Koya']]
        return dfs
