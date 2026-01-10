# Claude Guide: Creating Dune Table References

This guide documents the process for creating new table reference documentation in `skills/dune/references/`.

## Overview

Table references provide comprehensive documentation for Dune Analytics tables, including:
- Table schema and column descriptions
- Sample data
- Common use case queries with results
- Best practices and tips

Each table reference consists of:
1. A markdown file (e.g., `labels-owner_details.md`)
2. A sample results directory (e.g., `labels-owner_details-sample-results/`)
3. CSV files containing query results (e.g., `table00.csv`, `table01.csv`, etc.)

## Step-by-Step Process

### 1. Create Python Script to Fetch Schema and Sample Data

Create a temporary Python script (e.g., `fetch_owner_details_schema.py`) in the project root:

```python
#!/usr/bin/env python3
"""
Fetch schema and sample data for labels.owner_details table from Dune Analytics.
"""
import os
from pathlib import Path
from dune_client.client import DuneClient
from dotenv import load_dotenv


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Initialize Dune client (reads DUNE_API_KEY from env)
    dune = DuneClient()

    # Create output directory
    output_dir = Path("skills/dune/references/TABLE_NAME-sample-results")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Query 1: Get table schema
    print("Fetching schema for schema.table_name...")
    schema_sql = """
    SELECT
      column_name,
      data_type
    FROM information_schema.columns
    WHERE table_schema = 'schema_name'
      AND table_name = 'table_name'
    ORDER BY ordinal_position;
    """

    schema_query = dune.create_query(
        name="table_name schema",
        query_sql=schema_sql
    )
    schema_results = dune.run_query_csv(schema_query.base)
    with open(output_dir / "table00.csv", "wb") as f:
        f.write(schema_results.data.getvalue())
    print(f"✓ Saved schema to {output_dir / 'table00.csv'}")

    # Query 2: Get sample data
    print("\nFetching sample data...")
    sample_sql = """
    SELECT *
    FROM schema.table_name
    LIMIT 5;
    """

    sample_query = dune.create_query(
        name="table_name sample data",
        query_sql=sample_sql
    )
    sample_results = dune.run_query_csv(sample_query.base)
    with open(output_dir / "table01.csv", "wb") as f:
        f.write(sample_results.data.getvalue())
    print(f"✓ Saved sample data to {output_dir / 'table01.csv'}")

    print("\n✓ All data fetched successfully!")
    print(f"\nNext steps:")
    print(f"1. Review the CSV files in {output_dir}")
    print(f"2. Create additional queries based on the schema")
    print(f"3. Create the TABLE_NAME.md reference file")


if __name__ == "__main__":
    main()
```

### 2. Run the Script

```bash
python fetch_script_name.py
```

This creates:
- `skills/dune/references/TABLE_NAME-sample-results/table00.csv` (schema from information_schema.columns)
- `skills/dune/references/TABLE_NAME-sample-results/table01.csv` (sample data)

### 3. Create Additional Query Results

Create another script to fetch all common use case query results:

```python
#!/usr/bin/env python3
"""
Fetch all common use case query results for table from Dune Analytics.
"""
import os
from pathlib import Path
from dune_client.client import DuneClient
from dotenv import load_dotenv


def main():
    load_dotenv()
    dune = DuneClient()

    output_dir = Path("skills/dune/references/TABLE_NAME-sample-results")
    output_dir.mkdir(parents=True, exist_ok=True)

    queries = [
        {
            "name": "Query description",
            "file": "table02.csv",
            "sql": """
SELECT ...
FROM schema.table_name
WHERE ...
LIMIT 20;
"""
        },
        # Add more queries...
    ]

    for i, query_info in enumerate(queries, start=2):
        print(f"\n[{i-1}/{len(queries)}] Fetching: {query_info['name']}...")

        try:
            query = dune.create_query(
                name=f"table_name - {query_info['name']}",
                query_sql=query_info['sql']
            )
            results = dune.run_query_csv(query.base)

            with open(output_dir / query_info['file'], "wb") as f:
                f.write(results.data.getvalue())

            print(f"✓ Saved to {query_info['file']}")

        except Exception as e:
            print(f"✗ Error: {e}")
            continue

    print("\n✓ All queries completed!")


if __name__ == "__main__":
    main()
```

### 4. Create Markdown Documentation

Create `skills/dune/references/TABLE_NAME.md` following this template:

```markdown
# Dune SQL for schema.table_name Table

Reference guide for querying the `schema.table_name` table in Dune Analytics.

## Overview

The `schema.table_name` table contains [description]. This includes:
- **Feature 1** (brief description)
- **Feature 2** (brief description)
- **Feature 3** (brief description)

## Tips

- **Tip 1**: Explanation
- **Tip 2**: Explanation
- **Coverage**: Mention data coverage/scope
- **Performance**: Time filtering advice if applicable
- **Special notes**: Any unique characteristics

## Schema

Query to retrieve all column names and data types:

\`\`\`sql
SELECT
  column_name,
  data_type
FROM information_schema.columns
WHERE table_schema = 'schema_name'
  AND table_name = 'table_name'
ORDER BY ordinal_position;
\`\`\`

**Result:** [TABLE_NAME-sample-results/table00.csv](TABLE_NAME-sample-results/table00.csv)

**Key columns:**
- `column1` (type): Description
- `column2` (type): Description
- `column3` (type): Description

## Sample Data

Query to view sample records and understand the data structure:

\`\`\`sql
SELECT *
FROM schema.table_name
LIMIT 5;
\`\`\`

**Result:** [TABLE_NAME-sample-results/table01.csv](TABLE_NAME-sample-results/table01.csv)

**Example records show:**
- Key insight 1
- Key insight 2
- Key insight 3

## Common Use Cases

### Use Case 1 Title
\`\`\`sql
SELECT
  column1,
  column2
FROM schema.table_name
WHERE condition
LIMIT 20;
\`\`\`

**Result:** [TABLE_NAME-sample-results/table02.csv](TABLE_NAME-sample-results/table02.csv)

### Use Case 2 Title
\`\`\`sql
SELECT ...
\`\`\`

**Result:** [TABLE_NAME-sample-results/table03.csv](TABLE_NAME-sample-results/table03.csv)

[Continue for all use cases...]
```

### 5. Update SKILL.md

Add the new reference to the list in `skills/dune/SKILL.md`:

```markdown
Available references:
- [tokens.transfers](references/tokens-transfers.md) - Token transfer events across chains
- [labels.ens](references/labels-ens.md) - Ethereum Name Service (ENS) domain labels
- [labels.owner_addresses](references/labels-owner_addresses.md) - Address ownership and custody information
- [labels.owner_details](references/labels-owner_details.md) - Project and entity metadata
- [schema.table_name](references/TABLE_NAME.md) - Brief description
```

### 6. Clean Up

Remove temporary Python scripts:

```bash
rm fetch_script_name.py
rm fetch_queries_script.py
```

## File Naming Conventions

- **Markdown file:** `table_name.md` (use hyphens for multi-word tables like `owner_details`)
- **Sample directory:** `table_name-sample-results/` (match the markdown filename)
- **CSV files:** `table00.csv`, `table01.csv`, `table02.csv`, etc. (sequential numbering)
  - `table00.csv` - Schema
  - `table01.csv` - Sample data
  - `table02.csv` and up - Common use case query results

## CSV File Mapping

| File | Content | Source |
|------|---------|--------|
| `table00.csv` | Table schema | `INFORMATION_SCHEMA.COLUMNS` query (auto-fetched) |
| `table01.csv` | Sample data | `SELECT * LIMIT 5` (auto-fetched) |
| `table02.csv` | First use case | Common use case query 1 |
| `table03.csv` | Second use case | Common use case query 2 |
| `table04.csv` | Third use case | Common use case query 3 |
| ... | ... | ... |

## Best Practices

### Tips Section
- Start with most important usage tips
- Include performance optimization advice (time filtering for transaction tables)
- Mention data coverage (chains, time range, special features)
- Note any unique characteristics (no blockchain field, array types, etc.)

### Common Use Cases
- Provide 5-7 practical query examples
- Order from simple to complex
- Include LIMIT clause (typically 20 for examples)
- Cover different query patterns (filters, aggregations, joins if applicable)
- Each query should solve a real use case

### Schema Documentation
- List **Key columns** with types and clear descriptions
- Focus on columns users will query most often
- Explain any special types (arrays, timestamps with timezone, etc.)

### Sample Data Insights
- Highlight what the example records demonstrate
- Point out interesting patterns or edge cases
- Explain category classifications or enum values if present

## Example: labels.owner_details

This reference was created following these exact steps:

1. Created `fetch_owner_details_schema.py` to fetch schema and sample data automatically
2. Ran script: `python fetch_owner_details_schema.py` (generated table00.csv and table01.csv)
3. Created `fetch_owner_details_queries.py` with 7 use case queries
4. Ran script: `python fetch_owner_details_queries.py` (generated table02-08.csv)
5. Created `labels-owner_details.md` with complete documentation
6. Updated `SKILL.md` to include the new reference
7. Deleted temporary Python scripts

**Result:** Complete reference with:
- Schema documentation (table00.csv - auto-fetched from information_schema.columns)
- Sample data (table01.csv - auto-fetched with SELECT * LIMIT 5)
- 7 common use cases with CSV results (table02-08.csv)

## Notes

- Always use `.env` file for `DUNE_API_KEY` (never hardcode)
- Use `python-dotenv` to load environment variables
- Run queries with `dune.create_query()` then `.run_query_csv(query.base)`
- Save CSV with `write(results.data.getvalue())` in binary mode (`"wb"`)
- Each script run creates/updates Dune queries in your account
- Consider API rate limits and execution credits when running multiple queries
