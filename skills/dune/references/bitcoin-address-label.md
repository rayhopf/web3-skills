# Bitcoin Address Labels

Guide for retrieving Bitcoin address labels using Dune Analytics queries.

## Overview

Bitcoin address labels help identify exchanges, entities, and notable addresses on the Bitcoin blockchain. Dune provides pre-built queries that aggregate this labeling data.

## Getting Bitcoin Address Labels

Use the following query to retrieve Bitcoin address labels from Dune's curated queries:

```sql
SELECT address, exchange as label
FROM query_2613158
UNION ALL
SELECT *
FROM query_2614243
```

### Query Components

- **query_2613158**: Exchange addresses with labels
- **query_2614243**: Additional Bitcoin address labels

### Sample Results

| address | label |
|---------|-------|
| 3JJmF63ifcamPLiAmLgG96RA599yNtY3EQ | Binance |
| 34HpHYiyQwg69gFmCq2BGHjF1DZnZnBeBP | Binance |
| 34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo | Binance |
| 3HdGoUTbcztBnS7UzY4vSPYhwr424CiWAA | Binance |
| 3M219KR5vEneNb47ewrPfWyb5jQ2DjxRP6 | Binance |
| bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h | Binance |
| 395vnFScKQ1ay695C6v7gf89UzoFpx3WuJ | Binance |
| 3AeUiDpPPUrUBS377584sFCpx8KLfpX9Ry | Binance |
| 3FHNBLobJnbCTFTVakh5TXmEneyf5PT61B | Binance |
| 3FrmCRcGKiTATfreBDM9F17yAUDoDsnWeA | Binance |
