#!/usr/bin/env python3
"""
Demo Network Builder

Creates sample relationships to demonstrate network analysis capabilities.
Based on social network theory principles:
- Network multipliers (high betweenness)
- Structural holes
- Strong vs weak ties
"""

from relationship_manager import RelationshipManager

def build_demo_network():
    """Build a demo network to showcase network analysis"""

    rm = RelationshipManager()

    print("Building demo network with social network theory patterns...")
    print()

    # Bob Burlinson (ID 1) - Network Multiplier
    # Strong ties to platform gatekeepers
    rm.add_relationship('1', '2', 'worked_with', 0.8, 'Collaborated on deals')  # Bob -> Alistair

    # Bob has weak ties that bridge to other networks (structural holes)
    rm.add_relationship('1', '3', 'knows', 0.4, 'Met at conference')  # Bob -> Marie
    rm.add_relationship('1', '4', 'knows', 0.3, 'LinkedIn connection')  # Bob -> VC Partner

    # Alistair (ID 2) - Platform Gatekeeper
    # Connected within his tier (homophily)
    rm.add_relationship('2', '3', 'knows', 0.5, 'Professional relationship')  # Alistair -> Marie

    # Marie (ID 3) - Family Office CIO
    # Strong tie within family office network
    rm.add_relationship('3', '5', 'worked_with', 0.7, 'Co-investment')  # Marie -> Jessica

    # VC Partner (ID 4) - Bridge to VC network
    rm.add_relationship('4', '5', 'knows', 0.4, 'Industry events')  # VC Partner -> Jessica

    print("✓ Created relationships demonstrating:")
    print("  • Network multiplier pattern (Bob Burlinson)")
    print("  • Structural holes (Bob's weak ties to different networks)")
    print("  • Strong vs weak ties (Granovetter)")
    print("  • Homophily (similar people connecting)")
    print("  • Brokerage opportunities (bridging disconnected groups)")
    print()
    print("Run: ./scripts/newco_cli.py network analyze")
    print("To see the full network analysis!")

if __name__ == '__main__':
    build_demo_network()
