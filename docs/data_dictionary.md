# Data dictionary

All data is **synthetic** (made up by `scripts/generate_data.py`). The company,
depots, managers and figures are fictional. Money is in Nigerian naira (NGN).

## data/raw/sales_transactions.csv (62,700 rows before cleaning)

One row = one product sold by one depot to one channel in one week.

| Column | Meaning |
|---|---|
| InvoiceNo | Invoice number |
| WeekEnding | Last day (Sunday) of the sales week. Most rows are `yyyy-mm-dd`; about 15% are `dd/mm/yyyy` text |
| DepotID | Depot code, D01 to D50. Some rows are lower case or have extra spaces |
| SKU | Product code |
| Channel | Distributor, Retailer or Direct Project. Some rows are in CAPITALS |
| Quantity | Units sold (bags, cartons, sheets...) |
| UnitPrice_NGN | List price per unit |
| Discount | Discount as a share of list price (0.03 = 3%). About 2% of cells are blank, meaning no discount |
| UnitCost_NGN | Cost per unit |

The file also holds 300 exact duplicate rows (a double upload).

## data/raw/depots.csv (50 rows)
DepotID, DepotName, State, Region (six geopolitical zones), DepotManager, OpenedYear.

## data/raw/products.csv (12 rows)
SKU, ProductName, Category (Building Materials, Foods, Beverages), Unit.

## data/raw/monthly_targets.csv (1,200 rows)
DepotID, Month (`yyyy-mm`), Target_NGN (net revenue target for that depot and month).

## Calculated in Power Query
- **NetRevenue** = Quantity × UnitPrice_NGN × (1 − Discount)
- **GrossProfit** = NetRevenue − Quantity × UnitCost_NGN
- **Gross margin %** = GrossProfit ÷ NetRevenue
- **Target attainment %** = NetRevenue ÷ Target_NGN

## Check figures (after cleaning)
| Check | Value |
|---|---|
| Rows in SalesClean | 62,400 |
| Net revenue 2024 | ₦85.17 bn |
| Net revenue 2025 | ₦105.69 bn |
| Gross margin (both years) | 13.4% |
| Top region | South West (₦44.2 bn over two years) |
