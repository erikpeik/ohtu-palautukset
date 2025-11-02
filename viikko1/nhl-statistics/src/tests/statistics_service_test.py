import unittest
from statistics_service import SortBy, StatisticsService
from player import Player


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  # 4+12 = 16
            Player("Lemieux", "PIT", 45, 54),  # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53),  # 37+53 = 90
            Player("Yzerman", "DET", 42, 56),  # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_player_found(self):
        player = self.stats.search("Semenko")
        self.assertEqual(player.name, "Semenko")

    def test_search_player_not_found(self):
        player = self.stats.search("Selänne")
        self.assertEqual(player, None)

    def test_search_team_players(self):
        team_players = self.stats.team("EDM")
        self.assertEqual(len(team_players), 3)
        self.assertEqual(team_players[0].name, "Semenko")
        self.assertEqual(team_players[1].name, "Kurri")
        self.assertEqual(team_players[2].name, "Gretzky")

    def test_top_scorers(self):
        # starts from index 0 so 2 means 3 players
        top_players = self.stats.top(2)
        self.assertEqual(len(top_players), 3)
        self.assertEqual(top_players[0].name, "Gretzky")  # 124
        self.assertEqual(top_players[1].name, "Lemieux")  # 99
        self.assertEqual(top_players[2].name, "Yzerman")  # 98

    def test_top_goal_scorers(self):
        top_players = self.stats.top(2, sort_by=SortBy.GOALS)
        self.assertEqual(len(top_players), 3)
        self.assertEqual(top_players[0].name, "Lemieux")  # 45
        self.assertEqual(top_players[1].name, "Yzerman")  # 42
        self.assertEqual(top_players[2].name, "Kurri")    # 37

    def test_top_assist_scorers(self):
        top_players = self.stats.top(2, sort_by=SortBy.ASSISTS)
        self.assertEqual(len(top_players), 3)
        self.assertEqual(top_players[0].name, "Gretzky")  # 89
        self.assertEqual(top_players[1].name, "Yzerman")  # 56
        self.assertEqual(top_players[2].name, "Lemieux")  # 54
