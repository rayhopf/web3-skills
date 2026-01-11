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

# Run existing query
query = QueryBase(query_id=1215383)
results = dune.run_query(query)

# Or get latest cached results (free, no execution credits)
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

### Create and Run Custom Query
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

# Create new query
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
# JSON (default)
results = dune.run_query(query)

# CSV
results_csv = dune.run_query_csv(query)

# Pandas DataFrame (requires pandas installed)
results_df = dune.run_query_dataframe(query)
```

## SQL Best Practices

- **ALWAYS check references FIRST**: Before writing SQL for any table, check the `references/` directory for table-specific documentation. This provides accurate column names, data types, and example queries.
- **Filter by time (when available)**: For tables with time columns like `block_time`, add date range filters to improve performance (e.g., `WHERE block_time >= DATE '2024-01-01'` or `WHERE block_time >= NOW() - INTERVAL '7' DAY`)
- **Use LIMIT**: Start with small limits when exploring data
- **Narrow scope first**: Begin with specific filters, expand as needed

## Table References

**IMPORTANT**: Before writing SQL queries for any table, always check its reference documentation in the `references/` directory. These files contain:
- Accurate column names and data types
- Table schemas and descriptions
- Example queries and best practices
- Performance optimization tips

Available references:
- [dex.trades](references/dex-trades.md) - Decentralized exchange trades across 40+ blockchains and protocols
- [tokens.transfers](references/tokens-transfers.md) - Token transfer events across chains
- [labels.addresses](references/labels-addresses.md) - Human-readable labels for blockchain addresses across multiple chains
- [labels.ens](references/labels-ens.md) - Ethereum Name Service (ENS) domain labels
- [labels.owner_addresses](references/labels-owner_addresses.md) - Address ownership and custody information across 47+ blockchains
- [labels.owner_details](references/labels-owner_details.md) - Project and entity metadata with categories, links, and verification status