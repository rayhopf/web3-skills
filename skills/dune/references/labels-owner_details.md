# Dune SQL for labels.owner_details Table

Reference guide for querying the `labels.owner_details` table in Dune Analytics.

## Overview

The `labels.owner_details` table contains detailed metadata about projects, protocols, and entities in the blockchain ecosystem. This includes:
- **Project information** (name, website, documentation, GitHub)
- **Social media links** and community resources
- **Category classification** (DEX, NFT, DeFi, scams, exploits, etc.)
- **Dune team curation** flags for verified projects
- **Country information** for projects with geographic presence
- **Contributor tracking** with creation and update timestamps

## Tips

- **Project discovery**: Use `primary_category` to find projects by type (e.g., "Decentralized Exchange", "NFT Marketplace")
- **Verified projects**: `dune_team` field indicates Dune-verified projects
- **Multi-category support**: `category_tags` array provides additional categorization beyond `primary_category`
- **Resource links**: Access project websites, documentation, GitHub repos, and social media
- **Scam identification**: Includes labeled phishing sites and exploit addresses
- **Data quality**: `updated_at` and `updated_by` track metadata freshness and contributors
- **No blockchain field**: This is a metadata table, not chain-specific
- **No time filtering needed**: Unlike transaction tables, this is a label/metadata table without time-based performance concerns

## Schema

Query to retrieve all column names and data types:

```sql
SELECT
  column_name,
  data_type
FROM information_schema.columns
WHERE table_schema = 'labels'
  AND table_name = 'owner_details'
ORDER BY ordinal_position;
```

**Result:** [labels-owner_details-sample-results/table00.csv](labels-owner_details-sample-results/table00.csv)

**Key columns:**
- `name` (varchar): Project or entity name
- `owner_key` (varchar): Unique identifier key for the owner/project
- `website` (varchar): Official project website URL
- `dune_team` (varchar): Dune team verification flag
- `project_documentation` (varchar): Documentation URL
- `project_github_url` (varchar): GitHub repository URL
- `social` (varchar): Social media links
- `primary_category` (varchar): Main category classification
- `category_tags` (array(varchar)): Additional category tags
- `country_name` (varchar): Country of origin or operation
- `description` (varchar): Project description
- `created_at` (timestamp): When the metadata was created
- `created_by` (varchar): Contributor who created the entry
- `updated_at` (timestamp): Last update timestamp
- `updated_by` (varchar): Contributor who last updated the entry

## Sample Data

Query to view sample records and understand the data structure:

```sql
SELECT *
FROM labels.owner_details
LIMIT 5;
```

**Result:** [labels-owner_details-sample-results/table01.csv](labels-owner_details-sample-results/table01.csv)

**Example records show:**
- Phishing/scam labels (Fake_Phishing sites)
- DeFi protocols (Swaap DEX)
- Security incidents (MultiSig Exploit entries)
- Category classifications ("Social Engineering Scams", "Decentralized Exchange", "Hacks and exploits")
- Contributor tracking and update history

## Common Use Cases

### Find projects by category
```sql
SELECT
  name,
  owner_key,
  website,
  primary_category,
  category_tags
FROM labels.owner_details
WHERE primary_category = 'Decentralized Exchange'
LIMIT 20;
```

**Result:** [labels-owner_details-sample-results/table02.csv](labels-owner_details-sample-results/table02.csv)

### Identify verified Dune team projects
```sql
SELECT
  name,
  owner_key,
  website,
  primary_category,
  dune_team
FROM labels.owner_details
WHERE dune_team IS NOT NULL
ORDER BY name
LIMIT 20;
```

**Result:** [labels-owner_details-sample-results/table03.csv](labels-owner_details-sample-results/table03.csv)

### Search for projects with GitHub repositories
```sql
SELECT
  name,
  owner_key,
  project_github_url,
  primary_category,
  website
FROM labels.owner_details
WHERE project_github_url IS NOT NULL
ORDER BY updated_at DESC
LIMIT 20;
```

**Result:** [labels-owner_details-sample-results/table04.csv](labels-owner_details-sample-results/table04.csv)

### Find scam and exploit labels
```sql
SELECT
  name,
  owner_key,
  primary_category,
  created_at,
  updated_at
FROM labels.owner_details
WHERE primary_category IN ('Social Engineering Scams', 'Hacks and exploits')
ORDER BY created_at DESC
LIMIT 20;
```

**Result:** [labels-owner_details-sample-results/table05.csv](labels-owner_details-sample-results/table05.csv)

### Get project metadata with all resources
```sql
SELECT
  name,
  owner_key,
  website,
  project_documentation,
  project_github_url,
  social,
  primary_category,
  description
FROM labels.owner_details
WHERE website IS NOT NULL
  AND (project_documentation IS NOT NULL OR project_github_url IS NOT NULL)
ORDER BY name
LIMIT 20;
```

**Result:** [labels-owner_details-sample-results/table06.csv](labels-owner_details-sample-results/table06.csv)

### Analyze category distribution
```sql
SELECT
  primary_category,
  COUNT(*) as project_count,
  COUNT(DISTINCT owner_key) as unique_owners,
  COUNT(CASE WHEN website IS NOT NULL THEN 1 END) as with_website,
  COUNT(CASE WHEN project_github_url IS NOT NULL THEN 1 END) as with_github,
  MIN(created_at) as first_entry,
  MAX(updated_at) as last_updated
FROM labels.owner_details
WHERE primary_category IS NOT NULL
GROUP BY primary_category
ORDER BY project_count DESC;
```

**Result:** [labels-owner_details-sample-results/table07.csv](labels-owner_details-sample-results/table07.csv)

### Track contributor activity
```sql
SELECT
  created_by as contributor,
  COUNT(*) as entries_created,
  COUNT(DISTINCT primary_category) as categories_covered,
  MIN(created_at) as first_contribution,
  MAX(created_at) as last_contribution
FROM labels.owner_details
WHERE created_by IS NOT NULL
GROUP BY created_by
ORDER BY entries_created DESC;
```

**Result:** [labels-owner_details-sample-results/table08.csv](labels-owner_details-sample-results/table08.csv)
