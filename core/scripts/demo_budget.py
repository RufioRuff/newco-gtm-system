#!/usr/bin/env python3
"""
Demo Budget Data

Creates sample budget and actual spending data for testing
"""

from financial_modeling import FinancialModeler
from datetime import datetime

def create_demo_budget():
    """Create sample budget and actuals"""
    modeler = FinancialModeler()

    current_year = datetime.now().year

    print("Creating demo budget data...")

    # Budget for current year
    budget_items = [
        ('Salaries & Benefits', 1200000),
        ('Office & Facilities', 150000),
        ('Travel & Entertainment', 100000),
        ('Professional Services', 200000),
        ('Technology & Software', 75000),
        ('Marketing & PR', 50000),
        ('Insurance & Legal', 100000),
        ('Due Diligence Costs', 300000),
        ('Board & Governance', 75000),
        ('Other Operating', 50000)
    ]

    for category, amount in budget_items:
        modeler.add_budget(current_year, category, amount)

    # Actuals (2 months of data)
    # Month 1 - mostly on track
    month1_actuals = [
        ('Salaries & Benefits', 100000),
        ('Office & Facilities', 12500),
        ('Travel & Entertainment', 7500),
        ('Professional Services', 15000),
        ('Technology & Software', 6000),
        ('Marketing & PR', 3500),
        ('Insurance & Legal', 8000),
        ('Due Diligence Costs', 20000),
        ('Board & Governance', 5000),
        ('Other Operating', 3000)
    ]

    for category, amount in month1_actuals:
        modeler.add_actual(1, current_year, category, amount)

    # Month 2 - some overspending in travel and DD
    month2_actuals = [
        ('Salaries & Benefits', 102000),
        ('Office & Facilities', 13000),
        ('Travel & Entertainment', 15000),  # Over budget
        ('Professional Services', 18000),
        ('Technology & Software', 6200),
        ('Marketing & PR', 4000),
        ('Insurance & Legal', 8500),
        ('Due Diligence Costs', 45000),  # Over budget (active DD)
        ('Board & Governance', 6000),
        ('Other Operating', 4000)
    ]

    for category, amount in month2_actuals:
        modeler.add_actual(2, current_year, category, amount)

    print(f"\n✓ Created budget for {current_year}")
    print(f"✓ Added 2 months of actuals\n")
    print("Try: ./scripts/newco_cli.py finance variance")

if __name__ == '__main__':
    create_demo_budget()
