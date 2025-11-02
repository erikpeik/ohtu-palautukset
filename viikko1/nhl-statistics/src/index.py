from statistics_service import SortBy, StatisticsService
from player_reader import PlayerReader


def main():
    stats = StatisticsService(
        PlayerReader(
            "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt")
    )

    # järjestetään kaikkien tehopisteiden eli maalit+syötöt perusteella
    print("Top point getters:")
    for player in stats.top(5, SortBy.POINTS):
        print(player)

    print()
    # metodi toimii samalla tavalla kuin yo. kutsu myös ilman toista parametria
    for player in stats.top(5):
        print(player)

    print()
    # järjestetään maalien perusteella
    print("Top point goal scorers:")
    for player in stats.top(5, SortBy.GOALS):
        print(player)

    print()
    # järjestetään syöttöjen perusteella
    print("Top by assists:")
    for player in stats.top(5, SortBy.ASSISTS):
        print(player)


if __name__ == "__main__":
    main()
