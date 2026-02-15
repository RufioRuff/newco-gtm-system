#!/usr/bin/env python3
"""
NEWCO Apache Arrow Data Processor
=================================

High-performance data processing for PE-VC data using Apache Arrow.

Benefits:
- 10-100x faster than pandas for large datasets
- Zero-copy data sharing between processes
- Efficient memory usage
- Columnar storage format
- Interoperability with all languages

Use cases:
- Fast portfolio analytics
- Real-time data feeds to agents
- Historical data analysis
- Cross-agent data sharing
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    import pyarrow.compute as pc
    ARROW_AVAILABLE = True
except ImportError:
    ARROW_AVAILABLE = False
    print("⚠️  Apache Arrow not installed")
    print("Install with: pip install pyarrow")

import pandas as pd

# Configuration
DATA_DIR = "/Users/rufio/NEWCO/PE-VC-Source-Data"
ARROW_DIR = "/Users/rufio/NEWCO/PE-VC-Source-Data/arrow"
os.makedirs(ARROW_DIR, exist_ok=True)

class ArrowDataProcessor:
    """High-performance data processor using Apache Arrow"""

    def __init__(self):
        if not ARROW_AVAILABLE:
            raise ImportError("Apache Arrow not available. Install with: pip install pyarrow")

        self.arrow_dir = ARROW_DIR
        self.companies_table = None
        self.people_table = None

    def load_from_json(self, json_file: str) -> pa.Table:
        """Load JSON data into Arrow table"""
        print(f"📊 Loading data from {json_file}...")

        with open(json_file, 'r') as f:
            data = json.load(f)

        # Extract companies
        companies = data.get('companies', {})
        company_records = []

        for name, company in companies.items():
            record = {
                'name': name,
                'sector': company.get('sector'),
                'stage': company.get('stage'),
                'founded': company.get('founded'),
                'location': company.get('location'),
                'employees': company.get('employees'),
                'revenue': company.get('revenue'),
                'revenue_growth': company.get('revenue_growth'),
                'burn_rate': company.get('burn_rate'),
                'burn_multiple': company.get('burn_multiple'),
                'valuation': company.get('valuation'),
                'total_funding': company.get('total_funding'),
                'ipo_probability': company.get('ipo_probability')
            }
            company_records.append(record)

        # Create Arrow table
        table = pa.Table.from_pylist(company_records)

        print(f"✅ Loaded {len(company_records)} companies into Arrow table")
        print(f"   Columns: {table.column_names}")
        print(f"   Memory: {table.nbytes / 1024:.2f} KB")

        return table

    def save_to_parquet(self, table: pa.Table, filename: str):
        """Save Arrow table to Parquet format"""
        filepath = os.path.join(self.arrow_dir, filename)

        pq.write_table(table, filepath, compression='snappy')

        print(f"✅ Saved to Parquet: {filepath}")
        print(f"   Size: {os.path.getsize(filepath) / 1024:.2f} KB")

    def load_from_parquet(self, filename: str) -> pa.Table:
        """Load Arrow table from Parquet"""
        filepath = os.path.join(self.arrow_dir, filename)

        table = pq.read_table(filepath)

        print(f"✅ Loaded from Parquet: {filepath}")
        return table

    def filter_companies(self, table: pa.Table, filters: Dict[str, Any]) -> pa.Table:
        """Filter companies using Arrow compute functions"""
        print(f"🔍 Filtering companies...")

        mask = None

        for column, condition in filters.items():
            if isinstance(condition, dict):
                op = condition.get('op', '==')
                value = condition.get('value')

                if op == '>':
                    col_mask = pc.greater(table[column], value)
                elif op == '>=':
                    col_mask = pc.greater_equal(table[column], value)
                elif op == '<':
                    col_mask = pc.less(table[column], value)
                elif op == '<=':
                    col_mask = pc.less_equal(table[column], value)
                elif op == '==':
                    col_mask = pc.equal(table[column], value)
                else:
                    continue

                mask = col_mask if mask is None else pc.and_(mask, col_mask)

        if mask is None:
            return table

        filtered = table.filter(mask)

        print(f"✅ Filtered: {len(table)} → {len(filtered)} rows")
        return filtered

    def aggregate_metrics(self, table: pa.Table) -> Dict[str, Any]:
        """Calculate aggregate metrics using Arrow"""
        print(f"📊 Calculating aggregate metrics...")

        metrics = {}

        # Total valuation
        if 'valuation' in table.column_names:
            valuations = table['valuation'].combine_chunks()
            metrics['total_valuation'] = pc.sum(valuations).as_py()
            metrics['avg_valuation'] = pc.mean(valuations).as_py()
            median_result = pc.quantile(valuations, q=0.5)
            metrics['median_valuation'] = median_result[0].as_py() if len(median_result) > 0 else None

        # Total funding
        if 'total_funding' in table.column_names:
            funding = table['total_funding'].combine_chunks()
            # Filter out None values
            funding_valid = funding.drop_null()
            if len(funding_valid) > 0:
                metrics['total_funding'] = pc.sum(funding_valid).as_py()
                metrics['avg_funding'] = pc.mean(funding_valid).as_py()

        # Revenue growth
        if 'revenue_growth' in table.column_names:
            growth = table['revenue_growth'].combine_chunks()
            growth_valid = growth.drop_null()
            if len(growth_valid) > 0:
                metrics['avg_growth'] = pc.mean(growth_valid).as_py()
                median_result = pc.quantile(growth_valid, q=0.5)
                metrics['median_growth'] = median_result[0].as_py() if len(median_result) > 0 else None

        # Count by stage
        if 'stage' in table.column_names:
            stages = table['stage'].combine_chunks()
            stage_counts = pc.value_counts(stages).to_pylist()
            metrics['stage_distribution'] = {item['values']: item['counts'] for item in stage_counts}

        print(f"✅ Metrics calculated: {len(metrics)} metrics")
        return metrics

    def benchmark_performance(self, json_file: str, iterations: int = 100):
        """Benchmark Arrow vs Pandas performance"""
        print(f"\n⚡ Benchmarking performance ({iterations} iterations)...")
        print("")

        # Load data
        with open(json_file, 'r') as f:
            data = json.load(f)

        companies = data.get('companies', {})
        company_records = [
            {**company, 'name': name}
            for name, company in companies.items()
        ]

        # Benchmark Arrow
        arrow_times = []
        for _ in range(iterations):
            start = time.time()
            table = pa.Table.from_pylist(company_records)
            # Filter: revenue > 100M
            mask = pc.greater(table['revenue'], 100000000)
            filtered = table.filter(mask)
            # Calculate average valuation
            avg = pc.mean(filtered['valuation'].combine_chunks())
            arrow_times.append(time.time() - start)

        arrow_avg = sum(arrow_times) / len(arrow_times) * 1000  # ms

        # Benchmark Pandas
        pandas_times = []
        for _ in range(iterations):
            start = time.time()
            df = pd.DataFrame(company_records)
            # Filter: revenue > 100M
            filtered = df[df['revenue'] > 100000000]
            # Calculate average valuation
            avg = filtered['valuation'].mean()
            pandas_times.append(time.time() - start)

        pandas_avg = sum(pandas_times) / len(pandas_times) * 1000  # ms

        # Results
        speedup = pandas_avg / arrow_avg

        print(f"Results:")
        print(f"  Arrow:  {arrow_avg:.3f} ms")
        print(f"  Pandas: {pandas_avg:.3f} ms")
        print(f"  Speedup: {speedup:.2f}x faster with Arrow")
        print("")

        return {
            'arrow_ms': arrow_avg,
            'pandas_ms': pandas_avg,
            'speedup': speedup
        }

    def create_agent_feed(self, table: pa.Table, agent_type: str) -> Dict[str, Any]:
        """Create optimized data feed for specific agent type"""
        print(f"📡 Creating data feed for {agent_type}...")

        if agent_type == "ipo_predictor":
            # Filter: high-growth, pre-IPO companies
            mask = pc.and_(
                pc.greater(table['revenue_growth'], 50),
                pc.not_equal(table['stage'], 'Public')
            )
            filtered = table.filter(mask)

            # Select relevant columns
            feed = filtered.select(['name', 'revenue', 'revenue_growth', 'burn_multiple', 'valuation'])

        elif agent_type == "deal_scout":
            # Filter: high-growth, Series B-D
            stages = ['Series B', 'Series C', 'Series D']
            mask = pc.and_(
                pc.greater(table['revenue_growth'], 70),
                pc.is_in(table['stage'], value_set=pa.array(stages))
            )
            filtered = table.filter(mask)

            feed = filtered.select(['name', 'sector', 'revenue', 'revenue_growth', 'valuation'])

        elif agent_type == "portfolio_monitor":
            # Filter: all non-public companies
            mask = pc.not_equal(table['stage'], 'Public')
            filtered = table.filter(mask)

            feed = filtered.select(['name', 'revenue', 'revenue_growth', 'burn_rate', 'valuation'])

        else:
            feed = table

        print(f"✅ Feed created: {len(feed)} companies")

        # Convert to dictionary format for agents
        return {
            'companies': feed.to_pylist(),
            'count': len(feed),
            'timestamp': datetime.now().isoformat()
        }

def demo():
    """Demo Apache Arrow capabilities"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║         NEWCO APACHE ARROW DATA PROCESSOR                    ║
╚═══════════════════════════════════════════════════════════════╝
""")

    if not ARROW_AVAILABLE:
        print("❌ Apache Arrow not installed")
        print("")
        print("Install with:")
        print("  pip install pyarrow")
        return

    processor = ArrowDataProcessor()

    # Load data
    json_file = os.path.join(DATA_DIR, "pe_vc_data.json")
    if not os.path.exists(json_file):
        print(f"❌ Data file not found: {json_file}")
        print("Run data scraper first:")
        print("  cd /Users/rufio/NEWCO/data-scraper && python3 pe_vc_scraper.py")
        return

    table = processor.load_from_json(json_file)

    # Save to Parquet
    processor.save_to_parquet(table, "companies.parquet")

    # Load from Parquet (much faster for large datasets)
    table = processor.load_from_parquet("companies.parquet")

    # Filter high-growth companies
    print("")
    filtered = processor.filter_companies(table, {
        'revenue_growth': {'op': '>', 'value': 50}
    })

    # Calculate metrics
    print("")
    metrics = processor.aggregate_metrics(table)
    print("")
    print("Aggregate Metrics:")
    for key, value in metrics.items():
        if isinstance(value, (int, float)):
            print(f"  {key}: {value:,.0f}")
        else:
            print(f"  {key}: {value}")

    # Benchmark performance
    benchmark = processor.benchmark_performance(json_file)

    # Create agent feeds
    print("")
    ipo_feed = processor.create_agent_feed(table, "ipo_predictor")
    deal_feed = processor.create_agent_feed(table, "deal_scout")
    portfolio_feed = processor.create_agent_feed(table, "portfolio_monitor")

    print("""
╔═══════════════════════════════════════════════════════════════╗
║                    DEMO COMPLETE! ✅                         ║
╚═══════════════════════════════════════════════════════════════╝

🚀 Apache Arrow Benefits:

1. Performance:
   • {speedup:.2f}x faster than pandas
   • Zero-copy data sharing
   • Columnar memory format

2. Scalability:
   • Handles billions of rows
   • Efficient memory usage
   • Streaming support

3. Interoperability:
   • Works with Python, R, C++, Java
   • Parquet file format
   • Cross-language data sharing

4. Agent Integration:
   • Fast data feeds to all agents
   • Real-time filtering and aggregation
   • Optimized memory footprint

📊 Integration:

Update data_feed_manager.py to use Arrow:

```python
from arrow_data_processor import ArrowDataProcessor

processor = ArrowDataProcessor()
table = processor.load_from_parquet("companies.parquet")
feed = processor.create_agent_feed(table, "ipo_predictor")
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""".format(speedup=benchmark['speedup']))

if __name__ == "__main__":
    demo()
