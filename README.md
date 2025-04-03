# Xerberus Metrics Python SDK

A lightweight Python SDK for accessing blockchain token metrics from the Xerberus GraphQL API.

---

## Features

- Query token metrics with filters like chain, date, and address
- Sort and paginate metric data
- Access available chains and whitelisted tokens
- Auto-generated GraphQL queries
- Ready for deployment and integration

---

## Installation

```bash
pip install xerberus-metrics-sdk
```


Or clone locally for development:

```bash
git clone https://github.com/XerberusTeam/xerberus-metrics-sdk.git
cd xerberus-metrics-sdk
pip install -e .
```

## SETUP

Create a .env file in the root:

```ini
XERBERUS_API_KEY=your-api-key-here
XERBERUS_API_EMAIL=your_email@here.com
```

## USAGE

```python
from xerberus.client import XerberusMetricsClient

client = XerberusMetricsClient()

result = client.metrics_get(
    date=["2025-03-18"],
    chain=["ethereum"],
    sort_by="wallet_count",
    sort_order="DESC",
    limit=5
)

for metric in result["metrics"]:
    print(metric["token"]["symbol"], metric["wallet_count"])

```
## GraphQL Documentation
For documentation regarding the GraphQL go to:
https://xerberus.gitbook.io/documentation


## Available Metrics Fields

### Token Field Reference

These are the fields you can expect in the `token_get()` response:

| Field                      | Type     | Description                                | Sortable |
|---------------------------|----------|--------------------------------------------|----------|
| `asset_id`                | Int      | Internal asset identifier                  | ✅       |
| `symbol`                  | String   | Token Symbol                               | ✅       |
| `chain`                   | String   | Blockchain name (e.g., ETHEREUM)           | ✅       |
| `address`                 | String   | Token contract address                     | ✅       |

### Metrics Fields Reference

These are the fields you can expect in the `metrics_get()` response:


| Field                      | Type     | Description                                | Sortable |
|---------------------------|----------|--------------------------------------------|----------|
| `asset_id`                | Int      | Internal asset identifier                  | ✅       |
| `chain`                   | String   | Blockchain name (e.g., ETHEREUM)           | ✅       |
| `partition_date`          | String   | Date of the metric snapshot (YYYY-MM-DD)   | ✅       |
| `wallet_count`            | Int      | Number of wallets holding the token        | ✅       |
| `wallet_count_change_1D`  | Int      | Wallet count change over 1 day             | ✅       |
| `wallet_count_change_7D`  | Int      | Wallet count change over 7 days            | ✅       |
| `wallet_count_change_30D` | Int      | Wallet count change over 30 days           | ✅       |
| `wallet_count_change_90D` | Int      | Wallet count change over 90 days           | ✅       |
| `wallet_count_change_365D`| Int      | Wallet count change over 365 days          | ✅       |
| `typical_price`           | Float    | Average token price                        | ✅       |
| `pct_price_change_1D`     | Float    | 1-day % price change                       | ✅       |
| `price_change_7D`         | Float    | 7-day price change                         | ✅       |
| `price_change_30D`        | Float    | 30-day price change                        | ✅       |
| `price_change_90D`        | Float    | 90-day price change                        | ✅       |
| `price_change_180D`       | Float    | 180-day price change                       | ✅       |
| `price_change_365D`       | Float    | 365-day price change                       | ✅       |
| `life_cycle_v1`           | Float    | Token life cycle score                     | ✅       |
| `diversity`               | Float    | Diversity metric (wallet spread)           | ✅       |
| `dominance`               | Float    | Dominance metric                           | ✅       |
| `assortativity`           | Float    | Assortativity metric                       | ✅       |
| `risk_rating`             | String   | Xerberus Risk Rating (AAA, BB, etc.)       | ❌       |
| `risk_score`              | Float    | Xerberus Risk Score                        | ❌       |
| `token.symbol`            | String   | Token symbol (e.g., USDC, WETH)            | ❌       |
| `token.address`           | String   | Token contract address                     | ❌       |


