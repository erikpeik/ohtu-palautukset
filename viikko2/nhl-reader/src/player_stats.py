class PlayerStats:
    def __init__(self, reader, console, season):
        self._reader = reader
        self._players = self._reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        nationality_players = list(
            filter(lambda p: p.nationality == nationality, self._players))

        nationality_players.sort(
            key=lambda p: p.goals + p.assists, reverse=True)
        return nationality_players

    def get_nationalities(self):
        nationalities = set()
        for player in self._players:
            nationalities.add(player.nationality)
        return list(nationalities)
