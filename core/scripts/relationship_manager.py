#!/usr/bin/env python3
"""
Relationship Management System

Build and manage the social network graph of contacts.
Track who knows whom, relationship strength, and mutual connections.
"""

import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


class RelationshipManager:
    """Manage relationships between contacts"""

    def __init__(self):
        self.contacts_file = DATA_DIR / "contacts.csv"
        self.relationships_file = DATA_DIR / "relationships.csv"

        # Initialize relationships file if it doesn't exist
        if not self.relationships_file.exists():
            self._create_relationships_file()

    def _create_relationships_file(self):
        """Create relationships CSV with headers"""
        with open(self.relationships_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'id',
                'contact_id_1',
                'contact_id_2',
                'relationship_type',
                'strength',
                'notes',
                'mutual_connections',
                'created_date'
            ])

    def load_contacts(self):
        """Load all contacts"""
        contacts = []
        if self.contacts_file.exists():
            with open(self.contacts_file, 'r') as f:
                reader = csv.DictReader(f)
                contacts = list(reader)
        return contacts

    def load_relationships(self):
        """Load all relationships"""
        relationships = []
        if self.relationships_file.exists():
            with open(self.relationships_file, 'r') as f:
                reader = csv.DictReader(f)
                relationships = list(reader)
        return relationships

    def save_relationships(self, relationships):
        """Save relationships to CSV"""
        if not relationships:
            self._create_relationships_file()
            return

        fieldnames = relationships[0].keys()
        with open(self.relationships_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(relationships)

    def add_relationship(self, contact_id_1, contact_id_2, relationship_type='knows',
                        strength=0.5, notes='', mutual_connections=''):
        """
        Add a relationship between two contacts

        Args:
            contact_id_1: First contact ID
            contact_id_2: Second contact ID
            relationship_type: Type of relationship (knows, worked_with, introduced_by, etc.)
            strength: Tie strength 0.0-1.0 (Granovetter's weak/strong ties)
                     0.0-0.3: Weak tie (acquaintance, met once)
                     0.4-0.6: Medium tie (professional relationship)
                     0.7-1.0: Strong tie (close relationship, frequent contact)
            notes: Additional notes
            mutual_connections: Who introduced them / mutual connections
        """
        relationships = self.load_relationships()

        # Check if relationship already exists
        for rel in relationships:
            if (rel['contact_id_1'] == contact_id_1 and rel['contact_id_2'] == contact_id_2) or \
               (rel['contact_id_1'] == contact_id_2 and rel['contact_id_2'] == contact_id_1):
                print(f"Relationship already exists between {contact_id_1} and {contact_id_2}")
                return None

        # Generate new ID
        if relationships:
            max_id = max(int(r['id']) for r in relationships if r.get('id'))
            new_id = max_id + 1
        else:
            new_id = 1

        relationship = {
            'id': str(new_id),
            'contact_id_1': str(contact_id_1),
            'contact_id_2': str(contact_id_2),
            'relationship_type': relationship_type,
            'strength': str(strength),
            'notes': notes,
            'mutual_connections': mutual_connections,
            'created_date': datetime.now().strftime('%Y-%m-%d')
        }

        relationships.append(relationship)
        self.save_relationships(relationships)

        return new_id

    def update_relationship(self, relationship_id, **updates):
        """Update an existing relationship"""
        relationships = self.load_relationships()

        for rel in relationships:
            if rel['id'] == str(relationship_id):
                rel.update(updates)
                self.save_relationships(relationships)
                return True

        return False

    def get_contact_relationships(self, contact_id):
        """Get all relationships for a contact"""
        relationships = self.load_relationships()
        contacts = self.load_contacts()

        contact_rels = []
        for rel in relationships:
            if rel['contact_id_1'] == str(contact_id):
                other_id = rel['contact_id_2']
            elif rel['contact_id_2'] == str(contact_id):
                other_id = rel['contact_id_1']
            else:
                continue

            # Get other contact details
            other_contact = next((c for c in contacts if c['id'] == other_id), None)
            if other_contact:
                contact_rels.append({
                    'relationship_id': rel['id'],
                    'contact_id': other_id,
                    'name': other_contact['name'],
                    'company': other_contact['company'],
                    'relationship_type': rel['relationship_type'],
                    'strength': rel['strength'],
                    'notes': rel['notes']
                })

        return contact_rels

    def find_mutual_connections(self, contact_id_1, contact_id_2):
        """
        Find mutual connections between two contacts
        "Friend of friend" analysis
        """
        rels_1 = set(r['contact_id'] for r in self.get_contact_relationships(contact_id_1))
        rels_2 = set(r['contact_id'] for r in self.get_contact_relationships(contact_id_2))

        mutual = rels_1.intersection(rels_2)

        contacts = self.load_contacts()
        mutual_contacts = []
        for cid in mutual:
            contact = next((c for c in contacts if c['id'] == cid), None)
            if contact:
                mutual_contacts.append({
                    'id': cid,
                    'name': contact['name'],
                    'company': contact['company']
                })

        return mutual_contacts

    def suggest_warm_intro_paths(self, target_contact_id, max_depth=2):
        """
        Find warm introduction paths to a target contact
        Uses breadth-first search through relationship graph

        Returns paths like: You -> Connector -> Target
        """
        relationships = self.load_relationships()
        contacts = self.load_contacts()

        # Build adjacency list
        graph = {}
        for rel in relationships:
            id1 = rel['contact_id_1']
            id2 = rel['contact_id_2']

            if id1 not in graph:
                graph[id1] = []
            if id2 not in graph:
                graph[id2] = []

            graph[id1].append({'id': id2, 'strength': float(rel['strength'])})
            graph[id2].append({'id': id1, 'strength': float(rel['strength'])})

        # BFS to find paths
        paths = []
        visited = set()
        queue = [([target_contact_id], 0)]  # (path, depth)

        while queue:
            path, depth = queue.pop(0)
            current = path[-1]

            if current in visited or depth >= max_depth:
                continue

            visited.add(current)

            # Get neighbors
            neighbors = graph.get(current, [])
            for neighbor in neighbors:
                neighbor_id = neighbor['id']
                if neighbor_id not in path:
                    new_path = path + [neighbor_id]

                    # If we found a path with depth > 1, save it
                    if len(new_path) > 1 and depth < max_depth:
                        # Get contact names for path
                        path_contacts = []
                        for cid in reversed(new_path):
                            contact = next((c for c in contacts if c['id'] == cid), None)
                            if contact:
                                path_contacts.append({
                                    'id': cid,
                                    'name': contact['name'],
                                    'company': contact['company']
                                })

                        if len(path_contacts) > 1:
                            paths.append({
                                'path': path_contacts,
                                'degrees': len(new_path) - 1,
                                'strength': neighbor['strength']
                            })

                    if depth + 1 < max_depth:
                        queue.append((new_path, depth + 1))

        return sorted(paths, key=lambda x: (x['degrees'], -x['strength']))[:10]

    def bulk_import_relationships(self, csv_file):
        """Import relationships from CSV file"""
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.add_relationship(
                    contact_id_1=row['contact_id_1'],
                    contact_id_2=row['contact_id_2'],
                    relationship_type=row.get('relationship_type', 'knows'),
                    strength=float(row.get('strength', 0.5)),
                    notes=row.get('notes', ''),
                    mutual_connections=row.get('mutual_connections', '')
                )

        print(f"✓ Imported relationships from {csv_file}")

    def identify_introduction_opportunities(self):
        """
        Identify opportunities to make valuable introductions
        "Social capital brokerage" opportunities

        Looks for contacts who:
        1. Are not connected
        2. Should be connected (same category/tier)
        3. You're connected to both
        """
        contacts = self.load_contacts()
        relationships = self.load_relationships()

        # Build who's connected to whom
        connections = {}
        for rel in relationships:
            id1 = rel['contact_id_1']
            id2 = rel['contact_id_2']

            if id1 not in connections:
                connections[id1] = set()
            if id2 not in connections:
                connections[id2] = set()

            connections[id1].add(id2)
            connections[id2].add(id1)

        opportunities = []

        # Find pairs who should be connected but aren't
        for i, c1 in enumerate(contacts):
            for c2 in contacts[i+1:]:
                # Skip if already connected
                if c2['id'] in connections.get(c1['id'], set()):
                    continue

                # Check if they should be connected
                score = 0
                reasons = []

                # Same category
                if c1['category'] == c2['category']:
                    score += 2
                    reasons.append(f"Both {c1['category']}")

                # Similar tier
                if abs(int(c1['tier']) - int(c2['tier'])) <= 1:
                    score += 1
                    reasons.append("Similar tier")

                # Both in your network (you could introduce them)
                # Placeholder: would need "you" contact ID

                if score >= 2:
                    opportunities.append({
                        'contact_1': c1['name'],
                        'contact_2': c2['name'],
                        'score': score,
                        'reason': ", ".join(reasons),
                        'action': f"Consider introducing {c1['name']} to {c2['name']}"
                    })

        return sorted(opportunities, key=lambda x: x['score'], reverse=True)[:20]

    def show_relationship_summary(self, contact_id):
        """Show relationship summary for a contact"""
        contacts = self.load_contacts()
        contact = next((c for c in contacts if c['id'] == str(contact_id)), None)

        if not contact:
            print(f"Contact {contact_id} not found")
            return

        rels = self.get_contact_relationships(contact_id)

        print(f"\n{'='*70}")
        print(f"RELATIONSHIPS: {contact['name']} ({contact['company']})")
        print(f"{'='*70}")

        if not rels:
            print("\nNo relationships recorded.")
            print("Add relationships with: ./scripts/newco_cli.py relationship add")
            return

        print(f"\nTotal Connections: {len(rels)}\n")

        # Group by tie strength
        strong_ties = [r for r in rels if float(r['strength']) >= 0.7]
        medium_ties = [r for r in rels if 0.4 <= float(r['strength']) < 0.7]
        weak_ties = [r for r in rels if float(r['strength']) < 0.4]

        if strong_ties:
            print(f"Strong Ties ({len(strong_ties)}):")
            for rel in strong_ties:
                print(f"  • {rel['name']} ({rel['company']}) - {rel['relationship_type']}")

        if medium_ties:
            print(f"\nMedium Ties ({len(medium_ties)}):")
            for rel in medium_ties[:5]:
                print(f"  • {rel['name']} ({rel['company']}) - {rel['relationship_type']}")

        if weak_ties:
            print(f"\nWeak Ties ({len(weak_ties)}) - [Showing first 5]:")
            for rel in weak_ties[:5]:
                print(f"  • {rel['name']} ({rel['company']}) - {rel['relationship_type']}")

        print(f"\n{'='*70}\n")


if __name__ == '__main__':
    rm = RelationshipManager()
    # Example usage
    print("Relationship Manager initialized")
