# Dune SQL for labels.ens Table

Reference guide for querying the `labels.ens` table in Dune Analytics.

## Tips

- This table contains Ethereum Name Service (ENS) domain information
- Use this to resolve addresses to human-readable ENS names
- Dune SQL is based on Trino SQL syntax

## Schema

Query to retrieve all column names and data types:

```sql
SELECT
  column_name,
  data_type
FROM information_schema.columns
WHERE table_schema = 'labels'
  AND table_name = 'ens'
ORDER BY ordinal_position;
```

**Result:** [labels-ens-sample-results/table00.csv](labels-ens-sample-results/table00.csv)

## Sample Data

Query to view sample records and understand the data structure:

```sql
SELECT *
FROM labels.ens
LIMIT 10;
```

**Result:** [labels-ens-sample-results/table01.csv](labels-ens-sample-results/table01.csv)

## Common Queries

### Resolve Address to ENS Name

Query to find ENS names for specific addresses:

```sql
SELECT
  address,
  name
FROM labels.ens
WHERE address = 0x123... -- Replace with target address
LIMIT 10;
```

**Result:** [labels-ens-sample-results/table02.csv](labels-ens-sample-results/table02.csv)
