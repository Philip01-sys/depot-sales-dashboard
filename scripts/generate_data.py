"""Generate the synthetic depot sales data used in this project.

The company, depots, managers and figures are all made up. The data copies the
shape of a real weekly depot sales report (many depots, many products, weekly
volumes, monthly targets) and includes a few common data-quality problems so the
cleaning steps in Power Query have something to fix.

Run:  python scripts/generate_data.py   (needs pandas and numpy)
"""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)
OUT = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

# ---- Depots: 50 depots in six regions ---------------------------------------
depot_rows = [
    # city, state, region
    ("Abuja Central", "FCT", "North Central"), ("Kubwa", "FCT", "North Central"),
    ("Lokoja", "Kogi", "North Central"), ("Makurdi", "Benue", "North Central"),
    ("Jos", "Plateau", "North Central"), ("Lafia", "Nasarawa", "North Central"),
    ("Minna", "Niger", "North Central"), ("Ilorin", "Kwara", "North Central"),
    ("Kano", "Kano", "North West"), ("Kano Sharada", "Kano", "North West"),
    ("Kaduna", "Kaduna", "North West"), ("Zaria", "Kaduna", "North West"),
    ("Katsina", "Katsina", "North West"), ("Sokoto", "Sokoto", "North West"),
    ("Gusau", "Zamfara", "North West"), ("Birnin Kebbi", "Kebbi", "North West"),
    ("Dutse", "Jigawa", "North West"),
    ("Maiduguri", "Borno", "North East"), ("Yola", "Adamawa", "North East"),
    ("Bauchi", "Bauchi", "North East"), ("Gombe", "Gombe", "North East"),
    ("Jalingo", "Taraba", "North East"), ("Damaturu", "Yobe", "North East"),
    ("Lagos Apapa", "Lagos", "South West"), ("Lagos Ikeja", "Lagos", "South West"),
    ("Lagos Lekki", "Lagos", "South West"), ("Ikorodu", "Lagos", "South West"),
    ("Ibadan", "Oyo", "South West"), ("Ogbomoso", "Oyo", "South West"),
    ("Abeokuta", "Ogun", "South West"), ("Sagamu", "Ogun", "South West"),
    ("Akure", "Ondo", "South West"), ("Osogbo", "Osun", "South West"),
    ("Ado Ekiti", "Ekiti", "South West"),
    ("Onitsha", "Anambra", "South East"), ("Awka", "Anambra", "South East"),
    ("Enugu", "Enugu", "South East"), ("Aba", "Abia", "South East"),
    ("Umuahia", "Abia", "South East"), ("Owerri", "Imo", "South East"),
    ("Abakaliki", "Ebonyi", "South East"),
    ("Port Harcourt", "Rivers", "South South"), ("Onne", "Rivers", "South South"),
    ("Warri", "Delta", "South South"), ("Asaba", "Delta", "South South"),
    ("Benin City", "Edo", "South South"), ("Uyo", "Akwa Ibom", "South South"),
    ("Calabar", "Cross River", "South South"), ("Yenagoa", "Bayelsa", "South South"),
    ("Eket", "Akwa Ibom", "South South"),
]
assert len(depot_rows) == 50

first = ["Amina", "Chinedu", "Tunde", "Ngozi", "Ibrahim", "Funke", "Emeka", "Halima",
         "Segun", "Blessing", "Musa", "Adaeze", "Yusuf", "Kemi", "Obinna", "Zainab",
         "Femi", "Uche", "Aisha", "Gbenga", "Ifeoma", "Sani", "Bisi", "Kelechi", "Hauwa"]
last = ["Bello", "Okafor", "Adeyemi", "Eze", "Abubakar", "Ogunleye", "Nwosu", "Lawal",
        "Okonkwo", "Danjuma", "Afolabi", "Umeh", "Garba", "Olatunji", "Ibe", "Yakubu"]

depots = pd.DataFrame({
    "DepotID": [f"D{i:02d}" for i in range(1, 51)],
    "DepotName": [r[0] for r in depot_rows],
    "State": [r[1] for r in depot_rows],
    "Region": [r[2] for r in depot_rows],
    "DepotManager": [f"{rng.choice(first)} {rng.choice(last)}" for _ in range(50)],
    "OpenedYear": rng.integers(2008, 2022, 50),
})
# Depot size drives volume; Lagos, Kano, Abuja, Port Harcourt, Onitsha are big.
size = rng.lognormal(0, 0.35, 50)
for big in ["Lagos Apapa", "Lagos Ikeja", "Kano", "Abuja Central", "Port Harcourt", "Onitsha"]:
    size[depots.index[depots.DepotName == big][0]] *= 1.9
depots["_size"] = size

# ---- Products ------------------------------------------------------------------
# price = list price per unit in Jan 2024 (NGN); margin = gross margin share
products = pd.DataFrame([
    ("SKU101", "Cement 42.5R 50kg", "Building Materials", "Bag", 8200, 0.18, 900),
    ("SKU102", "Cement 32.5N 50kg", "Building Materials", "Bag", 7600, 0.17, 650),
    ("SKU103", "Roofing Sheet 0.45mm", "Building Materials", "Sheet", 6500, 0.22, 120),
    ("SKU104", "Emulsion Paint 20L", "Building Materials", "Bucket", 28000, 0.27, 35),
    ("SKU201", "Granulated Sugar 50kg", "Foods", "Bag", 78000, 0.09, 40),
    ("SKU202", "Cube Sugar 24 pack", "Foods", "Carton", 21000, 0.14, 60),
    ("SKU203", "Wheat Flour 50kg", "Foods", "Bag", 62000, 0.10, 45),
    ("SKU204", "Semolina 10kg", "Foods", "Bag", 14500, 0.15, 70),
    ("SKU205", "Spaghetti 500g x 20", "Foods", "Carton", 17500, 0.16, 90),
    ("SKU206", "Table Salt 500g x 40", "Foods", "Carton", 9800, 0.20, 75),
    ("SKU301", "Bottled Water 75cl x 12", "Beverages", "Pack", 2200, 0.25, 220),
    ("SKU302", "Malt Drink 33cl x 24", "Beverages", "Crate", 11500, 0.19, 85),
], columns=["SKU", "ProductName", "Category", "Unit", "_price", "_margin", "_base_units"])

# ---- Weekly sales, Jan 2024 - Dec 2025 ----------------------------------------
weeks = pd.date_range("2024-01-07", "2025-12-28", freq="W-SUN")  # week ending Sunday
n_w = len(weeks)

month = weeks.month.values
# Building materials slow in the rainy season (Jun-Sep), strong in the dry season.
season_build = np.where(np.isin(month, [6, 7, 8, 9]), 0.72,
                        np.where(np.isin(month, [11, 12, 1, 2, 3]), 1.15, 1.0))
# Foods and beverages peak in December and around Ramadan (Mar 2024, Feb-Mar 2025).
season_food = np.where(month == 12, 1.30, 1.0)
ramadan = ((weeks >= "2024-03-10") & (weeks <= "2024-04-14")) | \
          ((weeks >= "2025-02-28") & (weeks <= "2025-04-03"))
season_food = season_food * np.where(ramadan, 1.18, 1.0)
season_bev = np.where(np.isin(month, [2, 3, 4, 12]), 1.20, 1.0)

# Prices rise with inflation: about 2.2% a month in 2024, 1.2% a month in 2025.
months_since = (weeks.year.values - 2024) * 12 + month - 1
infl = np.where(months_since < 12, 1.022 ** months_since,
                1.022 ** 12 * 1.012 ** (months_since - 12))
# Volume growth is weak in 2024 (high prices) and recovers in 2025.
vol_trend = np.where(months_since < 12, 1 - 0.006 * months_since,
                     0.934 + 0.009 * (months_since - 12))

# Story depots: two decline in 2025, one grows fast after a 2025 expansion.
decline = {"D17": 0.62, "D22": 0.70}
growth = {"D30": 1.45}
# Region mix: north buys more foods, south more building materials.
region_bias = {
    "North Central": {"Building Materials": 1.0, "Foods": 1.0, "Beverages": 1.0},
    "North West": {"Building Materials": 0.8, "Foods": 1.25, "Beverages": 0.9},
    "North East": {"Building Materials": 0.75, "Foods": 1.15, "Beverages": 0.8},
    "South West": {"Building Materials": 1.2, "Foods": 0.95, "Beverages": 1.2},
    "South East": {"Building Materials": 1.15, "Foods": 0.9, "Beverages": 1.05},
    "South South": {"Building Materials": 1.1, "Foods": 0.9, "Beverages": 1.1},
}
channels = ["Distributor", "Retailer", "Direct Project"]

rows = []
inv = 100000
for _, d in depots.iterrows():
    dep_mult = np.ones(n_w)
    if d.DepotID in decline:
        dep_mult = np.where(weeks.year == 2025, decline[d.DepotID], 1.0)
    if d.DepotID in growth:
        dep_mult = np.where(weeks >= "2025-04-01", growth[d.DepotID], 1.0)
    for _, p in products.iterrows():
        seas = {"Building Materials": season_build, "Foods": season_food,
                "Beverages": season_bev}[p.Category]
        mean_units = (p._base_units * d._size * region_bias[d.Region][p.Category]
                      * seas * vol_trend * dep_mult)
        units = rng.poisson(np.maximum(mean_units, 0.5))
        price = np.round(p._price * infl * rng.normal(1, 0.015, n_w), -1)
        disc = np.clip(rng.normal(0.03, 0.02, n_w), 0, 0.10).round(3)
        chan = rng.choice(channels, n_w, p=[0.55, 0.35, 0.10]
                          if p.Category == "Building Materials" else [0.6, 0.4, 0.0])
        for i in range(n_w):
            if units[i] == 0:
                continue
            inv += 1
            rows.append((f"INV{inv}", weeks[i], d.DepotID, p.SKU, chan[i],
                         int(units[i]), int(price[i]), float(disc[i])))

sales = pd.DataFrame(rows, columns=["InvoiceNo", "WeekEnding", "DepotID", "SKU",
                                    "Channel", "Quantity", "UnitPrice_NGN", "Discount"])
cost_share = 1 - products.set_index("SKU")._margin
sales["UnitCost_NGN"] = (sales.UnitPrice_NGN * sales.SKU.map(cost_share)
                         * rng.normal(1, 0.01, len(sales))).round(-1).astype(int)

# ---- Monthly revenue targets per depot ------------------------------------------
net = sales.Quantity * sales.UnitPrice_NGN * (1 - sales.Discount)
m = sales.assign(Month=sales.WeekEnding.dt.to_period("M"), Net=net)
by_dm = m.groupby(["DepotID", "Month"]).Net.sum().reset_index()
# Targets come from each depot's 2024 average month, with a seasonal plan, a
# planned 2025 uplift and a depot-level stretch, so some depots beat target
# and some miss.
plan = by_dm.DepotID.map(by_dm[by_dm.Month.dt.year == 2024].groupby("DepotID").Net.mean())
stretch = by_dm.DepotID.map(dict(zip(depots.DepotID, rng.normal(1.0, 0.06, 50))))
by_dm["Target_NGN"] = (plan * by_dm.Month.dt.month.map(
    {1: 1.02, 2: 1.0, 3: 1.04, 4: 1.0, 5: 0.98, 6: 0.9, 7: 0.86, 8: 0.86, 9: 0.92,
     10: 1.0, 11: 1.06, 12: 1.18})
    * np.where(by_dm.Month.dt.year == 2025, 1.22, 1.0) * stretch
    * rng.normal(1, 0.03, len(by_dm))).round(-4).astype(int)
targets = by_dm.assign(Month=by_dm.Month.dt.strftime("%Y-%m"))[
    ["DepotID", "Month", "Target_NGN"]]

# ---- Add realistic data-quality problems to the sales file ------------------------
sales = sales.sample(frac=1, random_state=7).reset_index(drop=True)
n = len(sales)
# 1. Mixed date formats (some exported as text dd/mm/yyyy)
dates = sales.WeekEnding.dt.strftime("%Y-%m-%d")
mask = rng.random(n) < 0.15
dates[mask] = sales.WeekEnding[mask].dt.strftime("%d/%m/%Y")
sales["WeekEnding"] = dates
# 2. Depot IDs typed in lower case or with spaces
mask = rng.random(n) < 0.03
sales.loc[mask, "DepotID"] = sales.loc[mask, "DepotID"].str.lower()
mask = rng.random(n) < 0.02
sales.loc[mask, "DepotID"] = " " + sales.loc[mask, "DepotID"] + " "
# 3. Channel spelling varies
mask = rng.random(n) < 0.04
sales.loc[mask, "Channel"] = sales.loc[mask, "Channel"].str.upper()
# 4. Blank discount cells (should be 0)
sales["Discount"] = sales.Discount.astype(object)
sales.loc[rng.random(n) < 0.02, "Discount"] = None
# 5. Exact duplicate rows from a double upload
dups = sales.sample(300, random_state=11)
sales = pd.concat([sales, dups]).sample(frac=1, random_state=3).reset_index(drop=True)

sales.to_csv(OUT / "sales_transactions.csv", index=False)
depots.drop(columns="_size").to_csv(OUT / "depots.csv", index=False)
products[["SKU", "ProductName", "Category", "Unit"]].to_csv(OUT / "products.csv", index=False)
targets.to_csv(OUT / "monthly_targets.csv", index=False)
print(f"sales rows: {len(sales):,} | depots: {len(depots)} | products: {len(products)}"
      f" | target rows: {len(targets):,}")
