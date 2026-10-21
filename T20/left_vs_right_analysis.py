"""
Right-handers vs Left-handers batting comparison
------------------------------------------------
Reads TWO csv files (same columns in both) and
  * prints count / mean / variance of each column, separately for each group
  * draws every graph with both groups on the SAME plot, in different colours

Columns used: player_name, runs, strike_rate_combined, centuries, fifties, S
The number of rows in each file can be different and can change freely.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# ------------------------------------------------------------------
# 1. SETTINGS  (change these)
# ------------------------------------------------------------------
RIGHT_FILE = "right_T20_final.csv"       # path of right-handers csv
LEFT_FILE = "left_T20_final.csv"         # path of left-handers csv

TOP_N = 50                           # top players shown PER GROUP in bar charts
HIST_DENSITY = False                   # True = compare shapes (use when group sizes differ a lot)

GROUPS = {                             # label -> (file, colour)
    "Right-handed": (RIGHT_FILE, "steelblue"),
    "Left-handed": (LEFT_FILE, "crimson"),
}

COLUMNS = {                            # column name in file -> label used in graphs
    "runs": "Total Runs",
    "strike_rate_combined": "Strike Rate",
    "centuries": "Centuries",
    "fifties": "Half Centuries",
    "S": "S",
}

# ------------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------------
WANTED = ["player_name", *COLUMNS]     # the only columns that get loaded

def load_data(path):
    df = pd.read_csv(path, usecols=lambda c: c.strip() in WANTED)
    df.columns = df.columns.str.strip()

    missing = [c for c in WANTED if c not in df.columns]
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df = df[WANTED]

    # sanity check: player_name must be text, not numbers
    if pd.api.types.is_numeric_dtype(df["player_name"]):
        raise ValueError(
            f"{path}: 'player_name' contains numbers, so the columns are "
            "misaligned (header and data have a different number of columns).\n"
            + df.head().to_string()
        )

    for col in COLUMNS:                # bad entries become NaN
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


data = {}                              # label -> dataframe
for label, (path, colour) in GROUPS.items():
    data[label] = load_data(path)
    print(f"Loaded {len(data[label])} players for {label}")

# ------------------------------------------------------------------
# 3. STATISTICS (mean and variance, separately for each group)
# ------------------------------------------------------------------
def column_stats(df, column):
    """Mean and variance of one column (missing values are ignored)."""
    values = df[column].dropna()
    return values.mean(), values.var()   # sample variance (n-1)
    # use values.var(ddof=0) for population variance


def print_all_stats():
    for label, df in data.items():
        print(f"\n=== {label} ===")
        print(f"{'Column':<18}{'Count':>7}{'Mean':>14}{'Variance':>18}")
        print("-" * 57)
        for col, name in COLUMNS.items():
            mean, var = column_stats(df, col)
            print(f"{name:<18}{df[col].count():>7}{mean:>14.4f}{var:>18.4f}")


# ------------------------------------------------------------------
# 4. GRAPHS - both groups on the same plot (one function per graph)
# ------------------------------------------------------------------
def _bar_both(column, title, filename):
    """Top players of each group on one bar chart, coloured by group.
    No player names on the x-axis and no value labels on the bars."""
    plt.figure(figsize=(14, 6.5))
    x_start = 0
    legend = []

    for label, (path, colour) in GROUPS.items():
        df = data[label]
        n = min(TOP_N, df[column].count())
        top = df.nlargest(n, column)
        xs = np.arange(x_start, x_start + n)
        plt.bar(xs, top[column], color=colour)      # no bar_label
        legend.append(Patch(color=colour, label=label))
        x_start += n + 1               # one empty slot between the two groups

    plt.xticks([])                     # remove player names / tick marks
    plt.xlabel(f"Top {TOP_N} players per group (ranked)")
    plt.ylabel(COLUMNS[column])
    plt.title(title)
    plt.legend(handles=legend)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()

def _hist_both(column, title, filename):
    """Overlapping histograms of both groups, with a mean line for each."""
    all_values = pd.concat([df[column].dropna() for df in data.values()])
    edges = np.histogram_bin_edges(all_values, bins=20)   # same bins for both

    plt.figure(figsize=(9, 5))
    for label, (path, colour) in GROUPS.items():
        values = data[label][column].dropna()
        plt.hist(values, bins=edges, alpha=0.55, color=colour,
                 edgecolor="black", label=label, density=HIST_DENSITY)
        plt.axvline(values.mean(), color=colour, linestyle="--", linewidth=2,
                    label=f"{label} mean = {values.mean():.2f}")
    plt.xlabel(COLUMNS[column])
    plt.ylabel("Share of players" if HIST_DENSITY else "Number of players")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()


def _scatter_both(x_col, y_col, title, filename):
    """Scatter plot of two columns, one colour per group."""
    plt.figure(figsize=(9, 6))
    for label, (path, colour) in GROUPS.items():
        df = data[label]
        plt.scatter(df[x_col], df[y_col], alpha=0.65, color=colour, label=label)
    plt.xlabel(COLUMNS[x_col])
    plt.ylabel(COLUMNS[y_col])
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()


# ---- Total runs ----
def plot_runs_vs_player():
    _bar_both("runs", f"Top {TOP_N} Players per Group by Total Runs",
              "both_runs_vs_player.png")

def plot_runs_hist():
    _hist_both("runs", "Distribution of Total Runs", "both_runs_hist.png")


# ---- Strike rate ----
def plot_strike_rate_vs_player():
    _bar_both("strike_rate_combined",
              f"Top {TOP_N} Players per Group by Strike Rate",
              "both_strike_rate_vs_player.png")

def plot_strike_rate_hist():
    _hist_both("strike_rate_combined", "Distribution of Strike Rate",
               "both_strike_rate_hist.png")


# ---- Centuries ----
def plot_centuries_vs_player():
    _bar_both("centuries", f"Top {TOP_N} Players per Group by Centuries",
              "both_centuries_vs_player.png")

def plot_centuries_hist():
    _hist_both("centuries", "Distribution of Centuries", "both_centuries_hist.png")


# ---- Half centuries ----
def plot_fifties_vs_player():
    _bar_both("fifties", f"Top {TOP_N} Players per Group by Half Centuries",
              "both_fifties_vs_player.png")

def plot_fifties_hist():
    _hist_both("fifties", "Distribution of Half Centuries",
               "both_fifties_hist.png")


# ---- Column S ----
def plot_S_vs_player():
    _bar_both("S", f"Top {TOP_N} Players per Group by S", "both_S_vs_player.png")

def plot_S_hist():
    _hist_both("S", "Distribution of S", "both_S_hist.png")


# ---- Relationship graphs ----
def plot_runs_vs_strike_rate():
    _scatter_both("strike_rate_combined", "runs",
                  "Total Runs vs Strike Rate", "both_runs_vs_strike_rate.png")

def plot_S_vs_runs():
    _scatter_both("runs", "S", "S vs Total Runs", "both_S_vs_runs.png")


# ---- Mean comparison (one bar per group for each column) ----
def plot_mean_comparison():
    """Side-by-side bars of each group's mean, one small panel per column."""
    fig, axes = plt.subplots(1, len(COLUMNS), figsize=(16, 4.5))
    for ax, (col, name) in zip(axes, COLUMNS.items()):
        means = [column_stats(data[label], col)[0] for label in GROUPS]
        colours = [colour for (_, colour) in GROUPS.values()]
        bars = ax.bar(list(GROUPS), means, color=colours)
        ax.bar_label(bars, fmt="%.2f", fontsize=8, padding=2)
        ax.set_title(f"Mean {name}")
        ax.tick_params(axis="x", rotation=20)
    plt.tight_layout()
    plt.savefig("both_mean_comparison.png", dpi=150)
    plt.show()


# ------------------------------------------------------------------
# 5. RUN
# ------------------------------------------------------------------
if __name__ == "__main__":
    print_all_stats()

    # Call whichever graphs you want, one at a time:
    plot_runs_vs_player()
    plot_runs_hist()
    plot_strike_rate_vs_player()
    plot_strike_rate_hist()
    plot_centuries_vs_player()
    plot_centuries_hist()
    plot_fifties_vs_player()
    plot_fifties_hist()
    plot_S_vs_player()
    plot_S_hist()
    plot_runs_vs_strike_rate()
    plot_S_vs_runs()
    plot_mean_comparison()
