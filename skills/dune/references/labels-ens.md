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
LIMIT 5;
```

**Result:** [labels-ens-sample-results/table01.csv](labels-ens-sample-results/table01.csv)

## Common Queries

Check data distribution across blockchains

```sql
SELECT 
  blockchain,
  COUNT(*) as ens_label_count,
  MIN(created_at) as earliest_label,
  MAX(created_at) as newest_label,
  COUNT(DISTINCT address) as unique_addresses,
  COUNT(DISTINCT name) as unique_names,
  COUNT(DISTINCT category) as unique_categories,
  COUNT(DISTINCT contributor) as unique_contributors,
  COUNT(DISTINCT source) as unique_sources,
  COUNT(DISTINCT model_name) as unique_model_names,
  COUNT(DISTINCT label_type) as unique_label_types
FROM labels.ens
GROUP BY blockchain
ORDER BY ens_label_count DESC;
```

**Result:** [labels-ens-sample-results/table02.csv](labels-ens-sample-results/table02.csv)
