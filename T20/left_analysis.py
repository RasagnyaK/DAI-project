"""
Cricket batting statistics analysis (CSV version)
-------------------------------------------------
Reads a CSV file and gives mean / variance for:
    runs, strike_rate_combined, centuries, fifties, S
with a SEPARATE function for each graph.

The number of rows can change freely. Only the column names matter,
and they are expected to stay the same.
"""

import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# 1. SETTINGS
# ------------------------------------------------------------------
FILE_PATH = "left_T20_final.csv"  # change to your CSV path
TOP_N = 50                     # max players shown in bar charts

COLUMNS = {                        # column name in file -> label used in graphs
    "runs": "Total Runs",
    "strike_rate_combined": "Strike Rate",
    "centuries": "Centuries",
    "fifties": "Half Centuries",
    "S": "S",
}

# ------------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------------
WANTED = ["player_name", *COLUMNS]                 # the only columns that get loaded

def load_data(path=FILE_PATH):
    # usecols loads ONLY these columns; everything else in the file is skipped.
    # The lambda also tolerates stray spaces in the header names.
    df = pd.read_csv(path, usecols=lambda c: c.strip() in WANTED)
    df.columns = df.columns.str.strip()

    missing = [c for c in WANTED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in file: {missing}")
    df = df[WANTED]                                # fixed column order

    # sanity check: player_name must be text, not numbers
    if pd.api.types.is_numeric_dtype(df["player_name"]):
        raise ValueError(
            "'player_name' contains numbers, so the columns are misaligned.\n"
            "First rows read from the file:\n" + df.head().to_string()
        )

    # make sure the analysed columns are numeric (bad entries become NaN)
    for col in COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


df = load_data()
print(f"Loaded {len(df)} players")

# ------------------------------------------------------------------
# 3. STATISTICS (mean and variance of each column, separately)
# ------------------------------------------------------------------
def column_stats(column):
    """Mean and variance of one column (missing values are ignored)."""
    data = df[column].dropna()
    return data.mean(), data.var()      # sample variance (n-1)
    # use data.var(ddof=0) for population variance


def print_all_stats():
    print(f"\n{'Column':<18}{'Count':>7}{'Mean':>14}{'Variance':>18}")
    print("-" * 57)
    for col, label in COLUMNS.items():
        mean, var = column_stats(col)
        print(f"{label:<18}{df[col].count():>7}{mean:>14.4f}{var:>18.4f}")


# One stats function per column, if you want to call them individually
def stats_runs():           return column_stats("runs")
def stats_strike_rate():    return column_stats("strike_rate_combined")
def stats_centuries():      return column_stats("centuries")
def stats_fifties():        return column_stats("fifties")
def stats_S():              return column_stats("S")


# ------------------------------------------------------------------
# 4. GRAPHS (one function per graph)
# ------------------------------------------------------------------
def _bar_vs_player(column, title, color, filename):
    """Vertical bar chart: player name on X axis, the column's value on Y axis."""
    n = min(TOP_N, df[column].count())             # works even with few rows
    top = df.nlargest(n, column)                   # highest first (left to right)
    plt.figure(figsize=(max(9, 0.8 * n + 3), 6))
    bars = plt.bar(top["player_name"].astype(str), top[column], color=color)
    plt.bar_label(bars, fmt="%g", fontsize=8, padding=2)   # value on top of each bar
    plt.xlabel("Player")
    plt.ylabel(COLUMNS[column])
    plt.title(title.format(n=n))
    plt.xticks(rotation=45, ha="right")            # tilt names so they don't overlap
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()


def _histogram(column, title, color, filename):
    """Distribution of a column across all players, with mean line."""
    data = df[column].dropna()
    bins = max(5, min(25, len(data) // 5))         # bin count adapts to row count
    plt.figure(figsize=(9, 5))
    plt.hist(data, bins=bins, color=color, edgecolor="black")
    plt.axvline(data.mean(), color="red", linestyle="--",
                label=f"Mean = {data.mean():.2f}")
    plt.xlabel(COLUMNS[column])
    plt.ylabel("Number of players")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()


# ---- Total runs ----
def plot_runs_vs_player():
    _bar_vs_player("runs", "Top {n} Players by Total Runs",
                   "steelblue", "runs_vs_player.png")

def plot_runs_hist():
    _histogram("runs", "Distribution of Total Runs", "steelblue", "runs_hist.png")


# ---- Strike rate ----
def plot_strike_rate_vs_player():
    _bar_vs_player("strike_rate_combined", "Top {n} Players by Strike Rate",
                   "darkorange", "strike_rate_vs_player.png")

def plot_strike_rate_hist():
    _histogram("strike_rate_combined", "Distribution of Strike Rate",
               "darkorange", "strike_rate_hist.png")


# ---- Centuries ----
def plot_centuries_vs_player():
    _bar_vs_player("centuries", "Top {n} Players by Centuries",
                   "seagreen", "centuries_vs_player.png")

def plot_centuries_hist():
    _histogram("centuries", "Distribution of Centuries", "seagreen",
               "centuries_hist.png")


# ---- Half centuries ----
def plot_fifties_vs_player():
    _bar_vs_player("fifties", "Top {n} Players by Half Centuries",
                   "purple", "fifties_vs_player.png")

def plot_fifties_hist():
    _histogram("fifties", "Distribution of Half Centuries", "purple",
               "fifties_hist.png")


# ---- Column S ----
def plot_S_vs_player():
    _bar_vs_player("S", "Top {n} Players by S", "crimson", "S_vs_player.png")

def plot_S_hist():
    _histogram("S", "Distribution of S", "crimson", "S_hist.png")


# ---- Relationship graphs (optional) ----
def plot_runs_vs_strike_rate():
    plt.figure(figsize=(9, 6))
    plt.scatter(df["strike_rate_combined"], df["runs"], alpha=0.6, color="teal")
    plt.xlabel("Strike Rate")
    plt.ylabel("Total Runs")
    plt.title("Total Runs vs Strike Rate")
    plt.tight_layout()
    plt.savefig("runs_vs_strike_rate.png", dpi=150)
    plt.show()


def plot_S_vs_runs():
    plt.figure(figsize=(9, 6))
    plt.scatter(df["runs"], df["S"], alpha=0.6, color="crimson")
    plt.xlabel("Total Runs")
    plt.ylabel("S")
    plt.title("S vs Total Runs")
    plt.tight_layout()
    plt.savefig("S_vs_runs.png", dpi=150)
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