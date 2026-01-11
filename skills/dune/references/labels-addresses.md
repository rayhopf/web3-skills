# Dune SQL for labels.addresses Table

Reference guide for querying the `labels.addresses` table in Dune Analytics.

## Overview

The `labels.addresses` table contains human-readable labels for blockchain addresses across multiple chains. This includes:
- **Address labels** (exchange wallets, smart contracts, notable entities)
- **Multi-chain coverage** (Ethereum, Base, Polygon, and other major blockchains)
- **Categorization** (DEX, CEX, DeFi protocols, NFT, etc.)
- **Community contributions** (labels from various contributors and data sources)
- **Label types** (usage patterns, entity identification, behavioral classification)
- **Model-generated labels** (algorithmic and query-based labeling)

## Tips

- **Address lookup**: Use this table to resolve addresses to human-readable names
- **Category filtering**: Filter by `category` to find addresses of specific types (dex, cex, defi, etc.)
- **Multi-chain**: Use `blockchain` field to filter by specific chain
- **Label types**: The `label_type` field indicates how the label was classified (usage, entity, etc.)
- **Data sources**: `source` shows where the label originated (query, model, manual, etc.)
- **Address format**: The `address` column is `varbinary` type - use `0x` prefix for hex addresses
- **No time filtering needed**: This is a label/metadata table without time-based performance concerns
- **Community driven**: Check `contributor` to see who added or maintains labels
- **Model names**: `model_name` identifies the specific labeling algorithm or model used

## Schema

Query to retrieve all column names and data types:

```sql
SELECT
  column_name,
  data_type
FROM information_schema.columns
WHERE table_schema = 'labels'
  AND table_name = 'addresses'
ORDER BY ordinal_position;
```

**Result:** [labels-addresses-sample-results/table00.csv](labels-addresses-sample-results/table00.csv)

**Key columns:**
- `blockchain` (varchar): Chain where the address exists (ethereum, base, polygon, etc.)
- `address` (varbinary): The blockchain address being labeled
- `name` (varchar): Human-readable label/name for the address
- `category` (varchar): Category classification (dex, cex, defi, nft, etc.)
- `contributor` (varchar): Person or entity who contributed the label
- `source` (varchar): Source of the label (query, model, manual, etc.)
- `created_at` (timestamp): When the label was first created
- `updated_at` (timestamp): When the label was last updated
- `model_name` (varchar): Name of the model/algorithm that generated the label
- `label_type` (varchar): Type of label (usage, entity, behavior, etc.)

## Sample Data

Query to view sample records and understand the data structure:

```sql
SELECT *
FROM labels.addresses
LIMIT 5;
```

**Result:** [labels-addresses-sample-results/table01.csv](labels-addresses-sample-results/table01.csv)

**Example records show:**
- Base chain addresses labeled as "Sparse Trader"
- DEX category usage labels
- Query-generated labels from contributor "gentrexha"
- Trader frequency model classifications
- Timestamp tracking for label creation and updates

## Common Use Cases

### Label distribution by blockchain
```sql
SELECT
  blockchain,
  COUNT(*) as label_count,
  COUNT(DISTINCT address) as unique_addresses,
  COUNT(DISTINCT category) as unique_categories,
  COUNT(DISTINCT name) as unique_names,
  COUNT(DISTINCT contributor) as unique_contributors,
  MIN(created_at) as earliest_label,
  MAX(updated_at) as latest_update
FROM labels.addresses
GROUP BY blockchain
ORDER BY label_count DESC
LIMIT 20;
```

**Result:** [labels-addresses-sample-results/table02.csv](labels-addresses-sample-results/table02.csv)

### Top categories by label count
```sql
SELECT
  category,
  COUNT(*) as label_count,
  COUNT(DISTINCT blockchain) as blockchains,
  COUNT(DISTINCT address) as unique_addresses,
  COUNT(DISTINCT name) as unique_names,
  COUNT(DISTINCT contributor) as unique_contributors
FROM labels.addresses
WHERE category IS NOT NULL
GROUP BY category
ORDER BY label_count DESC
LIMIT 20;
```

**Result:** [labels-addresses-sample-results/table03.csv](labels-addresses-sample-results/table03.csv)

### Find label for a specific address
```sql
SELECT
  blockchain,
  address,
  name,
  category,
  label_type,
  contributor,
  source,
  created_at,
  updated_at
FROM labels.addresses
WHERE address = 0xdac17f958d2ee523a2206206994597c13d831ec7
  AND blockchain = 'ethereum'
LIMIT 20;
```

**Result:** [labels-addresses-sample-results/table04.csv](labels-addresses-sample-results/table04.csv)

**Example:** Looking up the Tether USDT contract address returns multiple labels including "Fiat-backed stablecoin", "Tether: Tether_USD", and various DEX trading behavior labels.

### Find addresses by keyword (e.g., "japan gov")
```sql
SELECT
  blockchain,
  address,
  name,
  category,
  label_type,
  contributor,
  source
FROM labels.addresses
WHERE LOWER(name) LIKE '%japan%'
   OR LOWER(name) LIKE '%government%'
ORDER BY blockchain, name
LIMIT 20;
```

**Result:** [labels-addresses-sample-results/table05.csv](labels-addresses-sample-results/table05.csv)

**Example:** Searching for "japan" finds addresses with Japan-related ENS names like "0x🇯🇵japan.eth" and other Japanese-themed labels.
