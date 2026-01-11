# Dune SQL for bitcoin.inputs Table

Reference guide for querying the `bitcoin.inputs` table in Dune Analytics.

## Overview

The `bitcoin.inputs` table contains all Bitcoin transaction inputs, which spend previous outputs. This includes:
- **Input details** (value, address, index)
- **Block information** (time, date, height, hash)
- **Transaction reference** (tx_id)
- **Spent output tracking** (spent_block_height, spent_tx_id, spent_output_number)
- **Coinbase data** (coinbase, is_coinbase flag)
- **Script and witness data** (type, assembly, hex, signatures, witness_data)

## Tips

- **ALWAYS filter by time**: Use `WHERE block_time >= DATE '2024-01-01'` or `WHERE block_time >= NOW() - INTERVAL '7' DAY` to improve query performance
- **Value in BTC**: The `value` column is in Bitcoin (not satoshis)
- **Coinbase inputs**: Mining rewards have `is_coinbase = true` and contain block reward + fees
- **NULL addresses**: Coinbase inputs don't spend previous outputs, so address may be NULL
- **Spent output tracking**: Use `spent_tx_id` and `spent_output_number` to trace which output was spent
- **SegWit data**: `witness_data` array contains witness information for SegWit transactions
- **Performance**: Always include time filters - this table is very large

## Schema

Query to retrieve all column names and data types:

```sql
SELECT
  column_name,
  data_type
FROM information_schema.columns
WHERE table_schema = 'bitcoin'
  AND table_name = 'inputs'
ORDER BY ordinal_position;
```

**Result:** [bitcoin-inputs-sample-results/table00.csv](bitcoin-inputs-sample-results/table00.csv)

**Key columns:**
- `block_time` (timestamp): When the input was created
- `block_date` (date): Input creation date (useful for daily aggregations)
- `block_height` (bigint): Block number
- `block_hash` (varbinary): Block hash
- `tx_id` (varbinary): Transaction ID that contains this input
- `index` (integer): Input index within the transaction
- `spent_block_height` (bigint): Block height of the output being spent
- `spent_tx_id` (varbinary): Transaction ID of the output being spent
- `spent_output_number` (bigint): Output index being spent
- `value` (double): Input value in BTC
- `address` (varchar): Spending address (can be NULL for coinbase)
- `type` (varchar): Script type
- `coinbase` (varbinary): Coinbase data for mining rewards
- `is_coinbase` (boolean): True if this is a coinbase (mining) input
- `script_asm` (varchar): Script in assembly format
- `script_hex` (varbinary): Script in hexadecimal format
- `script_desc` (varchar): Script description
- `script_signature_asm` (varchar): Signature script in assembly format
- `script_signature_hex` (varbinary): Signature script in hexadecimal format
- `sequence` (bigint): Sequence number for transaction ordering
- `witness_data` (array(varbinary)): SegWit witness data array

## Sample Data

Query to view sample records and understand the data structure:

```sql
SELECT *
FROM bitcoin.inputs
LIMIT 5;
```

**Result:** [bitcoin-inputs-sample-results/table01.csv](bitcoin-inputs-sample-results/table01.csv)

**Example records show:**
- Early Bitcoin coinbase inputs from 2009 (block heights 6983-9288)
- All inputs have `is_coinbase = true` (mining rewards)
- NULL addresses and values for coinbase inputs
- Coinbase data in hexadecimal format
- Maximum sequence numbers (4294967295)

## Common Use Cases

### Daily input statistics
```sql
SELECT
  block_date,
  COUNT(*) as input_count,
  SUM(value) as total_btc_spent,
  AVG(value) as avg_btc,
  COUNT(DISTINCT address) as unique_addresses,
  SUM(CASE WHEN is_coinbase = true THEN 1 ELSE 0 END) as coinbase_inputs
FROM bitcoin.inputs
WHERE block_time >= NOW() - INTERVAL '30' DAY
  AND value > 0
GROUP BY block_date
ORDER BY block_date DESC
LIMIT 20;
```

**Result:** [bitcoin-inputs-sample-results/table02.csv](bitcoin-inputs-sample-results/table02.csv)

### Top spending addresses
```sql
SELECT
  address,
  COUNT(*) as input_count,
  SUM(value) as total_btc_spent,
  AVG(value) as avg_btc_per_input,
  MIN(block_time) as first_spend,
  MAX(block_time) as latest_spend
FROM bitcoin.inputs
WHERE block_time >= NOW() - INTERVAL '30' DAY
  AND address IS NOT NULL
  AND value > 0
  AND is_coinbase = false
GROUP BY address
ORDER BY total_btc_spent DESC
LIMIT 20;
```

**Result:** [bitcoin-inputs-sample-results/table03.csv](bitcoin-inputs-sample-results/table03.csv)
