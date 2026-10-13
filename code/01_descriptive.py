# =====================================================================
# Table 2 — Card & Krueger (1994), "Minimum Wages and Employment"
# Distribution of store types, and means of key variables (Wave 1 & Wave 2)
# =====================================================================
import numpy as np
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------
# 0. Locate the project root.
#    `__file__` is the absolute path of this script, so this works no matter
#    which directory the script is launched from (e.g. `python code/make_table2.py`
#    from the project root, or an absolute path from elsewhere). Without this,
#    a bare `data/processed/...` path only works when the CWD is the project root.
# ---------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------
# 1. Load the cleaned data
# ---------------------------------------------------------------------
df = pd.read_csv(ROOT / "data" / "processed" / "cleaned_data.csv")

# ---------------------------------------------------------------------
# 2. Data preparation
# ---------------------------------------------------------------------
# Full meal price = soda + fries + entree
df["price1"] = df["psoda"] + df["pfry"] + df["pentree"]      # Wave 1
df["price2"] = df["psoda2"] + df["pfry2"] + df["pentree2"]   # Wave 2

# Chain dummies (1 = Burger King, 2 = KFC, 3 = Roy Rogers, 4 = Wendy's)
df["bk"]    = (df["chain"] == 1).astype(int)
df["kfc"]   = (df["chain"] == 2).astype(int)
df["roy"]   = (df["chain"] == 3).astype(int)
df["wendy"] = (df["chain"] == 4).astype(int)

# Company-owned dummy
df["co_owned"] = (df["co_owned"] == 1).astype(int)

# Starting-wage threshold dummies.
# `np.isclose(atol=1e-4)` handles floating-point noise: $5.05 is stored as
# 5.0500002, so a literal `== 5.05` would silently match 0 stores and wrongly
# report 0%. The tolerance is far below any real wage gap ($0.05).
# Missing wages evaluate to False -> 0, i.e. a full-sample denominator, matching
# the paper's convention (wave-1 "Wage = $4.25" = 101/331 = 30.5%).
df["wage_425_1"] = np.isclose(df["wage_st"],  4.25, atol=1e-4).astype(int)
df["wage_425_2"] = np.isclose(df["wage_st2"], 4.25, atol=1e-4).astype(int)
df["wage_505_2"] = np.isclose(df["wage_st2"], 5.05, atol=1e-4).astype(int)

# Recruiting-bonus dummies (reported as percentages in the paper).
# Wave 1 uses `bonus`; the wave-2 recruiting bonus is stored as `special2`
# (there is no `bonus2` column in the cleaned data).
# Missing responses are kept as NaN so they are excluded from the mean, which
# reproduces the paper's wave-2 values (20.3% / 23.4%).
df["bonus"]  = df["bonus"].eq(1).astype(float).mask(df["bonus"].isna())
df["bonus2"] = df["special2"].eq(1).astype(float).mask(df["special2"].isna())

# Percentage full-time employees = 100 * full-time / FTE, where
#   FTE = full-time + managers + 0.5 * part-time   (see 00_clean_data.do).
# (This is Card & Krueger's Table 2 definition: full-time workers as a share
#  of full-time-equivalent employment, giving NJ ~32.8% in Wave 1.)
df["pct_ft1"] = 100 * df["empft"]  / df["fte1"]
df["pct_ft2"] = 100 * df["empft2"] / df["fte2"]

# FTE employment is already in the cleaned data as `fte1` / `fte2`:
#   fte = full-time + managers + 0.5 * part-time   (see 00_clean_data.do)

# ---------------------------------------------------------------------
# 3. Variable inventory: (panel, label, column, scale)
#    scale = 100 for proportions reported as percentages, else 1
# ---------------------------------------------------------------------
VARS = [
    # Panel A — distribution of store types (percentages)
    ("Distribution of store types", "Burger King",   "bk",        100),
    ("Distribution of store types", "KFC",           "kfc",       100),
    ("Distribution of store types", "Roy Rogers",    "roy",       100),
    ("Distribution of store types", "Wendy's",       "wendy",     100),
    ("Distribution of store types", "Company-owned", "co_owned",  100),

    # Panel B — means in Wave 1
    ("Means in Wave 1", "FTE employment",                 "fte1",        1),
    ("Means in Wave 1", "Percentage full-time employees", "pct_ft1",     1),
    ("Means in Wave 1", "Starting wage",                  "wage_st",     1),
    ("Means in Wave 1", "Wage = $4.25 (%)",               "wage_425_1",  100),
    ("Means in Wave 1", "Price of full meal",             "price1",      1),
    ("Means in Wave 1", "Hours open (weekday)",           "hrsopen",     1),
    ("Means in Wave 1", "Recruiting bonus",               "bonus",       100),

    # Panel C — means in Wave 2
    ("Means in Wave 2", "FTE employment",                 "fte2",        1),
    ("Means in Wave 2", "Percentage full-time employees", "pct_ft2",     1),
    ("Means in Wave 2", "Starting wage",                  "wage_st2",    1),
    ("Means in Wave 2", "Wage = $4.25 (%)",               "wage_425_2",  100),
    ("Means in Wave 2", "Wage = $5.05 (%)",               "wage_505_2",  100),
    ("Means in Wave 2", "Price of full meal",             "price2",      1),
    ("Means in Wave 2", "Hours open (weekday)",           "hrsopen2",    1),
    ("Means in Wave 2", "Recruiting bonus",               "bonus2",      100),
]

nj_mask = df["nj"] == 1   # New Jersey
pa_mask = df["nj"] == 0   # Pennsylvania

# ---------------------------------------------------------------------
# 4. Statistical analysis
# ---------------------------------------------------------------------
def means_and_t(series):
    """Mean and standard error for NJ and PA, the difference, and its
    Welch t-statistic (H0: mean_NJ = mean_PA, unequal variances)."""
    x = series[nj_mask].dropna()   # NJ observations
    y = series[pa_mask].dropna()   # PA observations

    mean_nj, mean_pa = x.mean(), y.mean()

    # Standard error of each mean (sample std. dev. / sqrt(n))
    se_nj = x.std(ddof=1) / np.sqrt(len(x))
    se_pa = y.std(ddof=1) / np.sqrt(len(y))

    # Difference and its standard error (no equal-variance assumption)
    diff    = mean_nj - mean_pa
    se_diff = np.sqrt(se_nj ** 2 + se_pa ** 2)

    # Welch t-statistic (guard against a zero-variance group, e.g. PA never
    # reports wage = $5.05 in Wave 2, so its standard error is 0)
    t = diff / se_diff if se_diff > 0 else np.nan
    return mean_nj, se_nj, mean_pa, se_pa, diff, t


rows = []
for panel, label, col, scale in VARS:
    mean_nj, se_nj, mean_pa, se_pa, diff, t = means_and_t(df[col])
    rows.append({
        "Panel":    panel,
        "Variable": label,
        "NJ_mean":  mean_nj * scale,
        "NJ_se":    se_nj   * scale,
        "PA_mean":  mean_pa * scale,
        "PA_se":    se_pa   * scale,
        "Diff":     diff    * scale,
        "t":        t,          # scale-invariant
    })

stats = pd.DataFrame(rows)

# ---------------------------------------------------------------------
# 5. Format the output table (SE shown directly below each mean)
# ---------------------------------------------------------------------
def fmt(x):
    """Round to 3 decimals and strip trailing zeros ('41.1', '21.04')."""
    s = f"{x:.3f}"
    return s.rstrip("0").rstrip(".")

table2_rows = []
for panel, group in stats.groupby("Panel", sort=False):
    # Panel header row
    table2_rows.append({"Variable": panel, "NJ": "", "PA": "", "Diff": "", "t": ""})
    for _, r in group.iterrows():
        # Mean row
        table2_rows.append({
            "Variable": r["Variable"],
            "NJ":       fmt(r["NJ_mean"]),
            "PA":       fmt(r["PA_mean"]),
            "Diff":     fmt(r["Diff"]),
            "t":        f"{r['t']:.2f}",
        })
        # Standard-error row
        table2_rows.append({
            "Variable": "",
            "NJ":       f"({fmt(r['NJ_se'])})",
            "PA":       f"({fmt(r['PA_se'])})",
            "Diff":     "",
            "t":        "",
        })

table2 = pd.DataFrame(table2_rows, columns=["Variable", "NJ", "PA", "Diff", "t"])

# ---------------------------------------------------------------------
# 6. Print a clean Markdown table
# ---------------------------------------------------------------------
md = ["| Variable | NJ | PA | Diff (NJ-PA) | t |",
      "|---|---|---|---|---|"]
for _, r in table2.iterrows():
    md.append(f"| {r['Variable']} | {r['NJ']} | {r['PA']} | {r['Diff']} | {r['t']} |")
print("\n".join(md))

# ---------------------------------------------------------------------
# 7. Export to CSV
# ---------------------------------------------------------------------
(ROOT / "output" / "tables").mkdir(parents=True, exist_ok=True)
table2.to_csv(ROOT / "output" / "tables" / "Table2.csv", index=False)
print("\nSaved:", ROOT / "output" / "tables" / "Table2.csv")

# =====================================================================
# Figure 1 — Distribution of starting wages in NJ and PA restaurants,
# before (February 1992) and after (November 1992) the minimum-wage rise.
# Matches the paper's Figure 1: grouped bars, NJ vs PA, as a percent of
# stores. $4.25 (the old minimum) is its own category; $5.05 (the new
# minimum) falls inside the "$5.00–$5.24" bin.
# =====================================================================
import matplotlib
matplotlib.use("Agg")          # non-interactive backend: write a PNG, no window
import matplotlib.pyplot as plt

# Starting-wage categories, in cents (the paper's Table 2 bins). $4.25 is
# singled out because it is the binding pre-increase minimum wage; every other
# bin is $0.25 wide. Wages are rounded to cents first so that values stored
# with float noise (e.g. 5.0500002) fall into the correct bin.
CATEGORIES = [
    ("$4.25",        425, 425),
    ("$4.26–$4.49",  426, 449),
    ("$4.50–$4.74",  450, 474),
    ("$4.75–$4.99",  475, 499),
    ("$5.00–$5.24",  500, 524),
    ("$5.25–$5.49",  525, 549),
    ("$5.50–$5.74",  550, 574),
    ("$5.75–$5.99",  575, 599),
    ("$6.00+",       600, None),
]


def _category(cents):
    """Category label for a starting wage given in cents."""
    if np.isnan(cents):
        return None                       # missing wage: not plotted
    cents = int(cents)
    for label, lo, hi in CATEGORIES:
        if hi is None or lo <= cents <= hi:
            return label
    return None                           # below $4.25 (none in the data)


def wage_dist(wave_col, mask, total):
    """Percent of stores in each wage category, over the rows in `mask`.

    The denominator is `total` = the state's full store count, so stores with
    a missing starting wage are simply excluded from the bars (matching the
    paper's Table 2, e.g. wave-1 "Wage = $4.25" = 101/331 = 30.5% for NJ)."""
    cents = (df.loc[mask, wave_col] * 100).round()
    counts = cents.map(_category).value_counts()   # drops None (missing)
    return [100.0 * counts.get(label, 0) / total for label, _, _ in CATEGORIES]


labels = [c[0] for c in CATEGORIES]
n_cat = len(CATEGORIES)
x = np.arange(n_cat)
width = 0.38

fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.0), sharey=True)

for ax, (title, wave) in zip(axes, [("Before (February 1992)", "wage_st"),
                                    ("After (November 1992)",  "wage_st2")]):
    ax.bar(x - width / 2, wage_dist(wave, nj_mask, nj_mask.sum()),
           width, color="black", label="New Jersey")
    ax.bar(x + width / 2, wage_dist(wave, pa_mask, pa_mask.sum()),
           width, color="white", edgecolor="black", hatch="//",
           label="Pennsylvania")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_xlabel("Starting wage (dollars per hour)")
    ax.set_ylim(0, 100)

axes[0].set_ylabel("Percent of stores")
axes[0].legend(loc="upper right", frameon=False)

fig.suptitle(
    "Distribution of Starting Wages in New Jersey and Pennsylvania Restaurants",
    fontweight="bold",
)
fig.tight_layout(rect=[0, 0, 1, 0.95])

fig_dir = ROOT / "output" / "figures"
fig_dir.mkdir(parents=True, exist_ok=True)
fig.savefig(fig_dir / "Figure1.png", dpi=300)
print("Saved:", fig_dir / "Figure1.png")
