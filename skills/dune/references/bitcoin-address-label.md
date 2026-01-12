# Bitcoin Address Labels

Guide for retrieving Bitcoin address labels using Dune Analytics queries.

## Overview

Bitcoin address labels help identify exchanges, entities, and notable addresses on the Bitcoin blockchain. This reference provides a pre-built query that aggregates Bitcoin address labeling data from multiple sources, returning **54,111+ labeled addresses**.

## Usage

### Method 1: Use as Subquery (Recommended)

**⚠️ IMPORTANT:** This query contains 54,111+ rows. Downloading all rows costs significant download credits.

**Best practice:** Reference this query in your own SQL instead of downloading it directly:

```python
from dune_client.client import DuneClient
from dotenv import load_dotenv

load_dotenv()
dune = DuneClient()

# ✅ GOOD: Check count first
count_sql = "SELECT COUNT(*) as total FROM query_6509358"
count = dune.run_sql(query_sql=count_sql)
print(f"Total labels: {count.result.rows[0]['total']}")

# ✅ GOOD: Query specific labels with filters and limits
lookup_sql = """
SELECT address, label
FROM query_6509358
WHERE label = 'Binance'
LIMIT 100
"""
results = dune.run_sql(query_sql=lookup_sql)

# ❌ BAD: Don't download all 54,111 rows (costs many download credits)
# query = QueryBase(query_id=6509358)
# results = dune.run_query(query)  # DON'T DO THIS
```

**Query URL:** https://dune.com/queries/6509358

### Method 2: Join with Other Tables

Use this query to enrich your analysis by joining with transactions or other data:

```python
# Join labels with Bitcoin transactions to identify exchanges involved
sql = """
SELECT
  t.tx_hash,
  t.from_address,
  t.to_address,
  from_labels.label as from_label,
  to_labels.label as to_label
FROM bitcoin.transactions t
LEFT JOIN query_6509358 from_labels
  ON t.from_address = from_labels.address
LEFT JOIN query_6509358 to_labels
  ON t.to_address = to_labels.address
WHERE t.block_time >= NOW() - INTERVAL '7' DAY
  AND (from_labels.label IS NOT NULL OR to_labels.label IS NOT NULL)
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
