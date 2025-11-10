class Player:
    def __init__(self, player_dict):
        self.name = player_dict['name']
        self.nationality = player_dict['nationality']
        self.assists = player_dict['assists']
        self.goals = player_dict['goals']
        self.points = player_dict['goals'] + player_dict['assists']
        self.team = player_dict['team']
        self.games = player_dict['games']

    def __str__(self):
        return f"{self.name:<25} {self.team:<15} {self.goals} + {self.assists} = {self.points}"
