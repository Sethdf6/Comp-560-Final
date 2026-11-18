# draws results/chart.png from results/games.csv
# needs matplotlib
#
# python3 results/plot.py

import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))

# same order as the table in the readme
AGENTS = [
    "random",
    "greedy",
    "expectimax d1",
    "expectimax d2",
    "expectimax d3",
    "d2 snake only",
    "d2 empty only",
    "d3 snake only",
]

SURFACE = "#fcfcfb"
BAR = "#2a78d6"
INK = "#0b0b0b"
MUTED = "#898781"
GRID = "#e1e0d9"


def load():
    with open(os.path.join(HERE, "games.csv"), newline="") as file:
        rows = list(csv.DictReader(file))

    stats = []
    for name in AGENTS:
        games = [row for row in rows if row["agent"] == name]
        count = len(games)
        reached = sum(int(row["max_tile"]) >= 2048 for row in games)
        score = sum(int(row["score"]) for row in games) / count
        stats.append((name, count, 100 * reached / count, score))
    return stats


def panel(axis, names, values, title, label, limit):
    spots = range(len(names))
    axis.barh(spots, values, height=0.55, color=BAR)
    axis.set_yticks(spots)
    axis.set_yticklabels(names, color=INK, fontsize=11)
    axis.set_xlim(0, limit)
    axis.set_title(title, loc="left", color=INK, fontsize=12, pad=10)

    # the number sits at the end of every bar
    for spot, value in zip(spots, values):
        axis.text(value + limit * 0.015, spot, label(value), va="center", color=INK, fontsize=10)

    axis.set_facecolor(SURFACE)
    axis.xaxis.grid(True, color=GRID, linewidth=0.8)
    axis.set_axisbelow(True)
    axis.tick_params(axis="x", colors=MUTED, labelsize=9, length=0)
    axis.tick_params(axis="y", length=0)
    for side in ("top", "right", "bottom"):
        axis.spines[side].set_visible(False)
    axis.spines["left"].set_color("#c3c2b7")


def main():
    stats = load()
    names = [row[0] for row in stats]
    games = stats[0][1]

    figure, (left, right) = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    figure.patch.set_facecolor(SURFACE)

    panel(left, names, [row[2] for row in stats],
          "games that reached 2048 (%)", lambda value: f"{int(value + 0.5)}%", 100)
    panel(right, names, [row[3] for row in stats],
          "average score", lambda value: f"{round(value):,}", 34000)

    # the panels share the y axis, so flip it once to put the first agent on top
    left.invert_yaxis()

    figure.text(0.01, 0.01, f"{games} games per agent, 4x4 board", color=MUTED, fontsize=9)
    figure.tight_layout(rect=(0, 0.04, 1, 1))

    out = os.path.join(HERE, "chart.png")
    figure.savefig(out, dpi=160, facecolor=SURFACE)
    print("saved to", out)


if __name__ == "__main__":
    main()
