# Bitcoin Address Labels

Guide for retrieving Bitcoin address labels using Dune Analytics queries.

## Overview

Bitcoin address labels help identify exchanges, entities, and notable addresses on the Bitcoin blockchain. This reference provides a pre-built query that aggregates Bitcoin address labeling data from multiple sources, returning **54,111+ labeled addresses**.

## Usage

### Method 1: Run by Query ID (Recommended)

Execute the existing query to get the latest labeled addresses:

```python
from dune_client.client import DuneClient
from dune_client.query import QueryBase
from dotenv import load_dotenv

load_dotenv()
dune = DuneClient()

# Run the Bitcoin address labels query (uses execution credits)
query = QueryBase(query_id=6509358)
results = dune.run_query(query)

# Or get cached results if available (only re-executes if cache is older than max_age_hours)
# This uses credits only if the cached result is too old
results = dune.get_latest_result(6509358, max_age_hours=24)
```

**Query URL:** https://dune.com/queries/6509358

### Method 2: Use as Subquery

Reference this query in your own custom SQL:

```python
sql = """
SELECT
  t.tx_hash,
  t.from_address,
  t.to_address,
  labels.label as from_label
FROM bitcoin.transactions t
LEFT JOIN query_6509358 labels
  ON t.from_address = labels.address
WHERE t.block_time >= NOW() - INTERVAL '7' DAY
LIMIT 100
"""

results = dune.run_sql(query_sql=sql)
```

## Query Details

**Query ID:** 6509358
**Total labeled addresses:** 54,111+ addresses
**Label categories:** Exchanges (Binance, Coinbase, etc.), Government entities, Mining pools, Notable addresses
**Public query:** Available to all users at https://dune.com/queries/6509358

## Sample Results

| address | label |
|---------|-------|
| bc1qzd8c8h8dcgwuy5zd... | US Government |
| 3JJmF63ifcamPLiAmLgG96RA599yNtY3EQ | Binance |
| 34HpHYiyQwg69gFmCq2BGHjF1DZnZnBeBP | Binance |
| 34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo | Binance |
| 3M219KR5vEneNb47ewrPfWyb5jQ2DjxRP6 | Binance |
| bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h | Binance |

## Common Use Cases

### Look up specific address label

```python
sql = """
SELECT address, label
FROM query_6509358
WHERE address = 'bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h'
"""

results = dune.run_sql(query_sql=sql)
```

### Get all addresses for a specific exchange

```python
sql = """
SELECT address, label
FROM query_6509358
WHERE label = 'Binance'
ORDER BY address
"""

results = dune.run_sql(query_sql=sql)
```

### Count addresses by label category

```python
sql = """
SELECT
  label,
  COUNT(*) as address_count
FROM query_6509358
GROUP BY label
ORDER BY address_count DESC
LIMIT 20
"""

results = dune.run_sql(query_sql=sql)
```
