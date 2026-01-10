# Dune SQL for dex.trades Table

Reference guide for querying the `dex.trades` table in Dune Analytics.

## Overview

The `dex.trades` table contains all decentralized exchange (DEX) trades across multiple blockchains and protocols. This includes:
- **Multi-chain coverage** (Ethereum, Base, Arbitrum, Polygon, BNB Chain, and 40+ other blockchains)
- **Multi-DEX support** (Uniswap, PancakeSwap, SushiSwap, Curve, and dozens of other protocols)
- **Complete trade data** (tokens bought/sold, amounts, USD values, participants)
- **Transaction context** (block info, tx hash, event index)
- **Version tracking** (protocol versions like Uniswap v2/v3)

## Tips

- **ALWAYS filter by time**: Use `WHERE block_time >= DATE '2024-01-01'` or `WHERE block_time >= NOW() - INTERVAL '7' DAY` to improve query performance
- **Multi-chain analysis**: Filter by `blockchain` for chain-specific analysis
- **USD values**: Use `amount_usd` for volume calculations (may be NULL for some trades)
- **Token pairs**: The `token_pair` column provides formatted pair names (e.g., "ETH-USDC")
- **Raw amounts**: Use `token_bought_amount_raw` and `token_sold_amount_raw` for precise integer values
- **Decimal amounts**: Use `token_bought_amount` and `token_sold_amount` for human-readable decimals
- **Address format**: Token and participant addresses are `varbinary` type - use `0x` prefix for hex addresses
- **Event tracking**: `evt_index` helps identify specific trade events within a transaction
- **Performance**: Always include time filters - this table is very large and queries without time filters will be slow/expensive

## Schema

Query to retrieve all column names and data types:

```sql
SELECT
  column_name,
  data_type
FROM information_schema.columns
WHERE table_schema = 'dex'
  AND table_name = 'trades'
ORDER BY ordinal_position;
```

**Result:** [dex-trades-sample-results/table00.csv](dex-trades-sample-results/table00.csv)

**Key columns:**
- `blockchain` (varchar): Chain where the trade occurred (ethereum, base, arbitrum, etc.)
- `project` (varchar): DEX protocol name (uniswap, pancakeswap, sushiswap, etc.)
- `version` (varchar): Protocol version (v2, v3, 1, 2, etc.)
- `block_time` (timestamp): When the trade occurred
- `block_date` (date): Trade date (useful for daily aggregations)
- `block_number` (bigint): Block number
- `token_bought_symbol` (varchar): Symbol of token bought (ETH, USDC, etc.)
- `token_sold_symbol` (varchar): Symbol of token sold
- `token_pair` (varchar): Formatted trading pair (e.g., "ETH-USDC")
- `token_bought_amount` (double): Amount of token bought (decimal adjusted)
- `token_sold_amount` (double): Amount of token sold (decimal adjusted)
- `token_bought_amount_raw` (uint256): Raw amount bought (no decimal adjustment)
- `token_sold_amount_raw` (uint256): Raw amount sold (no decimal adjustment)
- `amount_usd` (double): Trade value in USD
- `token_bought_address` (varbinary): Contract address of token bought
- `token_sold_address` (varbinary): Contract address of token sold
- `taker` (varbinary): Address that initiated the trade
- `maker` (varbinary): Address providing liquidity (may be NULL for some DEX types)
- `project_contract_address` (varbinary): DEX contract address
- `tx_hash` (varbinary): Transaction hash
- `tx_from` (varbinary): Transaction sender
- `tx_to` (varbinary): Transaction recipient
- `evt_index` (bigint): Event index within the transaction

## Sample Data

Query to view sample records and understand the data structure:

```sql
SELECT *
FROM dex.trades
LIMIT 5;
```

**Result:** [dex-trades-sample-results/table01.csv](dex-trades-sample-results/table01.csv)

**Example records show:**
- Cross-chain trades (zkEVM, Base, Polygon)
- Various DEX protocols (Clipper, PlantBaseSwap, xChange)
- Different token pairs (POL-USDC, PLANT-USDbC, WPOL-XHELLOWORLD)
- USD-denominated volumes
- Complete transaction context (hashes, addresses, timestamps)

## Common Use Cases

### Trading volume by blockchain
```sql
SELECT
  blockchain,
  COUNT(*) as trade_count,
  SUM(amount_usd) as total_volume_usd,
  COUNT(DISTINCT project) as unique_dex_projects,
  COUNT(DISTINCT token_pair) as unique_pairs,
  MIN(block_time) as first_trade,
  MAX(block_time) as latest_trade
FROM dex.trades
WHERE block_time >= NOW() - INTERVAL '7' DAY
GROUP BY blockchain
ORDER BY total_volume_usd DESC
LIMIT 20;
```

**Result:** [dex-trades-sample-results/table02.csv](dex-trades-sample-results/table02.csv)

### Top DEX projects by volume
```sql
SELECT
  project,
  blockchain,
  COUNT(*) as trade_count,
  SUM(amount_usd) as total_volume_usd,
  AVG(amount_usd) as avg_trade_size_usd,
  COUNT(DISTINCT taker) as unique_traders
FROM dex.trades
WHERE block_time >= NOW() - INTERVAL '7' DAY
  AND amount_usd IS NOT NULL
GROUP BY project, blockchain
ORDER BY total_volume_usd DESC
LIMIT 20;
```

**Result:** [dex-trades-sample-results/table03.csv](dex-trades-sample-results/table03.csv)

### Recent trades for specific token pair
```sql
SELECT
  block_time,
  blockchain,
  project,
  token_bought_symbol,
  token_sold_symbol,
  token_bought_amount,
  token_sold_amount,
  amount_usd,
  tx_hash
FROM dex.trades
WHERE token_pair LIKE '%ETH%'
  AND block_time >= NOW() - INTERVAL '1' DAY
ORDER BY block_time DESC
LIMIT 20;
```

**Result:** [dex-trades-sample-results/table04.csv](dex-trades-sample-results/table04.csv)

### Top trading pairs by volume
```sql
SELECT
  token_pair,
  blockchain,
  COUNT(*) as trade_count,
  SUM(amount_usd) as total_volume_usd,
  AVG(amount_usd) as avg_trade_size_usd,
  COUNT(DISTINCT project) as dex_count
FROM dex.trades
WHERE block_time >= NOW() - INTERVAL '7' DAY
  AND token_pair IS NOT NULL
  AND amount_usd IS NOT NULL
GROUP BY token_pair, blockchain
ORDER BY total_volume_usd DESC
LIMIT 20;
```

**Result:** [dex-trades-sample-results/table05.csv](dex-trades-sample-results/table05.csv)

### Daily trading volume over time
```sql
SELECT
  block_date,
  COUNT(*) as trade_count,
  SUM(amount_usd) as total_volume_usd,
  COUNT(DISTINCT blockchain) as active_blockchains,
  COUNT(DISTINCT project) as active_dex_projects,
  COUNT(DISTINCT taker) as unique_traders
FROM dex.trades
WHERE block_time >= NOW() - INTERVAL '30' DAY
  AND amount_usd IS NOT NULL
GROUP BY block_date
ORDER BY block_date DESC
LIMIT 20;
```

**Result:** [dex-trades-sample-results/table06.csv](dex-trades-sample-results/table06.csv)

### Largest trades by USD value
```sql
SELECT
  block_time,
  blockchain,
  project,
  token_bought_symbol,
  token_sold_symbol,
  token_bought_amount,
  token_sold_amount,
  amount_usd,
  taker,
  tx_hash
FROM dex.trades
WHERE block_time >= NOW() - INTERVAL '7' DAY
  AND amount_usd IS NOT NULL
ORDER BY amount_usd DESC
LIMIT 20;
```

**Result:** [dex-trades-sample-results/table07.csv](dex-trades-sample-results/table07.csv)

### DEX project activity by version
```sql
SELECT
  project,
  version,
  blockchain,
  COUNT(*) as trade_count,
  SUM(amount_usd) as total_volume_usd,
  COUNT(DISTINCT token_pair) as unique_pairs
FROM dex.trades
WHERE block_time >= NOW() - INTERVAL '7' DAY
  AND amount_usd IS NOT NULL
GROUP BY project, version, blockchain
ORDER BY total_volume_usd DESC
LIMIT 20;
```

**Result:** [dex-trades-sample-results/table08.csv](dex-trades-sample-results/table08.csv)
