# =====================================================================
# 02_did_analysis.py
# Tables 3 & 4 — Card & Krueger (1994), "Minimum Wages and Employment"
#   Table 3: Average employment per store (difference-in-differences)
#   Table 4: Reduced-form models for the change in FTE employment
#
# Outputs: output/tables/Table3.csv and output/tables/Table4.csv
# =====================================================================
import numpy as np
import pandas as pd
from pathlib import Path
from statsmodels.formula.api import ols

# ---------------------------------------------------------------------
# 0. Locate the project root (works from any working directory).
#    `__file__` is this script's absolute path, so `parent.parent` is
#    the project root even when the script is launched from elsewhere.
# ---------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(ROOT / "data" / "processed" / "cleaned_data.csv")

# ---------------------------------------------------------------------
# 1. Variable preparation
# ---------------------------------------------------------------------
# Chain dummies (Wendy's, chain == 4, is the omitted baseline)
df["bk"]       = (df["chain"] == 1).astype(int)
df["kfc"]      = (df["chain"] == 2).astype(int)
df["roy"]      = (df["chain"] == 3).astype(int)
df["co_owned"] = (df["co_owned"] == 1).astype(int)

nj_mask = df["nj"] == 1    # New Jersey
pa_mask = df["nj"] == 0    # Pennsylvania

# NJ wage groups defined on the Wave-1 starting wage.
# wage_st is a Stata 'float', so cents like 4.99 may be stored as 4.9899998;
# multiplying by 100 and rounding makes the group boundaries exact. Kept as
# float so missing wages stay NaN (NaN comparisons are naturally False below).
wage_cents = (df["wage_st"] * 100).round()
low  = nj_mask & (wage_cents == 425)               # wage_st == 4.25
mid  = nj_mask & wage_cents.between(426, 499)      # 4.26 <= wage_st <= 4.99
high = nj_mask & (wage_cents >= 500)               # wage_st >= 5.00

# Proportional wage gap = (5.05 - W)/W.
#   - NJ stores below $5.05: proportional increase needed to reach $5.05
#   - NJ stores at/above $5.05: 0 (no increase needed)
#   - NJ stores with a missing starting wage: missing (excluded)
#   - PA stores: 0 (no minimum-wage increase)
# NOTE: the raw `gap` column from 00_clean_data.do assigns 0 (instead of
# missing) to NJ stores with a missing starting wage, which wrongly counts
# them as "no treatment" and biases the gap coefficient down (~12.5 vs the
# paper's ~15.7). Rebuilding gap with missing -> NaN reproduces the paper.
gap = np.where(
    nj_mask & (wage_cents < 505),
    (505.0 - wage_cents) / wage_cents,
    np.where(nj_mask,
             np.where(wage_cents.notna(), 0.0, np.nan),
             0.0),
)
df["gap"] = gap

# FTE change is already in the cleaned data (see 00_clean_data.do):
#   fte2 = 0 for permanently closed stores, missing for temporarily closed
#   stores, then delta_fte = fte2 - fte1. So delta_fte excludes temporarily
#   closed stores (NaN) and treats permanent closures as employment -> 0.
#
# `fte2_temp0` is fte2 with temporarily closed stores set to 0 (instead of
# missing); `change_fte_temp0 = fte2_temp0 - fte1` then treats those closures
# as employment falling to zero (the paper's "temporarily closed = 0" row).
df["fte2_temp0"] = df["fte2"].where(df["temp_closed"] != 1, 0.0)
df["change_fte_temp0"] = df["fte2_temp0"] - df["fte1"]

# (The Table 3 statistics — columns of the transposed table — are defined
# as COLUMNS in Section 3.)

# ---------------------------------------------------------------------
# 2. Helpers
# ---------------------------------------------------------------------
def mean_se(series, mask):
    """Mean and standard error of `series` over the rows in `mask`."""
    x = series[mask].dropna()
    return x.mean(), x.std(ddof=1) / np.sqrt(len(x))


def diff_mean_se(m1, se1, m2, se2):
    """Difference of two independent means and its SE (unequal variances)."""
    d = m1 - m2
    sed = np.sqrt(se1 ** 2 + se2 ** 2)
    return d, sed


def change_mean_se(mask):
    """Mean and SE of 'change in mean FTE employment' = mean(fte2) - mean(fte1),
    using all available observations in each wave and the store-level
    correlation between the two waves (overlapping panel)."""
    fte1 = df.loc[mask, "fte1"].dropna()
    fte2 = df.loc[mask, "fte2"].dropna()
    both = df.loc[mask, ["fte1", "fte2"]].dropna()
    m = fte2.mean() - fte1.mean()
    se1 = fte1.std(ddof=1) / np.sqrt(len(fte1))
    se2 = fte2.std(ddof=1) / np.sqrt(len(fte2))
    r = both["fte1"].corr(both["fte2"])
    se = np.sqrt(se1 ** 2 + se2 ** 2 - 2 * r * se1 * se2)
    return m, se


def fmt(x):
    """Round to 3 decimals, stripping trailing zeros ('41.1', '21.04')."""
    return f"{x:.3f}".rstrip("0").rstrip(".")

# ---------------------------------------------------------------------
# 3. Table 3 — average employment per store (DiD), transposed.
#    Rows = store groups, columns = the paper's five statistics (in order):
#    before, after, change in mean FTE employment, balanced sample, and the
#    change with temporarily closed stores set to 0. Each cell shows
#    "Mean\n(SE)"; the three difference rows are the difference of the two
#    group means.
# ---------------------------------------------------------------------
COLUMNS = ["FTE_before",
           "FTE_after",
           "Change in mean FTE employment",
           "Balanced sample",
           "Change_FTE_Temp0"]


def stat_values(mask):
    """{column: (mean, se)} for the five Table 3 statistics over `mask`."""
    return {
        "FTE_before":                    mean_se(df["fte1"], mask),
        "FTE_after":                     mean_se(df["fte2"], mask),
        "Change in mean FTE employment": change_mean_se(mask),
        "Balanced sample":               mean_se(df["delta_fte"], mask),
        "Change_FTE_Temp0":              mean_se(df["change_fte_temp0"], mask),
    }


groups = [
    ("PA",                  "group", (pa_mask,)),
    ("NJ",                  "group", (nj_mask,)),
    ("Difference, NJ - PA", "diff",  (nj_mask, pa_mask)),
    ("Wage = $4.25",        "group", (low,)),
    ("Wage = $4.26-$4.99",  "group", (mid,)),
    ("Wage >= $5.00",       "group", (high,)),
    ("Low-high",            "diff",  (low, high)),
    ("Midrange-high",       "diff",  (mid, high)),
]

table3 = pd.DataFrame(index=[label for label, _, _ in groups],
                      columns=COLUMNS, dtype=object)
table3.index.name = "Group"

for label, kind, args in groups:
    if kind == "group":
        for name, (m, se) in stat_values(args[0]).items():
            table3.loc[label, name] = f"{fmt(m)}\n({fmt(se)})"
    else:  # difference of two independent group means
        v1 = stat_values(args[0])
        v2 = stat_values(args[1])
        for name in COLUMNS:
            d, sed = diff_mean_se(v1[name][0], v1[name][1],
                                  v2[name][0], v2[name][1])
            table3.loc[label, name] = f"{fmt(d)}\n({fmt(sed)})"

table3 = table3.reset_index()

# ---------------------------------------------------------------------
# 4. Table 4 — reduced-form OLS for the change in FTE employment.
#    Sample = stores with employment AND starting-wage data in both waves
#    (the paper's N = 357; this public file gives 365). Classical OLS
#    standard errors, plus the standard error of regression (SER) and the
#    joint F-test p-value for the controls.
# ---------------------------------------------------------------------
df4 = df[df["wage_st"].notna()].copy()

specs = [
    ("(i)",   "delta_fte ~ nj", "nj"),
    ("(ii)",  "delta_fte ~ nj + bk + kfc + roy + co_owned", "nj"),
    ("(iii)", "delta_fte ~ gap", "gap"),
    ("(iv)",  "delta_fte ~ gap + bk + kfc + roy + co_owned", "gap"),
    ("(v)",   "delta_fte ~ gap + bk + kfc + roy + co_owned "
              "+ southj + centralj + pa1 + pa2", "gap"),
]

# Joint F-test restrictions on the controls (classical F-test).
CONTROL_TESTS = {
    "(ii)": "bk = 0, kfc = 0, roy = 0, co_owned = 0",
    "(iv)": "bk = 0, kfc = 0, roy = 0, co_owned = 0",
    "(v)":  "bk = 0, kfc = 0, roy = 0, co_owned = 0, "
            "southj = 0, centralj = 0, pa1 = 0, pa2 = 0",
}


def star(p):
    """Significance stars: *** p<.01, ** p<.05, * p<.10."""
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


res_store = {}
for name, spec, key in specs:
    res = ols(spec, data=df4).fit()          # classical (homoskedastic) SEs
    p_ctrl = None
    if name in CONTROL_TESTS:
        ft = res.f_test(CONTROL_TESTS[name])
        p_ctrl = float(np.asarray(ft.pvalue).reshape(-1)[0])
    res_store[name] = {
        "coef":   res.params[key],
        "se":     res.bse[key],
        "p":      res.pvalues[key],
        "ser":    np.sqrt(res.mse_resid),
        "p_ctrl": p_ctrl,
    }

model_cols = [n for n, _, _ in specs]

table4_rows = []
# New Jersey dummy -> models (i) and (ii)
row = {"Regressor": "New Jersey dummy"}
for n in model_cols:
    row[n] = (f"{fmt(res_store[n]['coef'])}{star(res_store[n]['p'])}"
              if n in ("(i)", "(ii)") else "")
table4_rows.append(row)
row = {"Regressor": ""}
for n in model_cols:
    row[n] = f"({fmt(res_store[n]['se'])})" if n in ("(i)", "(ii)") else ""
table4_rows.append(row)

# Gap -> models (iii), (iv), (v)
row = {"Regressor": "Gap (proportional increase)"}
for n in model_cols:
    row[n] = (f"{fmt(res_store[n]['coef'])}{star(res_store[n]['p'])}"
              if n in ("(iii)", "(iv)", "(v)") else "")
table4_rows.append(row)
row = {"Regressor": ""}
for n in model_cols:
    row[n] = f"({fmt(res_store[n]['se'])})" if n in ("(iii)", "(iv)", "(v)") else ""
table4_rows.append(row)

# Control indicators
table4_rows.append({"Regressor": "Chain & ownership controls",
                    **{n: ("Yes" if n in ("(ii)", "(iv)", "(v)") else "No")
                       for n in model_cols}})
table4_rows.append({"Regressor": "Region controls",
                    **{n: ("Yes" if n == "(v)" else "No")
                       for n in model_cols}})
# Standard error of regression (SER)
table4_rows.append({"Regressor": "Standard error of regression",
                    **{n: fmt(res_store[n]["ser"]) for n in model_cols}})
# Probability value for controls (joint F-test)
table4_rows.append({"Regressor": "Probability value for controls",
                    **{n: (fmt(res_store[n]["p_ctrl"])
                           if res_store[n]["p_ctrl"] is not None else "")
                       for n in model_cols}})

table4 = pd.DataFrame(table4_rows, columns=["Regressor"] + model_cols)

# ---------------------------------------------------------------------
# 5. Print clean Markdown tables
# ---------------------------------------------------------------------
def to_md(frame, first_col):
    cols = [first_col] + [c for c in frame.columns if c != first_col]
    lines = ["| " + " | ".join(cols) + " |",
             "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in frame.iterrows():
        # `\n` -> `<br>` so multi-line cells ("Mean\n(SE)") render as two
        # lines inside a single Markdown table cell.
        cells = [str(r[c]).replace("\n", "<br>") for c in cols]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


print("## Table 3: Average employment per store (difference-in-differences)\n")
print(to_md(table3, "Group"))
print("\n## Table 4: Reduced-form models for change in FTE employment\n")
print(to_md(table4, "Regressor"))

# ---------------------------------------------------------------------
# 6. Export to CSV
# ---------------------------------------------------------------------
out = ROOT / "output" / "tables"
out.mkdir(parents=True, exist_ok=True)
table3.to_csv(out / "Table3.csv", index=False)
table4.to_csv(out / "Table4.csv", index=False)
print("\nSaved:", out / "Table3.csv")
print("Saved:", out / "Table4.csv")
