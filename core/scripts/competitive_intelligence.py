#!/usr/bin/env python3
"""
Competitive Intelligence - Market Analysis & Competitor Tracking

Tracks competitors, manager market, and industry benchmarks:
- Competitor fund tracking (other public VC vehicles)
- Manager market mapping (emerging managers universe)
- LP overlap analysis
- Fee structure benchmarking
- Performance comparisons
"""

import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
INTEL_DIR = DATA_DIR / "intelligence"


class CompetitiveIntelligence:
    """Competitive intelligence and market analysis"""

    def __init__(self):
        self.competitors_file = INTEL_DIR / "competitors.csv"
        self.manager_universe_file = INTEL_DIR / "manager_universe.csv"
        self.fee_benchmarks_file = INTEL_DIR / "fee_benchmarks.csv"
        self.lp_overlap_file = INTEL_DIR / "lp_overlap.csv"
        self.market_data_file = INTEL_DIR / "market_data.csv"
        self._initialize_files()

    def _initialize_files(self):
        """Initialize competitive intelligence files"""
        INTEL_DIR.mkdir(parents=True, exist_ok=True)

        if not self.competitors_file.exists():
            self.competitors_file.write_text(
                "competitor_id,name,type,structure,aum,nav_per_share,premium_discount,"
                "management_fee,incentive_fee,ticker,website,strategy,geography,focus,notes\n"
            )

        if not self.manager_universe_file.exists():
            self.manager_universe_file.write_text(
                "manager_id,firm_name,fund_name,fund_size,vintage,stage_focus,sector_focus,"
                "geography,lead_gp,gp_background,fundraising_status,close_date,min_check,max_check,"
                "strategy_description,competitive_positioning,our_status,notes\n"
            )

        if not self.fee_benchmarks_file.exists():
            self.fee_benchmarks_file.write_text(
                "vehicle_type,name,management_fee_rate,management_fee_basis,carry_rate,"
                "hurdle_rate,catch_up,gp_commitment,fund_size,notes\n"
            )

        if not self.lp_overlap_file.exists():
            self.lp_overlap_file.write_text(
                "lp_name,lp_type,our_investor,competitor_investors,total_vc_allocation,"
                "allocation_to_fofs,strategy_preference,decision_maker,last_contact,notes\n"
            )

        if not self.market_data_file.exists():
            self.market_data_file.write_text(
                "date,metric,value,source,notes\n"
            )

    def add_competitor(self, name, type, structure='Publicly Traded', aum=0,
                      management_fee=0, incentive_fee=0, ticker='', strategy='', notes=''):
        """Add competitor to tracking"""
        competitors = self._load_csv(self.competitors_file)

        competitor_id = f"COMP{len(competitors) + 1:03d}"

        competitor = {
            'competitor_id': competitor_id,
            'name': name,
            'type': type,
            'structure': structure,
            'aum': str(aum),
            'nav_per_share': '',
            'premium_discount': '',
            'management_fee': str(management_fee),
            'incentive_fee': str(incentive_fee),
            'ticker': ticker,
            'website': '',
            'strategy': strategy,
            'geography': 'US',
            'focus': '',
            'notes': notes
        }

        competitors.append(competitor)
        self._save_csv(self.competitors_file, competitors)

        print(f"✓ Added competitor: {name} ({competitor_id})")
        return competitor_id

    def add_manager_to_universe(self, firm_name, fund_name, fund_size, vintage,
                                stage_focus='', sector_focus='', lead_gp='',
                                fundraising_status='Open', our_status='Tracking'):
        """Add manager to universe tracking"""
        managers = self._load_csv(self.manager_universe_file)

        manager_id = f"UNIV{len(managers) + 1:04d}"

        manager = {
            'manager_id': manager_id,
            'firm_name': firm_name,
            'fund_name': fund_name,
            'fund_size': str(fund_size),
            'vintage': str(vintage),
            'stage_focus': stage_focus,
            'sector_focus': sector_focus,
            'geography': 'US',
            'lead_gp': lead_gp,
            'gp_background': '',
            'fundraising_status': fundraising_status,
            'close_date': '',
            'min_check': '',
            'max_check': '',
            'strategy_description': '',
            'competitive_positioning': '',
            'our_status': our_status,
            'notes': ''
        }

        managers.append(manager)
        self._save_csv(self.manager_universe_file, managers)

        print(f"✓ Added to universe: {firm_name} - {fund_name} ({manager_id})")
        return manager_id

    def get_competitor_landscape(self):
        """Get competitive landscape overview"""
        competitors = self._load_csv(self.competitors_file)

        landscape = {
            'total_competitors': len(competitors),
            'by_type': defaultdict(int),
            'by_structure': defaultdict(int),
            'total_aum': 0,
            'avg_mgmt_fee': 0,
            'competitors': []
        }

        total_aum = 0
        total_fee = 0
        fee_count = 0

        for comp in competitors:
            landscape['by_type'][comp['type']] += 1
            landscape['by_structure'][comp['structure']] += 1

            if comp['aum']:
                aum = float(comp['aum'])
                total_aum += aum

            if comp['management_fee']:
                fee = float(comp['management_fee'])
                total_fee += fee
                fee_count += 1

            landscape['competitors'].append({
                'id': comp['competitor_id'],
                'name': comp['name'],
                'type': comp['type'],
                'structure': comp['structure'],
                'aum': float(comp['aum']) if comp['aum'] else 0,
                'mgmt_fee': float(comp['management_fee']) if comp['management_fee'] else 0,
                'ticker': comp['ticker'],
                'strategy': comp['strategy']
            })

        landscape['total_aum'] = total_aum
        landscape['avg_mgmt_fee'] = total_fee / fee_count if fee_count > 0 else 0
        landscape['by_type'] = dict(landscape['by_type'])
        landscape['by_structure'] = dict(landscape['by_structure'])

        return landscape

    def show_competitor_landscape(self):
        """Display competitive landscape"""
        landscape = self.get_competitor_landscape()

        print("\n" + "="*80)
        print("COMPETITIVE LANDSCAPE")
        print("="*80)

        print(f"\n📊 Market Overview")
        print(f"  Total Competitors: {landscape['total_competitors']}")
        print(f"  Total AUM: ${landscape['total_aum']:,.0f}")
        print(f"  Avg Management Fee: {landscape['avg_mgmt_fee']:.2f}%")

        print(f"\n🏢 By Type:")
        for type_name, count in sorted(landscape['by_type'].items(), key=lambda x: -x[1]):
            print(f"  • {type_name:<30} {count:>3}")

        print(f"\n🏗️  By Structure:")
        for structure, count in sorted(landscape['by_structure'].items(), key=lambda x: -x[1]):
            print(f"  • {structure:<30} {count:>3}")

        print(f"\n📋 Competitors:")
        print(f"{'Name':<35} {'Type':<25} {'AUM':<15} {'Mgmt Fee'}")
        print("-"*80)

        for comp in sorted(landscape['competitors'], key=lambda x: -x['aum']):
            print(f"{comp['name']:<35} {comp['type']:<25} "
                  f"${comp['aum']:>13,.0f} {comp['mgmt_fee']:>6.2f}%")

        print("\n" + "="*80 + "\n")

    def get_manager_universe(self, filters=None):
        """Get manager universe with optional filters"""
        managers = self._load_csv(self.manager_universe_file)

        if filters:
            # Apply filters
            if 'stage_focus' in filters:
                managers = [m for m in managers if m['stage_focus'] == filters['stage_focus']]
            if 'sector_focus' in filters:
                managers = [m for m in managers if m['sector_focus'] == filters['sector_focus']]
            if 'fundraising_status' in filters:
                managers = [m for m in managers if m['fundraising_status'] == filters['fundraising_status']]
            if 'our_status' in filters:
                managers = [m for m in managers if m['our_status'] == filters['our_status']]

        return managers

    def show_manager_universe(self, filters=None):
        """Display manager universe"""
        managers = self.get_manager_universe(filters)

        print("\n" + "="*80)
        print("MANAGER UNIVERSE")
        if filters:
            print(f"Filters: {filters}")
        print("="*80)

        # Summary stats
        by_stage = defaultdict(int)
        by_sector = defaultdict(int)
        by_status = defaultdict(int)
        total_size = 0

        for manager in managers:
            if manager['stage_focus']:
                by_stage[manager['stage_focus']] += 1
            if manager['sector_focus']:
                by_sector[manager['sector_focus']] += 1
            if manager['our_status']:
                by_status[manager['our_status']] += 1
            if manager['fund_size']:
                total_size += float(manager['fund_size'])

        print(f"\n📊 Universe Stats")
        print(f"  Total Managers: {len(managers)}")
        print(f"  Total Fund Size: ${total_size:,.0f}")
        print(f"  Average Fund Size: ${total_size/len(managers):,.0f}" if managers else "  Average Fund Size: $0")

        print(f"\n🎯 By Stage:")
        for stage, count in sorted(by_stage.items(), key=lambda x: -x[1]):
            print(f"  • {stage:<20} {count:>3}")

        print(f"\n🏭 By Sector:")
        for sector, count in sorted(by_sector.items(), key=lambda x: -x[1]):
            print(f"  • {sector:<20} {count:>3}")

        print(f"\n📍 Our Status:")
        for status, count in sorted(by_status.items(), key=lambda x: -x[1]):
            print(f"  • {status:<20} {count:>3}")

        # List managers
        if len(managers) <= 20:
            print(f"\n📋 Managers:")
            print(f"{'Firm':<30} {'Fund':<25} {'Size':<12} {'Stage':<15} {'Status'}")
            print("-"*80)

            for mgr in managers:
                size = float(mgr['fund_size']) if mgr['fund_size'] else 0
                print(f"{mgr['firm_name']:<30} {mgr['fund_name']:<25} "
                      f"${size:>10,.0f} {mgr['stage_focus']:<15} {mgr['our_status']}")
        else:
            print(f"\n(Showing summary only - {len(managers)} managers)")

        print("\n" + "="*80 + "\n")

    def fee_benchmark_analysis(self):
        """Analyze fee structures across market"""
        benchmarks = self._load_csv(self.fee_benchmarks_file)

        if not benchmarks:
            print("No fee benchmark data available")
            return None

        analysis = {
            'count': len(benchmarks),
            'by_vehicle_type': defaultdict(list),
            'mgmt_fees': [],
            'carry_rates': []
        }

        for benchmark in benchmarks:
            vehicle_type = benchmark['vehicle_type']
            analysis['by_vehicle_type'][vehicle_type].append(benchmark)

            if benchmark['management_fee_rate']:
                analysis['mgmt_fees'].append(float(benchmark['management_fee_rate']))

            if benchmark['carry_rate']:
                analysis['carry_rates'].append(float(benchmark['carry_rate']))

        # Calculate statistics
        if analysis['mgmt_fees']:
            analysis['avg_mgmt_fee'] = sum(analysis['mgmt_fees']) / len(analysis['mgmt_fees'])
            analysis['min_mgmt_fee'] = min(analysis['mgmt_fees'])
            analysis['max_mgmt_fee'] = max(analysis['mgmt_fees'])
        else:
            analysis['avg_mgmt_fee'] = 0
            analysis['min_mgmt_fee'] = 0
            analysis['max_mgmt_fee'] = 0

        if analysis['carry_rates']:
            analysis['avg_carry'] = sum(analysis['carry_rates']) / len(analysis['carry_rates'])
        else:
            analysis['avg_carry'] = 0

        analysis['by_vehicle_type'] = dict(analysis['by_vehicle_type'])

        return analysis

    def show_fee_benchmarks(self):
        """Display fee benchmark analysis"""
        analysis = self.fee_benchmark_analysis()

        if not analysis:
            return

        print("\n" + "="*80)
        print("FEE STRUCTURE BENCHMARKS")
        print("="*80)

        print(f"\n📊 Market Statistics")
        print(f"  Vehicles Analyzed: {analysis['count']}")
        print(f"  Avg Management Fee: {analysis['avg_mgmt_fee']:.2f}%")
        print(f"  Range: {analysis['min_mgmt_fee']:.2f}% - {analysis['max_mgmt_fee']:.2f}%")
        print(f"  Avg Carry: {analysis['avg_carry']:.1f}%")

        print(f"\n💰 Fee Structures by Vehicle Type:")

        benchmarks = self._load_csv(self.fee_benchmarks_file)
        for benchmark in benchmarks:
            print(f"\n{benchmark['name']}")
            print(f"  Type: {benchmark['vehicle_type']}")
            if benchmark['management_fee_rate']:
                print(f"  Management Fee: {float(benchmark['management_fee_rate']):.2f}% on {benchmark['management_fee_basis']}")
            if benchmark['carry_rate']:
                print(f"  Carry: {float(benchmark['carry_rate']):.1f}%")
            if benchmark['hurdle_rate']:
                print(f"  Hurdle Rate: {float(benchmark['hurdle_rate']):.1f}%")
            if benchmark['fund_size']:
                print(f"  Fund Size: ${float(benchmark['fund_size']):,.0f}")

        print("\n" + "="*80 + "\n")

    def lp_overlap_analysis(self):
        """Analyze LP overlap with competitors"""
        overlaps = self._load_csv(self.lp_overlap_file)

        analysis = {
            'total_lps': len(overlaps),
            'our_investors': 0,
            'competitor_overlap': 0,
            'exclusive_lps': 0,
            'by_type': defaultdict(int),
            'high_overlap_lps': []
        }

        for lp in overlaps:
            analysis['by_type'][lp['lp_type']] += 1

            if lp['our_investor'].lower() == 'yes':
                analysis['our_investors'] += 1

            if lp['competitor_investors']:
                competitors = lp['competitor_investors'].split(',')
                overlap_count = len(competitors)
                analysis['competitor_overlap'] += 1

                if overlap_count >= 2:
                    analysis['high_overlap_lps'].append({
                        'name': lp['lp_name'],
                        'type': lp['lp_type'],
                        'competitors': competitors,
                        'overlap_count': overlap_count
                    })
            else:
                analysis['exclusive_lps'] += 1

        analysis['by_type'] = dict(analysis['by_type'])

        return analysis

    def show_lp_overlap(self):
        """Display LP overlap analysis"""
        analysis = self.lp_overlap_analysis()

        print("\n" + "="*80)
        print("LP OVERLAP ANALYSIS")
        print("="*80)

        print(f"\n📊 LP Universe")
        print(f"  Total LPs Tracked: {analysis['total_lps']}")
        print(f"  Our Investors: {analysis['our_investors']}")
        print(f"  Competitor Overlap: {analysis['competitor_overlap']}")
        print(f"  Exclusive to Us: {analysis['exclusive_lps']}")

        print(f"\n🏢 By LP Type:")
        for lp_type, count in sorted(analysis['by_type'].items(), key=lambda x: -x[1]):
            print(f"  • {lp_type:<30} {count:>3}")

        if analysis['high_overlap_lps']:
            print(f"\n⚠️  High Overlap LPs (invested in 2+ competitors):")
            for lp in analysis['high_overlap_lps']:
                print(f"\n  {lp['name']} ({lp['type']})")
                print(f"    Also invested in: {', '.join(lp['competitors'])}")

        print("\n" + "="*80 + "\n")

    def competitive_positioning_matrix(self):
        """Create competitive positioning matrix"""
        competitors = self._load_csv(self.competitors_file)

        # Define positioning axes
        # X-axis: Fee structure (low to high)
        # Y-axis: Focus (broad to niche)

        matrix = []

        for comp in competitors:
            mgmt_fee = float(comp['management_fee']) if comp['management_fee'] else 1.25

            # Classify focus breadth
            strategy = comp['strategy'].lower()
            if 'emerging' in strategy or 'seed' in strategy or 'early' in strategy:
                focus_score = 8  # Niche
            elif 'growth' in strategy:
                focus_score = 6
            elif 'diversified' in strategy or 'multi' in strategy:
                focus_score = 3  # Broad
            else:
                focus_score = 5  # Middle

            matrix.append({
                'name': comp['name'],
                'type': comp['type'],
                'fee': mgmt_fee,
                'focus': focus_score,
                'aum': float(comp['aum']) if comp['aum'] else 0,
                'strategy': comp['strategy']
            })

        return matrix

    def show_positioning_matrix(self):
        """Display competitive positioning"""
        matrix = self.competitive_positioning_matrix()

        print("\n" + "="*80)
        print("COMPETITIVE POSITIONING MATRIX")
        print("="*80)

        print(f"\n📍 Positioning (Fee Structure vs Focus)")
        print(f"\nY-axis: Focus (1=Broad, 10=Niche)")
        print(f"X-axis: Management Fee (%)\n")

        # Sort by focus (highest to lowest) then fee
        sorted_matrix = sorted(matrix, key=lambda x: (-x['focus'], x['fee']))

        print(f"{'Name':<35} {'Fee':<8} {'Focus':<8} {'Strategy'}")
        print("-"*80)

        for comp in sorted_matrix:
            focus_label = 'Niche' if comp['focus'] >= 7 else 'Mid' if comp['focus'] >= 4 else 'Broad'
            print(f"{comp['name']:<35} {comp['fee']:>6.2f}% {focus_label:<8} {comp['strategy'][:30]}")

        print("\n💡 Strategic Insights:")
        print("  • NEWCO (1.25% fee, emerging manager focus) = Niche/Premium")
        print("  • Lower fees = More competitive on price")
        print("  • Niche focus = Differentiation")
        print("  • Broad diversified = Commodity")

        print("\n" + "="*80 + "\n")

    def add_market_data(self, metric, value, source='', notes=''):
        """Log market data point"""
        data = self._load_csv(self.market_data_file)

        data.append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'metric': metric,
            'value': str(value),
            'source': source,
            'notes': notes
        })

        self._save_csv(self.market_data_file, data)
        print(f"✓ Logged market data: {metric} = {value}")

    def get_market_trends(self, metric=None):
        """Get market trend data"""
        data = self._load_csv(self.market_data_file)

        if metric:
            data = [d for d in data if d['metric'] == metric]

        # Group by metric
        trends = defaultdict(list)
        for point in data:
            trends[point['metric']].append({
                'date': point['date'],
                'value': float(point['value']) if point['value'] else 0,
                'source': point['source']
            })

        return dict(trends)

    def show_market_trends(self):
        """Display market trends"""
        trends = self.get_market_trends()

        print("\n" + "="*80)
        print("MARKET TRENDS")
        print("="*80)

        if not trends:
            print("\nNo market data available")
            print("\n" + "="*80 + "\n")
            return

        for metric, datapoints in sorted(trends.items()):
            print(f"\n📈 {metric}")
            # Sort by date
            sorted_points = sorted(datapoints, key=lambda x: x['date'])

            for point in sorted_points[-5:]:  # Last 5 data points
                print(f"  {point['date']}: {point['value']:>12,.0f} ({point['source']})")

        print("\n" + "="*80 + "\n")

    def _load_csv(self, filepath):
        """Load CSV file"""
        data = []
        if filepath.exists():
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)
        return data

    def _save_csv(self, filepath, data):
        """Save CSV file"""
        if not data:
            return

        fieldnames = data[0].keys()
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


if __name__ == '__main__':
    intel = CompetitiveIntelligence()
    intel.show_competitor_landscape()
