---
name: dune
description: Query and analyze blockchain data using Dune Analytics Python SDK. Supports multi-chain data analysis with SQL queries.
---

# Dune Analytics

AI agent skill for querying blockchain data using Dune Analytics Python SDK.

## Overview

- **SDK**: `dune-client` - Official Python client for Dune Analytics API
- **SQL Dialect**: Dune SQL (based on Trino SQL syntax)
- **Data**: Multi-chain blockchain data (Ethereum, Polygon, Arbitrum, Optimism, Base, etc.)

## Setup

### Installation
```bash
pip install dune-client python-dotenv
```

### Authentication

**IMPORTANT**: Always set your DUNE_API_KEY in a `.env` file. Never hardcode it in your Python code.

Create a `.env` file in your project root:
```
DUNE_API_KEY=your_api_key_here
```

The DuneClient will automatically read from your environment - no need to pass the key in your Python code.

## Usage

**Important:** For ad-hoc data queries, use `run_sql()` to avoid creating saved queries in your Dune account. Only use `create_query()` when you need parameterized queries or want to save queries for reuse.

### Run Query by ID
Execute existing Dune query by query_id:

```python
from dune_client.client import DuneClient
from dune_client.query import QueryBase
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize client (reads DUNE_API_KEY from env)
dune = DuneClient()

# Run existing query (uses execution credits)
query = QueryBase(query_id=1215383)
results = dune.run_query(query)

# Or get cached results (only uses credits if cache is older than max_age_hours)
# If results exist and are fresh, no credits used. If too old, automatically re-executes.
results = dune.get_latest_result(1215383, max_age_hours=8)
```

### Run Query with Parameters
```python
from dune_client.types import QueryParameter

query = QueryBase(
    query_id=1215383,
    params=[
        QueryParameter.text_type(name="Blockchain", value="ethereum"),
        QueryParameter.number_type(name="Limit", value=100),
        QueryParameter.date_type(name="StartDate", value="2024-01-01 00:00:00"),
    ]
)
results = dune.run_query(query)
```

### Run Custom SQL Query (Without Saving)
**Recommended for ad-hoc queries** - Executes SQL without creating saved queries in your Dune account:

```python
sql = """
SELECT
  blockchain,
  COUNT(*) as transfer_count
FROM tokens.transfers
WHERE block_time >= NOW() - INTERVAL '7' DAY
GROUP BY blockchain
ORDER BY transfer_count DESC
LIMIT 10
"""

# Execute SQL directly (no saved query created)
results = dune.run_sql(query_sql=sql)
```

**Note:** `run_sql()` does not support parameterized queries. If you need parameters, use the saved query approach below.

### Create and Run Saved Query (With Parameters)
**Use only when you need parameterized queries:**

```python
sql = """
SELECT
  blockchain,
  COUNT(*) as transfer_count
FROM tokens.transfers
WHERE block_time >= NOW() - INTERVAL '7' DAY
GROUP BY blockchain
ORDER BY transfer_count DESC
LIMIT {{Limit}}
"""

# This creates a saved query in your Dune account
query = dune.create_query(
    name="Token Transfers by Chain",
    query_sql=sql,
    params=[QueryParameter.number_type(name="Limit", value=10)]
)

# Run it
results = dune.run_query(query.base)
```

### Output Formats
```python
# For run_sql() - JSON format only
results = dune.run_sql(query_sql=sql)

# For saved queries - multiple formats available:
# JSON (default)
results = dune.run_query(query)

# CSV
results_csv = dune.run_query_csv(query)

# Pandas DataFrame (requires pandas installed)
results_df = dune.run_query_dataframe(query)
```

## When to Use Each Query Method

### Use `run_sql()` for:
- ✅ Ad-hoc data queries and exploration
- ✅ One-time analysis
- ✅ Simple queries without parameters
- ✅ **Recommended default for most use cases**

### Use `create_query()` + `run_query()` for:
- ✅ Parameterized queries (with `{{Parameter}}` syntax)
- ✅ Queries you want to save and reuse
- ✅ Queries you want to share with others
- ✅ Building dashboards or reference materials

### Use `run_query()` with query_id for:
- ✅ Executing existing saved queries
- ✅ Re-running queries with different parameters

### Use `get_latest_result()` for:
- ✅ Getting cached query results when available (saves execution credits)
- ✅ Automatically re-executing if cache is too old (controlled by `max_age_hours`)
- ✅ Best for queries that don't need real-time data

**⚠️ IMPORTANT - Download Credits:**
`get_latest_result()` and `run_query()` both cost **download credits** when retrieving large datasets. For large queries:
- **DO NOT** download entire result sets
- **Instead:** Reference the query in your own SQL (`FROM query_xxxxx`)
- **Best practice:**
  1. First count rows: `SELECT COUNT(*) FROM query_xxxxx`
  2. If small (<1000 rows), safe to download with `get_latest_result()`
  3. If large, use as subquery with `LIMIT`, filters, or aggregations
  4. Return only statistics/aggregated data instead of raw rows

```python
# ❌ BAD: Downloads 50,000+ rows (costs many download credits)
results = dune.get_latest_result(6509358)

# ✅ GOOD: Check size first
count_sql = "SELECT COUNT(*) as total FROM query_6509358"
count = dune.run_sql(query_sql=count_sql)

# ✅ GOOD: Use as subquery with filters and limits
filtered_sql = """
SELECT address, label
FROM query_6509358
WHERE label = 'Binance'
LIMIT 100
"""
results = dune.run_sql(query_sql=filtered_sql)

# ✅ GOOD: Aggregate instead of downloading raw data
stats_sql = """
SELECT
  label,
  COUNT(*) as address_count
FROM query_6509358
GROUP BY label
ORDER BY address_count DESC
"""
results = dune.run_sql(query_sql=stats_sql)
```

## SQL Best Practices

- **ALWAYS check references FIRST**: Before writing SQL for any table, check the `references/` directory for table-specific documentation. This provides accurate column names, data types, and example queries.
- **⚠️ Avoid downloading large datasets**: Downloading query results costs download credits. Always count rows first, use `LIMIT`, or aggregate data before downloading. Reference large queries as subqueries (`FROM query_xxxxx`) instead of downloading all rows.
- **Filter by time (when available)**: For tables with time columns like `block_time`, add date range filters to improve performance (e.g., `WHERE block_time >= DATE '2024-01-01'` or `WHERE block_time >= NOW() - INTERVAL '7' DAY`)
- **Use LIMIT**: Start with small limits when exploring data
- **Narrow scope first**: Begin with specific filters, expand as needed

## Usage Guides

Purpose-driven guides for common blockchain data analysis tasks:

- [Bitcoin Addresses and Entities](references/bitcoin-address-label.md) - Label and categorize bitcoin addresses

## Table References

**IMPORTANT**: Before writing SQL queries for any table, always check its reference documentation in the `references/` directory. These files contain:
- Accurate column names and data types
- Table schemas and descriptions
- Example queries and best practices
- Performance optimization tips

Available references:
- [bitcoin.inputs](references/bitcoin-inputs.md) - Bitcoin transaction inputs spending previous outputs with coinbase data
- [bitcoin.outputs](references/bitcoin-outputs.md) - Bitcoin transaction outputs (UTXOs) with block and script data
- [dex.trades](references/dex-trades.md) - Decentralized exchange trades across 40+ blockchains and protocols
- [tokens.transfers](references/tokens-transfers.md) - Token transfer events across chains
- [labels.ens](references/labels-ens.md) - Ethereum Name Service (ENS) domain labels (EVM chains only, excludes Bitcoin)
- [labels.owner_addresses](references/labels-owner_addresses.md) - Address ownership and custody information (EVM chains only, excludes Bitcoin)
- [labels.owner_details](references/labels-owner_details.md) - Project and entity metadata with categories, links, and verification status (excludes Bitcoin)