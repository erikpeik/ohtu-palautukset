import requests
from player import Player


def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    players = []

    for player_dict in response:
        player = Player(player_dict)
        players.append(player)

    nationality = "FIN"


    print(f"Players from {nationality}:")
    print()

    nationality_players = list(filter(lambda p: p.nationality == nationality, players))
    nationality_players.sort(key=lambda p: p.goals + p.assists, reverse=True)

    for player in nationality_players:
        print(player)

if __name__ == "__main__":
    main()
