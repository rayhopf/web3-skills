# Dune SQL for bitcoin.outputs Table

Reference guide for querying the `bitcoin.outputs` table in Dune Analytics.

## Overview

The `bitcoin.outputs` table contains all Bitcoin transaction outputs (UTXOs). This includes:
- **Output details** (value, address, index)
- **Block information** (time, date, height, hash)
- **Transaction reference** (tx_id)
- **Script data** (type, assembly, hex)

## Tips

- **ALWAYS filter by time**: Use `WHERE block_time >= DATE '2024-01-01'` or `WHERE block_time >= NOW() - INTERVAL '7' DAY` to improve query performance
- **Value in BTC**: The `value` column is in Bitcoin (not satoshis)
- **NULL addresses**: Early coinbase outputs may have NULL addresses (pubkey type)
- **UTXO tracking**: Each row represents an unspent transaction output that can be spent in future transactions
- **Script types**: Common types include pubkey, pubkeyhash, scripthash, witness_v0_keyhash, witness_v0_scripthash
- **Performance**: Always include time filters - this table is very large

## Schema

Query to retrieve all column names and data types:

```sql
SELECT
  column_name,
  data_type
FROM information_schema.columns
WHERE table_schema = 'bitcoin'
  AND table_name = 'outputs'
ORDER BY ordinal_position;
```

**Result:** [bitcoin-outputs-sample-results/table00.csv](bitcoin-outputs-sample-results/table00.csv)

**Key columns:**
- `block_time` (timestamp): When the output was created
- `block_date` (date): Output creation date (useful for daily aggregations)
- `block_height` (bigint): Block number
- `block_hash` (varbinary): Block hash
- `tx_id` (varbinary): Transaction ID that created this output
- `index` (bigint): Output index within the transaction
- `value` (double): Output value in BTC
- `address` (varchar): Receiving address (can be NULL for early outputs)
- `type` (varchar): Script type (pubkey, pubkeyhash, scripthash, etc.)
- `script_asm` (varchar): Script in assembly format
- `script_hex` (varbinary): Script in hexadecimal format

## Sample Data

Query to view sample records and understand the data structure:

```sql
SELECT *
FROM bitcoin.outputs
LIMIT 5;
```

**Result:** [bitcoin-outputs-sample-results/table01.csv](bitcoin-outputs-sample-results/table01.csv)

**Example records show:**
- Early Bitcoin outputs from 2009 (block heights 18428-24136)
- Coinbase rewards of 50 BTC
- Pubkey script types (early Bitcoin standard)
- NULL addresses for pubkey outputs
- Complete script data in both assembly and hex formats

## Common Use Cases

### Daily output statistics
```sql
SELECT
  block_date,
  COUNT(*) as output_count,
  SUM(value) as total_btc,
  AVG(value) as avg_btc,
  COUNT(DISTINCT address) as unique_addresses
FROM bitcoin.outputs
WHERE block_time >= NOW() - INTERVAL '30' DAY
  AND value > 0
GROUP BY block_date
ORDER BY block_date DESC
LIMIT 20;
```

**Result:** [bitcoin-outputs-sample-results/table02.csv](bitcoin-outputs-sample-results/table02.csv)

### Top addresses by output value
```sql
SELECT
  address,
  COUNT(*) as output_count,
  SUM(value) as total_btc_received,
  AVG(value) as avg_btc_per_output,
  MIN(block_time) as first_output,
  MAX(block_time) as latest_output
FROM bitcoin.outputs
WHERE block_time >= NOW() - INTERVAL '30' DAY
  AND address IS NOT NULL
  AND value > 0
GROUP BY address
ORDER BY total_btc_received DESC
LIMIT 20;
```

**Result:** [bitcoin-outputs-sample-results/table03.csv](bitcoin-outputs-sample-results/table03.csv)
