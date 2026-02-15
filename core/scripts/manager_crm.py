#!/usr/bin/env python3
"""
Manager CRM - Fund Manager Relationship Management

Separate from LP CRM - this tracks relationships with FUND MANAGERS
(the GPs whose funds we invest in)

Pipeline stages:
1. Sourced - Identified potential manager
2. Screening - Initial evaluation
3. Deep DD - Full due diligence
4. IC Review - Investment committee review
5. Committed - Invested in their fund
6. Passed - Decided not to invest (track for future)
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


class ManagerCRM:
    """CRM for fund manager relationships"""

    def __init__(self):
        self.managers_file = DATA_DIR / "fund_managers.csv"
        self.manager_interactions_file = DATA_DIR / "manager_interactions.csv"
        self.due_diligence_file = DATA_DIR / "due_diligence.csv"
        self.ic_decisions_file = DATA_DIR / "ic_decisions.csv"

        self._initialize_files()

    def _initialize_files(self):
        """Initialize manager CRM files"""
        if not self.managers_file.exists():
            self.managers_file.write_text(
                "manager_id,fund_name,gp_names,firm_name,stage_focus,sector_focus,geography,"
                "aum,fund_size,vintage_year,pipeline_stage,source,last_contact,next_action,"
                "priority,notes\n"
            )

        if not self.manager_interactions_file.exists():
            self.manager_interactions_file.write_text(
                "interaction_id,manager_id,date,type,subject,attendees,notes,outcome\n"
            )

        if not self.due_diligence_file.exists():
            self.due_diligence_file.write_text(
                "dd_id,manager_id,started_date,status,lead_analyst,"
                "initial_call,track_record_verified,references_completed,portfolio_visits,"
                "operations_review,legal_review,ic_memo_drafted,completed_date,notes\n"
            )

        if not self.ic_decisions_file.exists():
            self.ic_decisions_file.write_text(
                "ic_id,manager_id,ic_date,decision,vote_results,commitment_amount,"
                "fund_id,notes\n"
            )

    def add_manager(self, fund_name, gp_names, firm_name, stage_focus='',
                   sector_focus='', geography='US', pipeline_stage='Sourced',
                   source='', notes=''):
        """Add a fund manager to pipeline"""
        managers = self._load_csv(self.managers_file)

        manager_id = f"M{len(managers) + 1:03d}"

        manager = {
            'manager_id': manager_id,
            'fund_name': fund_name,
            'gp_names': gp_names,
            'firm_name': firm_name,
            'stage_focus': stage_focus,
            'sector_focus': sector_focus,
            'geography': geography,
            'aum': '',
            'fund_size': '',
            'vintage_year': '',
            'pipeline_stage': pipeline_stage,
            'source': source,
            'last_contact': datetime.now().strftime('%Y-%m-%d'),
            'next_action': '',
            'priority': 'Medium',
            'notes': notes
        }

        managers.append(manager)
        self._save_csv(self.managers_file, managers)

        print(f"✓ Added manager: {fund_name} ({manager_id})")
        print(f"  GPs: {gp_names}")
        print(f"  Stage: {pipeline_stage}")

        return manager_id

    def update_pipeline_stage(self, manager_id, new_stage, notes=''):
        """Move manager through pipeline"""
        managers = self._load_csv(self.managers_file)

        for manager in managers:
            if manager['manager_id'] == manager_id:
                old_stage = manager['pipeline_stage']
                manager['pipeline_stage'] = new_stage
                manager['last_contact'] = datetime.now().strftime('%Y-%m-%d')
                if notes:
                    manager['notes'] += f" | {notes}"

                self._save_csv(self.managers_file, managers)

                print(f"✓ Updated {manager['fund_name']}")
                print(f"  {old_stage} → {new_stage}")
                return True

        return False

    def log_manager_interaction(self, manager_id, interaction_type, subject,
                                attendees='', notes='', outcome=''):
        """Log interaction with fund manager"""
        interactions = self._load_csv(self.manager_interactions_file)

        interaction_id = f"MI{len(interactions) + 1:05d}"

        interaction = {
            'interaction_id': interaction_id,
            'manager_id': manager_id,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': interaction_type,
            'subject': subject,
            'attendees': attendees,
            'notes': notes,
            'outcome': outcome
        }

        interactions.append(interaction)
        self._save_csv(self.manager_interactions_file, interactions)

        # Update manager last contact
        managers = self._load_csv(self.managers_file)
        for manager in managers:
            if manager['manager_id'] == manager_id:
                manager['last_contact'] = datetime.now().strftime('%Y-%m-%d')
                self._save_csv(self.managers_file, managers)
                break

        return interaction_id

    def start_due_diligence(self, manager_id, lead_analyst):
        """Start due diligence process for a manager"""
        dd_items = self._load_csv(self.due_diligence_file)

        # Check if DD already exists
        for item in dd_items:
            if item['manager_id'] == manager_id and item['status'] != 'Completed':
                print(f"Due diligence already in progress for {manager_id}")
                return item['dd_id']

        dd_id = f"DD{len(dd_items) + 1:04d}"

        dd = {
            'dd_id': dd_id,
            'manager_id': manager_id,
            'started_date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'In Progress',
            'lead_analyst': lead_analyst,
            'initial_call': 'No',
            'track_record_verified': 'No',
            'references_completed': 'No',
            'portfolio_visits': 'No',
            'operations_review': 'No',
            'legal_review': 'No',
            'ic_memo_drafted': 'No',
            'completed_date': '',
            'notes': ''
        }

        dd_items.append(dd)
        self._save_csv(self.due_diligence_file, dd_items)

        # Update manager to Deep DD stage
        self.update_pipeline_stage(manager_id, 'Deep DD', f'DD started by {lead_analyst}')

        print(f"✓ Started due diligence: {dd_id}")
        print(f"  Lead Analyst: {lead_analyst}")

        return dd_id

    def update_dd_checklist(self, dd_id, **updates):
        """Update due diligence checklist"""
        dd_items = self._load_csv(self.due_diligence_file)

        for dd in dd_items:
            if dd['dd_id'] == dd_id:
                dd.update(updates)

                # Check if all items completed
                checklist_items = [
                    'initial_call', 'track_record_verified', 'references_completed',
                    'portfolio_visits', 'operations_review', 'legal_review', 'ic_memo_drafted'
                ]
                if all(dd.get(item) == 'Yes' for item in checklist_items):
                    dd['status'] = 'Completed'
                    dd['completed_date'] = datetime.now().strftime('%Y-%m-%d')

                self._save_csv(self.due_diligence_file, dd_items)
                return True

        return False

    def record_ic_decision(self, manager_id, decision, vote_results='',
                          commitment_amount=0, fund_id='', notes=''):
        """Record Investment Committee decision"""
        ic_decisions = self._load_csv(self.ic_decisions_file)

        ic_id = f"IC{len(ic_decisions) + 1:04d}"

        ic = {
            'ic_id': ic_id,
            'manager_id': manager_id,
            'ic_date': datetime.now().strftime('%Y-%m-%d'),
            'decision': decision,
            'vote_results': vote_results,
            'commitment_amount': str(commitment_amount),
            'fund_id': fund_id,
            'notes': notes
        }

        ic_decisions.append(ic)
        self._save_csv(self.ic_decisions_file, ic_decisions)

        # Update manager pipeline stage based on decision
        if decision == 'Approved':
            self.update_pipeline_stage(manager_id, 'Committed', f'IC approved: ${commitment_amount:,.0f}')
        elif decision == 'Declined':
            self.update_pipeline_stage(manager_id, 'Passed', 'IC declined')
        else:
            self.update_pipeline_stage(manager_id, 'IC Review', f'IC {decision}')

        print(f"✓ Recorded IC decision: {decision}")
        if commitment_amount > 0:
            print(f"  Commitment: ${commitment_amount:,.0f}")

        return ic_id

    def get_pipeline_summary(self):
        """Get summary of manager pipeline"""
        managers = self._load_csv(self.managers_file)

        summary = {
            'total': len(managers),
            'by_stage': defaultdict(int),
            'by_source': defaultdict(int),
            'by_stage_list': defaultdict(list)
        }

        for manager in managers:
            stage = manager['pipeline_stage']
            source = manager['source'] or 'Unknown'

            summary['by_stage'][stage] += 1
            summary['by_source'][source] += 1
            summary['by_stage_list'][stage].append(manager)

        return summary

    def show_pipeline_dashboard(self):
        """Display manager pipeline dashboard"""
        summary = self.get_pipeline_summary()

        print("\n" + "="*80)
        print("MANAGER PIPELINE DASHBOARD")
        print("="*80)

        print(f"\n📊 PIPELINE SUMMARY")
        print(f"  Total Managers: {summary['total']}")

        print(f"\n  By Stage:")
        stages = ['Sourced', 'Screening', 'Deep DD', 'IC Review', 'Committed', 'Passed']
        for stage in stages:
            count = summary['by_stage'].get(stage, 0)
            print(f"    • {stage:<15} {count:>3}")

        print(f"\n  By Source:")
        for source, count in sorted(summary['by_source'].items(), key=lambda x: -x[1]):
            print(f"    • {source:<25} {count:>3}")

        # Active DD
        dd_items = self._load_csv(self.due_diligence_file)
        active_dd = [dd for dd in dd_items if dd['status'] == 'In Progress']

        if active_dd:
            print(f"\n🔍 ACTIVE DUE DILIGENCE ({len(active_dd)})")
            for dd in active_dd:
                managers = self._load_csv(self.managers_file)
                manager = next((m for m in managers if m['manager_id'] == dd['manager_id']), None)
                if manager:
                    print(f"  • {manager['fund_name']:<30} Lead: {dd['lead_analyst']}")

        # Upcoming IC
        managers_in_ic = summary['by_stage_list'].get('IC Review', [])
        if managers_in_ic:
            print(f"\n⚖️  PENDING IC REVIEW ({len(managers_in_ic)})")
            for manager in managers_in_ic:
                print(f"  • {manager['fund_name']:<30} {manager['gp_names']}")

        print("\n" + "="*80 + "\n")

    def show_dd_status(self, manager_id):
        """Show due diligence status for a manager"""
        managers = self._load_csv(self.managers_file)
        manager = next((m for m in managers if m['manager_id'] == manager_id), None)

        if not manager:
            print(f"Manager {manager_id} not found")
            return

        dd_items = self._load_csv(self.due_diligence_file)
        dd = next((d for d in dd_items if d['manager_id'] == manager_id and d['status'] == 'In Progress'), None)

        print(f"\n{'='*70}")
        print(f"DUE DILIGENCE STATUS: {manager['fund_name']}")
        print(f"{'='*70}")

        if not dd:
            print("\nNo active due diligence")
            return

        print(f"\nDD ID: {dd['dd_id']}")
        print(f"Started: {dd['started_date']}")
        print(f"Lead Analyst: {dd['lead_analyst']}")
        print(f"Status: {dd['status']}")

        print(f"\nChecklist:")
        checklist = [
            ('Initial Call', dd['initial_call']),
            ('Track Record Verified', dd['track_record_verified']),
            ('References (3+ LPs)', dd['references_completed']),
            ('Portfolio Company Visits', dd['portfolio_visits']),
            ('Operations Review', dd['operations_review']),
            ('Legal Review (LPA)', dd['legal_review']),
            ('IC Memo Drafted', dd['ic_memo_drafted'])
        ]

        for item, status in checklist:
            icon = '✓' if status == 'Yes' else '☐'
            print(f"  {icon} {item}")

        if dd['notes']:
            print(f"\nNotes: {dd['notes']}")

        print(f"\n{'='*70}\n")

    def get_referral_analytics(self):
        """Analyze which referral sources are most effective"""
        managers = self._load_csv(self.managers_file)

        referrals = defaultdict(lambda: {'total': 0, 'committed': 0, 'passed': 0, 'active': 0})

        for manager in managers:
            source = manager['source'] or 'Unknown'
            stage = manager['pipeline_stage']

            referrals[source]['total'] += 1

            if stage == 'Committed':
                referrals[source]['committed'] += 1
            elif stage == 'Passed':
                referrals[source]['passed'] += 1
            else:
                referrals[source]['active'] += 1

        # Calculate conversion rates
        for source, data in referrals.items():
            if data['total'] > 0:
                data['conversion_rate'] = (data['committed'] / data['total']) * 100
            else:
                data['conversion_rate'] = 0

        return dict(referrals)

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
    crm = ManagerCRM()
    crm.show_pipeline_dashboard()
