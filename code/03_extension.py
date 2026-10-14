# =====================================================================
# 04_extension.py
# Extension — Price pass-through of the 1992 NJ minimum-wage increase.
#
# Card & Krueger (1994) found that employment did NOT fall after New Jersey
# raised its minimum wage from $4.25 to $5.05. Their leading explanation is
# that restaurants absorbed the higher labour cost by raising menu prices
# rather than by cutting employment. This script tests that channel: it
# re-runs the paper's reduced-form difference-in-differences design (the same
# five specifications as Table 4) with the change in the full-meal price as
# the outcome, and then breaks the effect down by menu item (soda, fries,
# entree).
#
# Outputs: output/tables/extension_table/TableE1_full_meal.csv
#          output/tables/extension_table/TableE2_components.csv
# =====================================================================
import numpy as np
import pandas as pd
from pathlib import Path
from statsmodels.formula.api import ols

# ---------------------------------------------------------------------
# 0. Locate the project root and load the cleaned data.
# ---------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(ROOT / "data" / "processed" / "cleaned_data.csv")

# ---------------------------------------------------------------------
# 1. Variable preparation (mirrors 02_did_analysis.py)
# ---------------------------------------------------------------------
# Chain dummies (Wendy's, chain == 4, is the omitted baseline).
df["bk"]       = (df["chain"] == 1).astype(int)
df["kfc"]      = (df["chain"] == 2).astype(int)
df["roy"]      = (df["chain"] == 3).astype(int)
df["co_owned"] = (df["co_owned"] == 1).astype(int)

nj_mask = df["nj"] == 1    # New Jersey
pa_mask = df["nj"] == 0    # Pennsylvania

# Proportional wage gap = (5.05 - W)/W, rebuilt so that NJ stores with a
# missing starting wage are NaN (the raw `gap` column wrongly sets them to 0,
# which biases the coefficient toward zero).
wage_cents = (df["wage_st"] * 100).round()
df["gap"] = np.where(
    nj_mask & (wage_cents < 505),
    (505.0 - wage_cents) / wage_cents,
    np.where(nj_mask,
             np.where(wage_cents.notna(), 0.0, np.nan),
             0.0),
)

# Full-meal price = soda + fries + entree, in each wave, and its change.
df["price1"] = df["psoda"] + df["pfry"] + df["pentree"]
df["price2"] = df["psoda2"] + df["pfry2"] + df["pentree2"]
df["delta_price"] = df["price2"] - df["price1"]

# Component-level changes (for Table E2).
df["delta_soda"]   = df["psoda2"]   - df["psoda"]
df["delta_fries"]  = df["pfry2"]    - df["pfry"]
df["delta_entree"] = df["pentree2"] - df["pentree"]

# Common sample for Table E1: stores with a full-meal price in both waves and
# a starting wage (the latter is needed for the gap specifications). This keeps
# all five columns comparable, exactly as Table 4 restricts on wage_st.
dfe = df[df["wage_st"].notna() & df["delta_price"].notna()].copy()

# ---------------------------------------------------------------------
# 2. Helpers
# ---------------------------------------------------------------------
def fmt(x):
    """Round to 3 decimals, stripping trailing zeros ('41.1', '21.04')."""
    return f"{x:.3f}".rstrip("0").rstrip(".")


def star(p):
    """Significance stars: *** p<.01, ** p<.05, * p<.10."""
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""

# ---------------------------------------------------------------------
# 3. Table E1 — full-meal price pass-through (the five Table-4 specs)
# ---------------------------------------------------------------------
specs = [
    ("(i)",   "delta_price ~ nj", "nj"),
    ("(ii)",  "delta_price ~ nj + bk + kfc + roy + co_owned", "nj"),
    ("(iii)", "delta_price ~ gap", "gap"),
    ("(iv)",  "delta_price ~ gap + bk + kfc + roy + co_owned", "gap"),
    ("(v)",   "delta_price ~ gap + bk + kfc + roy + co_owned "
              "+ southj + centralj + pa1 + pa2", "gap"),
]

# Joint F-test restrictions on the controls (classical F-test).
CONTROL_TESTS = {
    "(ii)": "bk = 0, kfc = 0, roy = 0, co_owned = 0",
    "(iv)": "bk = 0, kfc = 0, roy = 0, co_owned = 0",
    "(v)":  "bk = 0, kfc = 0, roy = 0, co_owned = 0, "
            "southj = 0, centralj = 0, pa1 = 0, pa2 = 0",
}

res_store = {}
for name, spec, key in specs:
    res = ols(spec, data=dfe).fit()          # classical (homoskedastic) SEs
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

tableE1_rows = []
# New Jersey dummy -> models (i) and (ii)
row = {"Regressor": "New Jersey dummy"}
for n in model_cols:
    row[n] = (f"{fmt(res_store[n]['coef'])}{star(res_store[n]['p'])}"
              if n in ("(i)", "(ii)") else "")
tableE1_rows.append(row)
row = {"Regressor": ""}
for n in model_cols:
    row[n] = f"({fmt(res_store[n]['se'])})" if n in ("(i)", "(ii)") else ""
tableE1_rows.append(row)

# Gap -> models (iii), (iv), (v)
row = {"Regressor": "Gap (proportional increase)"}
for n in model_cols:
    row[n] = (f"{fmt(res_store[n]['coef'])}{star(res_store[n]['p'])}"
              if n in ("(iii)", "(iv)", "(v)") else "")
tableE1_rows.append(row)
row = {"Regressor": ""}
for n in model_cols:
    row[n] = f"({fmt(res_store[n]['se'])})" if n in ("(iii)", "(iv)", "(v)") else ""
tableE1_rows.append(row)

tableE1_rows.append({"Regressor": "Chain & ownership controls",
                     **{n: ("Yes" if n in ("(ii)", "(iv)", "(v)") else "No")
                        for n in model_cols}})
tableE1_rows.append({"Regressor": "Region controls",
                     **{n: ("Yes" if n == "(v)" else "No")
                        for n in model_cols}})
tableE1_rows.append({"Regressor": "Standard error of regression",
                     **{n: fmt(res_store[n]["ser"]) for n in model_cols}})
tableE1_rows.append({"Regressor": "Probability value for controls",
                     **{n: (fmt(res_store[n]["p_ctrl"])
                            if res_store[n]["p_ctrl"] is not None else "")
                        for n in model_cols}})

tableE1 = pd.DataFrame(tableE1_rows, columns=["Regressor"] + model_cols)

# ---------------------------------------------------------------------
# 4. Table E2 — pass-through by menu item (NJ dummy, with/without controls)
# ---------------------------------------------------------------------
components = [
    ("Full meal", "delta_price"),
    ("Soda",      "delta_soda"),
    ("Fries",     "delta_fries"),
    ("Entree",    "delta_entree"),
]


def nj_effect(outcome, with_controls):
    """NJ dummy coefficient (and SE/p) on a price-change outcome."""
    spec = (f"{outcome} ~ nj + bk + kfc + roy + co_owned"
            if with_controls else f"{outcome} ~ nj")
    res = ols(spec, data=df).fit()
    return res.params["nj"], res.bse["nj"], res.pvalues["nj"]


tableE2_rows = []
for label, outcome in components:
    c0, s0, p0 = nj_effect(outcome, with_controls=False)
    c1, s1, p1 = nj_effect(outcome, with_controls=True)
    tableE2_rows.append({"Menu item": label,
                         "(i) no controls": f"{fmt(c0)}{star(p0)}",
                         "(ii) with controls": f"{fmt(c1)}{star(p1)}"})
    tableE2_rows.append({"Menu item": "",
                         "(i) no controls": f"({fmt(s0)})",
                         "(ii) with controls": f"({fmt(s1)})"})

tableE2 = pd.DataFrame(tableE2_rows)

# ---------------------------------------------------------------------
# 5. Print clean Markdown tables
# ---------------------------------------------------------------------
def to_md(frame, first_col):
    cols = [first_col] + [c for c in frame.columns if c != first_col]
    lines = ["| " + " | ".join(cols) + " |",
             "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in frame.iterrows():
        cells = [str(r[c]).replace("\n", "<br>") for c in cols]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


print("## Table E1: Price pass-through of the minimum-wage increase "
      "(full meal)\n")
print(to_md(tableE1, "Regressor"))
print("\n## Table E2: Price pass-through by menu item (NJ dummy)\n")
print(to_md(tableE2, "Menu item"))
print(f"\nSample size (Table E1): {len(dfe)} stores "
      f"(NJ {(dfe['nj'] == 1).sum()}, PA {(dfe['nj'] == 0).sum()}).")

# ---------------------------------------------------------------------
# 6. Export to CSV
# ---------------------------------------------------------------------
out = ROOT / "output" / "tables" / "extension_table"
out.mkdir(parents=True, exist_ok=True)
tableE1.to_csv(out / "TableE1_full_meal.csv", index=False)
tableE2.to_csv(out / "TableE2_components.csv", index=False)
print("\nSaved:", out / "TableE1_full_meal.csv")
print("Saved:", out / "TableE2_components.csv")
