from player_reader import PlayerReader
from player_stats import PlayerStats

from rich.console import Console
from rich.table import Table


console = Console()

seasons = ["2018-19", "2019-20", "2020-21",
           "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]


def render_players_table(players, season, nationality):
    table = Table(title=f"Season {season} players from {nationality}")

    table.add_column("Released", style="cyan", no_wrap=True)
    table.add_column("teams", style="magenta")
    table.add_column("goals", justify="right", style="green")
    table.add_column("assists", justify="right", style="green")
    table.add_column("points", justify="right", style="green")

    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.points),
        )
    console.print(table)


def main():
    season = console.input(
        f"Season [magenta][{', '.join(seasons)}][/magenta] [cyan](2024-25)[cyan]: "
    ).strip()
    if season not in seasons:
        season = "2024-25"

    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader, console, season)

    nationalities = stats.get_nationalities()

    while True:
        console.print(
            f"Nationality options: [magenta][{', '.join(nationalities)}][/magenta]")
        nationality = console.input(
            "Nationality [cyan](or ENTER to quit)[/cyan]: ").strip()

        if not nationality:
            break
        if nationality not in nationalities:
            console.print("[red]Invalid nationality[/red]")
            continue

        players = stats.top_scorers_by_nationality(nationality)
        render_players_table(players, season, nationality)


if __name__ == "__main__":
    main()
