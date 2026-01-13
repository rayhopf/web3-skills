#!/usr/bin/env python3
"""
Test script to check if MicroStrategy has bought BTC in recent weeks.
Query Bitcoin blockchain data using Dune Analytics.
"""
from dune_client.client import DuneClient
from dotenv import load_dotenv
import sys


def main():
    # Load environment variables from .env file
    load_dotenv()

    try:
        # Initialize Dune client (reads DUNE_API_KEY from env)
        dune = DuneClient()

        print("=" * 80)
        print("Testing Dune Skill: MicroStrategy Bitcoin Purchases")
        print("=" * 80)
        print()

        # Step 1: Find MicroStrategy addresses
        print("[1/3] Finding MicroStrategy labeled Bitcoin addresses...")
        print("-" * 80)

        microstrategy_addresses_sql = """
        SELECT address, label
        FROM query_6509358
        WHERE LOWER(label) LIKE '%microstrategy%'
           OR LOWER(label) LIKE '%micro strategy%'
           OR LOWER(label) LIKE '%mstr%'
        """

        address_results = dune.run_sql(query_sql=microstrategy_addresses_sql)

        if not address_results.result.rows:
            print("⚠️  No MicroStrategy addresses found in labeled data.")
            print("    Checking for common entity labels instead...")

            # Try broader search
            broader_sql = """
            SELECT label, COUNT(*) as count
            FROM query_6509358
            WHERE LOWER(label) LIKE '%micro%'
               OR LOWER(label) LIKE '%strategy%'
            GROUP BY label
            """
            broader_results = dune.run_sql(query_sql=broader_sql)

            if broader_results.result.rows:
                print("\nFound similar labels:")
                for row in broader_results.result.rows:
                    print(f"  - {row['label']}: {row['count']} addresses")
            else:
                print("\n❌ MicroStrategy addresses not found in Dune's labeled dataset.")
                print("\nNote: This doesn't mean MicroStrategy didn't buy BTC.")
                print("It means their addresses aren't publicly labeled in this dataset.")
            return

        # Print found addresses
        print(f"✓ Found {len(address_results.result.rows)} MicroStrategy address(es):")
        addresses = []
        for row in address_results.result.rows:
            print(f"  - {row['address'][:20]}... ({row['label']})")
            addresses.append(f"'{row['address']}'")
        print()

        # Step 2: Check recent Bitcoin activity
        print("[2/3] Checking recent Bitcoin activity (last 7 days)...")
        print("-" * 80)

        addresses_list = ", ".join(addresses)

        recent_activity_sql = f"""
        SELECT
          block_date,
          block_time,
          tx_id,
          address,
          value as btc_amount,
          block_height
        FROM bitcoin.outputs
        WHERE address IN ({addresses_list})
          AND block_time >= NOW() - INTERVAL '7' DAY
        ORDER BY block_time DESC
        LIMIT 50
        """

        activity_results = dune.run_sql(query_sql=recent_activity_sql)

        if not activity_results.result.rows:
            print("❌ No recent Bitcoin transactions found in the last 7 days.")
            print()

            # Try last 30 days
            print("[2b/3] Expanding search to last 30 days...")
            print("-" * 80)

            activity_30d_sql = f"""
            SELECT
              block_date,
              block_time,
              tx_id,
              address,
              value as btc_amount,
              block_height
            FROM bitcoin.outputs
            WHERE address IN ({addresses_list})
              AND block_time >= NOW() - INTERVAL '30' DAY
            ORDER BY block_time DESC
            LIMIT 50
            """

            activity_30d_results = dune.run_sql(query_sql=activity_30d_sql)

            if not activity_30d_results.result.rows:
                print("❌ No Bitcoin transactions found in the last 30 days either.")
            else:
                print(f"✓ Found {len(activity_30d_results.result.rows)} transaction(s) in last 30 days:")
                for i, row in enumerate(activity_30d_results.result.rows[:10], 1):
                    print(f"  {i}. {row['block_time']}: {row['btc_amount']:.8f} BTC")
                if len(activity_30d_results.result.rows) > 10:
                    print(f"  ... and {len(activity_30d_results.result.rows) - 10} more")
        else:
            print(f"✓ Found {len(activity_results.result.rows)} transaction(s) in last 7 days:")
            for i, row in enumerate(activity_results.result.rows[:10], 1):
                print(f"  {i}. {row['block_time']}: {row['btc_amount']:.8f} BTC")
            if len(activity_results.result.rows) > 10:
                print(f"  ... and {len(activity_results.result.rows) - 10} more")

        print()

        # Step 3: Aggregate statistics
        print("[3/3] Calculating aggregated statistics...")
        print("-" * 80)

        stats_sql = f"""
        SELECT
          COUNT(*) as total_transactions,
          SUM(value) as total_btc,
          AVG(value) as avg_btc_per_tx,
          MIN(block_time) as first_transaction,
          MAX(block_time) as latest_transaction
        FROM bitcoin.outputs
        WHERE address IN ({addresses_list})
          AND block_time >= NOW() - INTERVAL '7' DAY
        """

        stats_results = dune.run_sql(query_sql=stats_sql)

        if stats_results.result.rows:
            stats = stats_results.result.rows[0]
            print(f"📊 Summary (Last 7 Days):")
            print(f"  • Total Transactions: {stats['total_transactions']}")
            print(f"  • Total BTC Received: {stats['total_btc']:.8f} BTC" if stats['total_btc'] else "  • Total BTC Received: 0 BTC")
            print(f"  • Average per Transaction: {stats['avg_btc_per_tx']:.8f} BTC" if stats['avg_btc_per_tx'] else "  • Average per Transaction: 0 BTC")

            if stats['total_transactions'] and stats['total_transactions'] > 0:
                print(f"  • First Transaction: {stats['first_transaction']}")
                print(f"  • Latest Transaction: {stats['latest_transaction']}")
                print()
                print("✅ YES - MicroStrategy addresses received BTC in the last week!")
            else:
                print()
                print("❌ NO - No BTC received in MicroStrategy addresses in the last week.")

        print()
        print("=" * 80)
        print("✓ Test completed successfully!")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nCommon issues:")
        print("  1. Missing DUNE_API_KEY: Create a .env file with DUNE_API_KEY=your_key")
        print("  2. Invalid API key: Check your Dune API key at https://dune.com/settings/api")
        print("  3. Network issues: Check your internet connection")
        sys.exit(1)


if __name__ == "__main__":
    main()
