from enum import IntEnum


class ScoreName(IntEnum):
    LOVE = 0
    FIFTEEN = 1
    THIRTY = 2
    FORTY = 3

    def __str__(self):
        display_names = {
            ScoreName.LOVE: "Love",
            ScoreName.FIFTEEN: "Fifteen",
            ScoreName.THIRTY: "Thirty",
            ScoreName.FORTY: "Forty",
        }
        return display_names[self]


class TennisGame:
    MIN_POINTS_FOR_ENDGAME = 4
    MAX_TIED_SCORE_BEFORE_DEUCE = 3

    def __init__(self, player1_name, player2_name):
        self.player1 = player1_name
        self.player2 = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == self.player1:
            self.player1_score += 1
        else:
            self.player2_score += 1

    def get_score(self):
        if self.is_tied():
            return self.get_tied_score()
        if self.is_endgame():
            return self.get_endgame_score()
        return self.get_regular_score()

    def is_tied(self):
        return self.player1_score == self.player2_score

    def get_tied_score(self):
        if self.player1_score < self.MAX_TIED_SCORE_BEFORE_DEUCE:
            name = self.get_score_label(self.player1_score)
            return f"{name}-All"
        return "Deuce"

    def is_endgame(self):
        return (self.player1_score >= self.MIN_POINTS_FOR_ENDGAME or
                self.player2_score >= self.MIN_POINTS_FOR_ENDGAME)

    def get_endgame_score(self):
        diff = self.player1_score - self.player2_score
        if diff == 1:
            return f"Advantage {self.player1}"
        elif diff == -1:
            return f"Advantage {self.player2}"
        elif diff >= 2:
            return f"Win for {self.player1}"
        else:
            return f"Win for {self.player2}"

    def get_regular_score(self):
        return f"{self.get_score_label(self.player1_score)}-{self.get_score_label(self.player2_score)}"

    def get_score_label(self, points):
        return str(ScoreName(points))
