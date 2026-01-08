
# Dune SQL for tokens.transfers Table

Reference guide for querying the `tokens.transfers` table in Dune Analytics.

## Tips

- Always add `block_time` with a date range filter to improve query performance and avoid timeouts
- Dune SQL is based on Trino SQL syntax

## Schema

Query to retrieve all column names and data types:

```sql
SELECT
  column_name,
  data_type
FROM information_schema.columns
WHERE table_schema = 'tokens'
  AND table_name = 'transfers'
ORDER BY ordinal_position;
```

**Result:** [tokens-transfers-sample-results/table00.csv](tokens-transfers-sample-results/table00.csv)

## Sample Data

Query to view sample records and understand the data structure:

```sql
SELECT *
FROM tokens.transfers
LIMIT 2;
```

**Result:** [tokens-transfers-sample-results/table01.csv](tokens-transfers-sample-results/table01.csv)

## Blockchain Distribution

Query to analyze transfer activity across different blockchains:

```sql
SELECT
  blockchain,
  COUNT(*) as transfer_count,
  COUNT(DISTINCT contract_address) as unique_tokens,
  MIN(block_date) as earliest_date,
  MAX(block_date) as latest_date
FROM tokens.transfers
WHERE block_time >= NOW() - INTERVAL '3' DAY
GROUP BY blockchain
ORDER BY transfer_count DESC;
```

**Result:** [tokens-transfers-sample-results/table02.csv](tokens-transfers-sample-results/table02.csv)