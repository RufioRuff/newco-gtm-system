#!/usr/bin/env python3
"""
Social Network Analysis Engine
Grounded in academic social network theory

Key Concepts Implemented:
- Centrality Measures (Freeman 1978, Bonacich 1987)
- Structural Holes & Brokerage (Burt 1992, 2004)
- Tie Strength (Granovetter 1973)
- Network Influence & Diffusion (Watts & Strogatz 1998)
- Homophily (McPherson et al. 2001)
- Small World Networks (Milgram 1967, Watts 1999)
"""

import csv
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import json
import math

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


class NetworkAnalysisEngine:
    """
    Social network analysis engine for contact relationships

    Based on foundational research in social network theory:
    - Freeman, L. (1978). Centrality in social networks
    - Granovetter, M. (1973). The strength of weak ties
    - Burt, R. (1992). Structural holes
    - Watts, D. & Strogatz, S. (1998). Small-world networks
    """

    def __init__(self):
        self.contacts_file = DATA_DIR / "contacts.csv"
        self.relationships_file = DATA_DIR / "relationships.csv"
        self.interactions_file = DATA_DIR / "interactions.csv"

        # Initialize relationships file if it doesn't exist
        if not self.relationships_file.exists():
            self.relationships_file.write_text("contact_id_1,contact_id_2,relationship_type,strength,notes,mutual_connections\n")

    def load_contacts(self):
        """Load all contacts"""
        contacts = []
        if self.contacts_file.exists():
            with open(self.contacts_file, 'r') as f:
                reader = csv.DictReader(f)
                contacts = list(reader)
        return contacts

    def load_relationships(self):
        """Load all relationships between contacts"""
        relationships = []
        if self.relationships_file.exists():
            with open(self.relationships_file, 'r') as f:
                reader = csv.DictReader(f)
                relationships = list(reader)
        return relationships

    def load_interactions(self):
        """Load all interactions"""
        interactions = []
        if self.interactions_file.exists():
            with open(self.interactions_file, 'r') as f:
                reader = csv.DictReader(f)
                interactions = list(reader)
        return interactions

    def build_network_graph(self):
        """
        Build network graph from contacts and relationships
        Returns adjacency list representation
        """
        graph = defaultdict(list)
        relationships = self.load_relationships()

        for rel in relationships:
            id1 = rel['contact_id_1']
            id2 = rel['contact_id_2']
            strength = float(rel.get('strength', 1.0))

            graph[id1].append({'node': id2, 'strength': strength})
            graph[id2].append({'node': id1, 'strength': strength})

        return graph

    def calculate_degree_centrality(self):
        """
        Degree Centrality (Freeman 1978)

        Measures the number of direct connections a node has.
        In GTM context: Identifies contacts with most direct relationships.

        High degree = well-connected individual who knows many people
        """
        graph = self.build_network_graph()
        contacts = self.load_contacts()

        centrality = {}
        for contact in contacts:
            contact_id = contact['id']
            degree = len(graph.get(contact_id, []))
            centrality[contact_id] = {
                'name': contact['name'],
                'company': contact['company'],
                'degree': degree,
                'normalized_degree': degree / max(1, len(contacts) - 1)
            }

        return sorted(centrality.values(), key=lambda x: x['degree'], reverse=True)

    def calculate_betweenness_centrality(self):
        """
        Betweenness Centrality (Freeman 1977)

        Measures how often a node lies on shortest paths between other nodes.
        In GTM context: Identifies BROKERS who connect different groups.

        High betweenness = gatekeeper, bridge between communities
        Critical for network multiplier effect!

        Simplified approximation using ego networks
        """
        graph = self.build_network_graph()
        contacts = self.load_contacts()

        betweenness = {}

        for contact in contacts:
            contact_id = contact['id']
            neighbors = graph.get(contact_id, [])

            # Count how many neighbors are NOT connected to each other
            # (indicates this person bridges otherwise disconnected groups)
            bridges = 0
            for i, n1 in enumerate(neighbors):
                for n2 in neighbors[i+1:]:
                    # Check if n1 and n2 are connected
                    n1_neighbors = [n['node'] for n in graph.get(n1['node'], [])]
                    if n2['node'] not in n1_neighbors:
                        bridges += 1

            betweenness[contact_id] = {
                'name': contact['name'],
                'company': contact['company'],
                'bridges': bridges,
                'broker_score': bridges / max(1, len(neighbors)) if neighbors else 0
            }

        return sorted(betweenness.values(), key=lambda x: x['bridges'], reverse=True)

    def calculate_structural_holes(self):
        """
        Structural Holes Theory (Burt 1992, 2004)

        "The people who stand near the holes in a social structure
        are at a higher risk of having good ideas"

        Measures network constraint - low constraint = access to structural holes

        In GTM context: Identifies contacts who span different networks
        and have non-redundant connections (network multipliers!)

        Constraint = redundancy in ego network
        Low constraint = many non-redundant contacts = VALUABLE
        """
        graph = self.build_network_graph()
        contacts = self.load_contacts()

        structural_holes = {}

        for contact in contacts:
            contact_id = contact['id']
            neighbors = graph.get(contact_id, [])

            if not neighbors:
                continue

            # Calculate network constraint (Burt's formula)
            # Constraint is HIGH when your contacts all know each other
            # Constraint is LOW when your contacts are disconnected (structural holes!)

            total_constraint = 0
            for neighbor in neighbors:
                neighbor_id = neighbor['node']
                neighbor_neighbors = set(n['node'] for n in graph.get(neighbor_id, []))

                # Count mutual connections
                your_neighbors = set(n['node'] for n in neighbors)
                mutual = your_neighbors.intersection(neighbor_neighbors)

                # Constraint from this neighbor
                direct = 1 / len(neighbors)
                indirect = sum(1 / len(neighbors) * (1 / len(graph.get(m, [{}])))
                              for m in mutual if m != contact_id)

                constraint_i = (direct + indirect) ** 2
                total_constraint += constraint_i

            avg_constraint = total_constraint / len(neighbors)

            # Lower constraint = better access to structural holes
            structural_holes[contact_id] = {
                'name': contact['name'],
                'company': contact['company'],
                'constraint': avg_constraint,
                'structural_holes_access': 1 - avg_constraint,  # Inverse for readability
                'non_redundant_contacts': len(neighbors)
            }

        return sorted(structural_holes.values(),
                     key=lambda x: x['structural_holes_access'], reverse=True)

    def analyze_tie_strength(self):
        """
        Tie Strength Theory (Granovetter 1973)
        "The Strength of Weak Ties"

        Strong ties: frequent interaction, emotional closeness, reciprocity
        Weak ties: infrequent interaction, but bridge to new networks

        PARADOX: Weak ties are MORE valuable for:
        - Job searches
        - Novel information
        - Accessing different social circles

        In GTM context:
        - Strong ties = trusted relationships, easier warm intros
        - Weak ties = access to NEW networks, broader reach

        Calculate tie strength based on:
        - Interaction frequency
        - Recency
        - Reciprocity
        - Mutual connections
        """
        relationships = self.load_relationships()
        interactions = self.load_interactions()
        contacts = self.load_contacts()

        # Count interactions per contact pair
        pair_interactions = defaultdict(int)
        for interaction in interactions:
            pair_interactions[interaction['contact_id']] += 1

        tie_analysis = []

        for rel in relationships:
            id1 = rel['contact_id_1']
            id2 = rel['contact_id_2']

            # Get contact names
            c1 = next((c for c in contacts if c['id'] == id1), {})
            c2 = next((c for c in contacts if c['id'] == id2), {})

            # Calculate tie strength (0-1 scale)
            strength_score = float(rel.get('strength', 0.5))

            # Interaction frequency component
            interactions_count = pair_interactions.get(id1, 0) + pair_interactions.get(id2, 0)
            frequency_score = min(interactions_count / 10, 1.0)  # Normalize to 0-1

            # Combined tie strength
            tie_strength = (strength_score + frequency_score) / 2

            # Classify tie
            if tie_strength > 0.7:
                tie_type = "Strong Tie"
                value = "Trusted relationship, good for warm intros"
            elif tie_strength > 0.4:
                tie_type = "Medium Tie"
                value = "Developing relationship"
            else:
                tie_type = "Weak Tie"
                value = "Access to new networks, novel information"

            tie_analysis.append({
                'contact_1': c1.get('name', 'Unknown'),
                'contact_2': c2.get('name', 'Unknown'),
                'tie_strength': tie_strength,
                'tie_type': tie_type,
                'strategic_value': value
            })

        return sorted(tie_analysis, key=lambda x: x['tie_strength'], reverse=True)

    def calculate_network_influence_score(self):
        """
        Network Influence (Bonacich 1987, PageRank-style)

        Eigenvector Centrality: You're important if you're connected to important people

        In GTM context: Identifies contacts whose influence extends
        through their network (not just direct connections)

        Power iteration method for eigenvector centrality
        """
        graph = self.build_network_graph()
        contacts = self.load_contacts()

        if not contacts:
            return []

        # Initialize all scores to 1
        scores = {c['id']: 1.0 for c in contacts}

        # Power iteration (simplified PageRank)
        for iteration in range(20):  # 20 iterations usually sufficient
            new_scores = {}

            for contact in contacts:
                contact_id = contact['id']
                neighbors = graph.get(contact_id, [])

                # Score = sum of neighbor scores / their degree
                score = 0
                for neighbor in neighbors:
                    neighbor_id = neighbor['node']
                    neighbor_degree = len(graph.get(neighbor_id, []))
                    if neighbor_degree > 0:
                        score += scores[neighbor_id] / neighbor_degree

                new_scores[contact_id] = score

            # Normalize
            total = sum(new_scores.values())
            if total > 0:
                scores = {k: v / total * len(contacts) for k, v in new_scores.items()}

        # Build results
        influence_scores = []
        for contact in contacts:
            contact_id = contact['id']
            influence_scores.append({
                'name': contact['name'],
                'company': contact['company'],
                'tier': contact['tier'],
                'influence_score': scores[contact_id],
                'interpretation': 'High network influence' if scores[contact_id] > 1.5 else 'Standard influence'
            })

        return sorted(influence_scores, key=lambda x: x['influence_score'], reverse=True)

    def identify_network_multipliers(self):
        """
        Identify TRUE Network Multipliers using composite score

        Network multipliers have:
        1. High betweenness (brokers)
        2. Access to structural holes (non-redundant networks)
        3. High influence score (connected to influential people)
        4. Mix of strong and weak ties

        These are your MOST VALUABLE contacts for GTM!
        """
        betweenness = {b['name']: b['broker_score'] for b in self.calculate_betweenness_centrality()}
        structural = {s['name']: s['structural_holes_access'] for s in self.calculate_structural_holes()}
        influence = {i['name']: i['influence_score'] for i in self.calculate_network_influence_score()}

        contacts = self.load_contacts()
        multipliers = []

        for contact in contacts:
            name = contact['name']

            # Composite network multiplier score
            broker_score = betweenness.get(name, 0)
            holes_score = structural.get(name, 0)
            influence_score = influence.get(name, 0)

            # Weighted composite (betweenness and structural holes most important)
            composite = (
                broker_score * 0.4 +
                holes_score * 0.4 +
                (influence_score / 5) * 0.2  # Normalize influence
            )

            if composite > 0.1:  # Threshold for being a multiplier
                multipliers.append({
                    'name': name,
                    'company': contact['company'],
                    'tier': contact['tier'],
                    'multiplier_score': composite,
                    'broker_score': broker_score,
                    'structural_holes': holes_score,
                    'influence': influence_score,
                    'why_valuable': self._explain_multiplier_value(broker_score, holes_score, influence_score)
                })

        return sorted(multipliers, key=lambda x: x['multiplier_score'], reverse=True)

    def _explain_multiplier_value(self, broker, holes, influence):
        """Explain why this person is a network multiplier"""
        reasons = []

        if broker > 0.5:
            reasons.append("Bridges disconnected groups (broker)")
        if holes > 0.6:
            reasons.append("Access to non-redundant networks")
        if influence > 2:
            reasons.append("Connected to influential people")

        if not reasons:
            reasons.append("Developing network position")

        return ", ".join(reasons)

    def analyze_homophily(self):
        """
        Homophily Analysis (McPherson et al. 2001)
        "Birds of a feather flock together"

        Tendency for similar people to connect.
        In GTM context: Analyze if contacts cluster by:
        - Category (VCs connect with VCs)
        - Tier
        - Company type

        Insight: Breaking out of homophilous clusters = accessing new networks
        """
        relationships = self.load_relationships()
        contacts = self.load_contacts()

        # Build contact lookup
        contact_lookup = {c['id']: c for c in contacts}

        # Analyze category homophily
        same_category = 0
        different_category = 0

        for rel in relationships:
            c1 = contact_lookup.get(rel['contact_id_1'], {})
            c2 = contact_lookup.get(rel['contact_id_2'], {})

            if c1 and c2:
                if c1.get('category') == c2.get('category'):
                    same_category += 1
                else:
                    different_category += 1

        total = same_category + different_category
        if total > 0:
            homophily_index = same_category / total
        else:
            homophily_index = 0

        return {
            'homophily_index': homophily_index,
            'same_category_connections': same_category,
            'cross_category_connections': different_category,
            'interpretation': self._interpret_homophily(homophily_index)
        }

    def _interpret_homophily(self, index):
        """Interpret homophily index"""
        if index > 0.7:
            return "High homophily - network is clustered. Seek cross-category connections for broader reach."
        elif index > 0.5:
            return "Moderate homophily - some clustering present."
        else:
            return "Low homophily - diverse network with cross-category connections. Good for information flow!"

    def calculate_network_reach(self, contact_id, degrees=2):
        """
        Calculate network reach using degrees of separation
        Small World Theory (Milgram 1967)

        In GTM context: How many people can you reach through this contact?

        degrees=1: direct connections
        degrees=2: friends of friends (most valuable for intros)
        """
        graph = self.build_network_graph()
        contacts = self.load_contacts()

        visited = set()
        current_level = {contact_id}

        for degree in range(degrees):
            next_level = set()
            for node in current_level:
                if node not in visited:
                    visited.add(node)
                    neighbors = [n['node'] for n in graph.get(node, [])]
                    next_level.update(neighbors)
            current_level = next_level

        # Get contact details
        reachable_contacts = []
        for cid in visited:
            if cid != contact_id:
                contact = next((c for c in contacts if c['id'] == cid), None)
                if contact:
                    reachable_contacts.append({
                        'name': contact['name'],
                        'company': contact['company']
                    })

        return {
            'total_reach': len(reachable_contacts),
            'reachable_contacts': reachable_contacts[:50]  # Limit output
        }

    def show_network_analysis_report(self):
        """Show comprehensive network analysis report"""
        print("\n" + "="*80)
        print("SOCIAL NETWORK ANALYSIS REPORT")
        print("="*80)

        # Network Multipliers (most important!)
        print("\n🌟 NETWORK MULTIPLIERS (Critical for GTM)")
        print("─" * 80)
        multipliers = self.identify_network_multipliers()
        if multipliers:
            for i, m in enumerate(multipliers[:10], 1):
                print(f"\n{i}. {m['name']} ({m['company']})")
                print(f"   Multiplier Score: {m['multiplier_score']:.2f} | Tier: {m['tier']}")
                print(f"   Value: {m['why_valuable']}")
        else:
            print("No network data available. Add relationships to analyze network.")

        # Structural Holes
        print("\n\n💎 STRUCTURAL HOLES ACCESS (Non-Redundant Networks)")
        print("─" * 80)
        print("Theory: Contacts spanning structural holes provide access to")
        print("        non-overlapping networks = novel information & opportunities")
        holes = self.calculate_structural_holes()
        for i, h in enumerate(holes[:5], 1):
            print(f"{i}. {h['name']:<30} Access: {h['structural_holes_access']:.2f}")

        # Betweenness (Brokers)
        print("\n\n🌉 BROKERS (Bridge Different Groups)")
        print("─" * 80)
        print("Theory: High betweenness = gatekeeper between communities")
        betweenness = self.calculate_betweenness_centrality()
        for i, b in enumerate(betweenness[:5], 1):
            print(f"{i}. {b['name']:<30} Broker Score: {b['broker_score']:.2f}")

        # Network Influence
        print("\n\n⚡ NETWORK INFLUENCE (Connected to Influential People)")
        print("─" * 80)
        influence = self.calculate_network_influence_score()
        for i, inf in enumerate(influence[:5], 1):
            print(f"{i}. {inf['name']:<30} Influence: {inf['influence_score']:.2f}")

        # Homophily
        print("\n\n🔗 NETWORK HOMOPHILY")
        print("─" * 80)
        homophily = self.analyze_homophily()
        print(f"Homophily Index: {homophily['homophily_index']:.2f}")
        print(f"Same Category: {homophily['same_category_connections']} | Cross Category: {homophily['cross_category_connections']}")
        print(f"\n{homophily['interpretation']}")

        print("\n" + "="*80)
        print("\n💡 KEY INSIGHT: Focus on Network Multipliers for maximum GTM leverage!")
        print("   These contacts can open doors to entire networks, not just individuals.\n")

    def export_network_graph(self, output_file=None):
        """Export network in common graph formats for visualization"""
        if output_file is None:
            output_file = BASE_DIR / "reports" / "network_graph.json"

        graph = self.build_network_graph()
        contacts = self.load_contacts()

        # Build nodes and edges
        nodes = []
        for contact in contacts:
            nodes.append({
                'id': contact['id'],
                'name': contact['name'],
                'company': contact['company'],
                'tier': int(contact['tier']),
                'category': contact['category']
            })

        edges = []
        relationships = self.load_relationships()
        for rel in relationships:
            edges.append({
                'source': rel['contact_id_1'],
                'target': rel['contact_id_2'],
                'strength': float(rel.get('strength', 1.0))
            })

        network_data = {
            'nodes': nodes,
            'edges': edges,
            'metadata': {
                'total_nodes': len(nodes),
                'total_edges': len(edges),
                'generated': datetime.now().isoformat()
            }
        }

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(network_data, f, indent=2)

        print(f"✓ Network graph exported to {output_file}")
        return network_data


if __name__ == '__main__':
    network = NetworkAnalysisEngine()
    network.show_network_analysis_report()
