# Dune SQL for labels.owner_addresses Table

Reference guide for querying the `labels.owner_addresses` table in Dune Analytics.

## Overview

The `labels.owner_addresses` table contains ownership and custody information for blockchain addresses across 47+ blockchains. This includes:
- **Smart contract wallets** (Gnosis Safe, Argent, etc.)
- **Factory-deployed contracts** with owner tracking
- **EOA (Externally Owned Account)** identification
- **Custody relationships** between addresses

## Tips

- **Multi-chain coverage**: Covers 47+ blockchains including Ethereum, Base, Polygon, Arbitrum, Optimism, Bitcoin, Solana, and many L2s
- **Owner identification**: Use `owner_key` for categorical ownership types (e.g., "gnosis_safe", "safe_wallet")
- **Custody tracking**: `custody_owner` provides human-readable names (e.g., "Gnosis Safe", "Argent Wallet")
- **Contract details**: `contract_name` and `contract_version` identify specific smart contract implementations
- **Address type**: `eoa` field indicates if an address is an Externally Owned Account
- **Factory patterns**: `factory_contract` tracks addresses deployed through factory contracts
- **Data freshness**: Updated regularly with `created_at` and `updated_at` timestamps
- **Address format**: The `address` column is `varbinary` type - use `0x` prefix for hex addresses
- **No time filtering needed**: Unlike transaction tables, this is a label/metadata table without time-based performance concerns

## Schema

Query to retrieve all column names and data types:

```sql
SELECT
  column_name,
  data_type
FROM information_schema.columns
WHERE table_schema = 'labels'
  AND table_name = 'owner_addresses'
ORDER BY ordinal_position;
```

**Result:** [labels-owner_addresses-sample-results/table00.csv](labels-owner_addresses-sample-results/table00.csv)

**Key columns:**
- `address` (varbinary): The blockchain address
- `blockchain` (varchar): Chain name (ethereum, polygon, base, etc.)
- `owner_key` (varchar): Categorical owner type identifier
- `custody_owner` (varchar): Human-readable custody owner name
- `account_owner` (varchar): Account-level ownership information
- `contract_name` (varchar): Smart contract implementation name
- `contract_version` (varchar): Contract version (e.g., "v1_3_0")
- `eoa` (varchar): Externally Owned Account indicator
- `factory_contract` (varchar): Factory contract address if deployed via factory
- `source` (varchar): Data source
- `algorithm_name` (varchar): Algorithm used for ownership detection
- `created_at` (timestamp): When the label was created
- `created_by` (varchar): Contributor who created the label

## Sample Data

Query to view sample records and understand the data structure:

```sql
SELECT *
FROM labels.owner_addresses
LIMIT 5;
```

**Result:** [labels-owner_addresses-sample-results/table01.csv](labels-owner_addresses-sample-results/table01.csv)

**Example records show:**
- Gnosis Safe multisig wallets on Polygon
- Contract version tracking (GnosisSafeL2_v1_3_0)
- Creator attribution (created_by)

## Blockchain Distribution

Query to analyze owner address data distribution across different blockchains:

```sql
SELECT
  blockchain,
  COUNT(*) as owner_address_count,
  COUNT(DISTINCT address) as unique_addresses,
  COUNT(DISTINCT owner_key) as unique_owner_keys,
  COUNT(DISTINCT custody_owner) as unique_custody_owners,
  COUNT(DISTINCT account_owner) as unique_account_owners,
  COUNT(DISTINCT contract_name) as unique_contract_names,
  COUNT(DISTINCT source) as unique_sources,
  COUNT(DISTINCT algorithm_name) as unique_algorithms,
  MIN(created_at) as earliest_label,
  MAX(created_at) as newest_label,
  COUNT(DISTINCT created_by) as contributors
FROM labels.owner_addresses
GROUP BY blockchain
ORDER BY owner_address_count DESC;
```

**Result:** [labels-owner_addresses-sample-results/table02.csv](labels-owner_addresses-sample-results/table02.csv)

**Key insights from distribution:**
- **Base** leads with 13M+ owner addresses
- **Worldchain** and **Optimism** follow with 12M+ and 6.4M+ respectively
- Coverage spans from major chains (Ethereum, Polygon) to newer L2s (Worldchain, Unichain, Sonic)
- Data history ranges from 2020 (Ethereum, Fantom) to 2026
- Most chains have 2-6 contributors maintaining the labels
- Hundreds of unique owner_keys and custody_owners per major chain

## Common Use Cases

### Find all Gnosis Safe addresses
```sql
SELECT address, blockchain, contract_name, contract_version
FROM labels.owner_addresses
WHERE owner_key = 'gnosis_safe'
LIMIT 100;
```

### Identify smart contract wallets on a specific chain
```sql
SELECT
  custody_owner,
  COUNT(*) as wallet_count,
  COUNT(DISTINCT contract_name) as contract_types
FROM labels.owner_addresses
WHERE blockchain = 'ethereum'
  AND custody_owner IS NOT NULL
GROUP BY custody_owner
ORDER BY wallet_count DESC;
```

### Track factory-deployed contracts
```sql
SELECT
  factory_contract,
  contract_name,
  COUNT(*) as deployed_count
FROM labels.owner_addresses
WHERE factory_contract IS NOT NULL
  AND blockchain = 'polygon'
GROUP BY factory_contract, contract_name
ORDER BY deployed_count DESC
LIMIT 20;
```
