# Social Network Analysis Guide
## Grounded in Academic Research

## Overview

The NEWCO system includes a comprehensive social network analysis engine based on foundational research in social network theory. This guide explains the concepts, how to use the tools, and how to apply insights to your GTM strategy.

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Why Network Analysis Matters for GTM](#why-network-analysis-matters-for-gtm)
3. [Key Metrics Explained](#key-metrics-explained)
4. [Using the Tools](#using-the-tools)
5. [Strategic Applications](#strategic-applications)
6. [Academic Foundation](#academic-foundation)

---

## Core Concepts

### Network Multipliers

**Contacts who can open doors to entire networks, not just individuals.**

Network multipliers have three key characteristics:
1. **High Betweenness** - They bridge otherwise disconnected groups
2. **Access to Structural Holes** - Their contacts don't overlap
3. **Network Influence** - They're connected to other influential people

**GTM Impact:** One relationship with a true network multiplier is worth 10+ individual contacts.

### Structural Holes (Burt 1992, 2004)

> "The people who stand near the holes in a social structure are at a higher risk of having good ideas"

**Concept:** Gaps between non-redundant contacts in a network.

**Why it matters:**
- Access to non-overlapping information
- Brokerage opportunities
- Novel insights from disconnected groups

**Example:**
- Person A knows VCs
- Person B knows family offices
- You know both, but they don't know each other
- You span a "structural hole" = valuable position

**Low Constraint = Good** (You have non-redundant contacts)
**High Constraint = Bad** (All your contacts know each other = redundant)

### Weak Ties (Granovetter 1973)

> "The Strength of Weak Ties"

**Paradox:** Weak ties are MORE valuable than strong ties for:
- Job searches
- Novel information
- Accessing different social circles
- Business opportunities

**Strong Ties:**
- Frequent contact
- Emotional closeness
- Redundant information (you already know what they know)

**Weak Ties:**
- Infrequent contact
- Professional relationship
- Bridge to NEW networks
- Novel, non-redundant information

**GTM Application:**
- Use strong ties for warm intros (trust)
- Use weak ties to access new networks (reach)

### Betweenness Centrality (Freeman 1977)

**Measures:** How often someone lies on shortest paths between others

**Interpretation:**
- High betweenness = BROKER, GATEKEEPER
- They connect otherwise disconnected groups
- Control information flow between communities

**Example:** Platform gatekeepers have high betweenness - they connect:
- Investors (LPs)
- Fund managers (GPs)
- Institutional allocators

### Homophily (McPherson et al. 2001)

> "Birds of a feather flock together"

**Concept:** Tendency for similar people to connect

**In GTM Context:**
- VCs cluster with VCs
- Family offices cluster with family offices
- Breaking homophilous clusters = accessing new markets

**High Homophily = Risk**
- Clustered network
- Redundant information
- Limited reach

**Low Homophily = Opportunity**
- Diverse network
- Cross-category connections
- Broader market access

---

## Why Network Analysis Matters for GTM

### Traditional Approach (Linear)
```
You → Contact 1
You → Contact 2
You → Contact 3
...
Result: 100 contacts = 100 relationships
```

### Network Approach (Exponential)
```
You → Network Multiplier → Their 50 contacts
Result: 1 relationship = 50+ potential intros
```

### Key Insights for Fundraising:

1. **Network Multipliers > Individual Contacts**
   - 1 relationship with Bob Burlinson (T0) who knows 50 LPs
   - Is worth MORE than 20 relationships with individual LPs you don't know

2. **Weak Ties Open New Markets**
   - Your close friends likely know the same LPs you know (redundant)
   - Weak ties bridge to DIFFERENT LP networks (novel)

3. **Brokers Control Access**
   - Platform gatekeepers (Hamilton Lane, Goldman, JPM)
   - Have high betweenness = gateway to institutional LPs
   - Focus here for institutional credibility

4. **Structural Holes = Opportunities**
   - If you know VCs AND family offices (but they don't know each other)
   - You can broker introductions (social capital)
   - Creates value for both sides + strengthens your position

---

## Key Metrics Explained

### 1. Network Multiplier Score (Composite Metric)

**Formula:**
```
Multiplier Score =
  (Broker Score × 0.4) +
  (Structural Holes Access × 0.4) +
  (Network Influence × 0.2)
```

**Interpretation:**
- **> 0.7**: Elite network multiplier - TOP PRIORITY
- **0.4-0.7**: Strong multiplier - high value
- **0.2-0.4**: Emerging multiplier
- **< 0.2**: Individual contributor (still valuable, but not a multiplier)

**Use:** Rank your top 20 priorities by multiplier score, not just tier.

### 2. Broker Score (Betweenness)

**What it measures:** Degree to which this person bridges disconnected groups

**Calculation:** Number of "bridges" (connections between otherwise disconnected people) divided by total connections

**Interpretation:**
- **> 0.6**: Strong broker - bridges multiple communities
- **0.3-0.6**: Moderate brokerage
- **< 0.3**: Within-community connector

**Strategic Value:** Brokers can provide:
- Warm intros to disconnected networks
- Novel information from different communities
- Gateway to institutional access

### 3. Structural Holes Access

**What it measures:** Access to non-overlapping networks

**Formula:** 1 - Network Constraint
- Low constraint = high structural holes access = GOOD

**Interpretation:**
- **> 0.7**: Excellent access to non-redundant networks
- **0.5-0.7**: Good access
- **< 0.5**: Redundant network (contacts all know each other)

**Strategic Value:**
- High access = diverse information sources
- Opportunity to broker connections
- Less competition (you're not redundant)

### 4. Network Influence Score

**What it measures:** You're important if you're connected to important people

**Method:** Eigenvector centrality (PageRank-style algorithm)

**Interpretation:**
- **> 2.0**: Very high influence
- **1.0-2.0**: Above average influence
- **< 1.0**: Below average influence

**Strategic Value:**
- High influence contacts lend credibility
- "Borrowed" status through association
- Endorsement carries more weight

### 5. Tie Strength

**Scale:** 0.0 - 1.0

**Classification:**
- **0.7-1.0:** Strong tie (close relationship, frequent contact)
- **0.4-0.6:** Medium tie (professional relationship)
- **0.0-0.3:** Weak tie (acquaintance, infrequent contact)

**Based on:**
- Interaction frequency
- Recency of contact
- Relationship type
- Reciprocity

**Strategic Use:**
- Strong ties: Ask for warm intros, advice, endorsements
- Weak ties: Explore new networks, novel opportunities

### 6. Homophily Index

**Scale:** 0.0 - 1.0

**Interpretation:**
- **> 0.7**: High homophily - clustered network (RISK)
- **0.5-0.7**: Moderate homophily
- **< 0.5**: Low homophily - diverse network (GOOD)

**Strategic Implication:**
- High homophily = echo chamber, limited reach
- Low homophily = diverse access, broader opportunities
- Track this to ensure you're not stuck in one cluster

---

## Using the Tools

### Build Your Network Graph

**1. Add Relationships**
```bash
# Add a relationship
./scripts/newco_cli.py relationship add 1 2 \
  --type "worked_with" \
  --strength 0.8 \
  --notes "Collaborated on deals"

# Tie strength guide:
# 0.0-0.3: Weak (met once, LinkedIn, acquaintance)
# 0.4-0.6: Medium (professional relationship, occasional contact)
# 0.7-1.0: Strong (close relationship, frequent contact, trust)
```

**2. View Relationships**
```bash
# Show all relationships for a contact
./scripts/newco_cli.py relationship show 1
```

### Analyze Your Network

**Comprehensive Analysis**
```bash
./scripts/newco_cli.py network analyze
```

Shows:
- Network multipliers (prioritized list)
- Structural holes access
- Brokers (betweenness centrality)
- Network influence scores
- Homophily analysis

**Identify Network Multipliers**
```bash
./scripts/newco_cli.py network multipliers
```

Returns prioritized list of contacts with highest multiplier effect.

**Find Brokers**
```bash
./scripts/newco_cli.py network brokers
```

Identifies contacts who bridge different groups (high betweenness).

**Network Influence**
```bash
./scripts/newco_cli.py network influence
```

Shows who's connected to influential people.

**Calculate Network Reach**
```bash
# How many people can you reach through this contact?
./scripts/newco_cli.py network reach 1 --degrees 2
```

### Find Warm Introduction Paths

**Find Path to Target Contact**
```bash
./scripts/newco_cli.py relationship intro-path 15
```

Returns: You → Connector → Target (with tie strength)

**Find Mutual Connections**
```bash
./scripts/newco_cli.py relationship mutual 1 5
```

Returns shared connections between two contacts.

**Identify Introduction Opportunities**
```bash
./scripts/newco_cli.py relationship opportunities
```

Finds contacts who should be connected but aren't (brokerage opportunities).

### Export Network

**Export for Visualization**
```bash
./scripts/newco_cli.py network export
```

Exports network graph to JSON for visualization in tools like Gephi, D3.js, or Cytoscape.

---

## Strategic Applications

### 1. Prioritize Outreach

**Old Way:**
- Tier-based prioritization
- Contact everyone in Tier 1, then Tier 2, etc.

**Network Way:**
- Sort by Network Multiplier Score
- Focus on contacts with:
  - High multiplier score
  - Access to non-redundant networks
  - Brokerage potential

**Command:**
```bash
./scripts/newco_cli.py network multipliers
```

Use this list for your weekly top 20.

### 2. Leverage Weak Ties

**Strategy:** Don't ignore weak ties!

Granovetter showed weak ties are MORE valuable for:
- Job searches (73% of jobs came through weak ties)
- Novel information
- Accessing different social circles

**Application:**
- Map your weak ties (strength 0.0-0.3)
- These bridge to NEW networks
- Use them to expand into new LP categories

**Tactic:**
- "Hi [weak tie], we haven't spoken in a while..."
- Ask about their network, not direct intros
- Low pressure, exploratory

### 3. Target Structural Hole Positions

**Goal:** Become a broker yourself

**Strategy:**
1. Identify disconnected groups in your network
2. Build bridges between them
3. Increase your own betweenness

**Example:**
- You know VCs (Group A)
- You know Family Offices (Group B)
- They don't know each other
- Broker introductions between them
- Result: You become valuable to both groups

**Command:**
```bash
./scripts/newco_cli.py relationship opportunities
```

Shows brokerage opportunities.

### 4. Warm Intro Paths

**Problem:** You want to reach a target contact but don't know them

**Solution:** Find 2-degree paths

**Command:**
```bash
./scripts/newco_cli.py relationship intro-path [target_id]
```

**Strategy:**
1. Find path with strongest ties
2. Approach the connector (middle person)
3. Ask for warm intro to target
4. Provide value to connector as "payment"

**Success Rate:**
- Cold email: 1-3% response
- Warm intro: 30-50% response
- 10-15x improvement!

### 5. Break Homophilous Clusters

**Problem:** Network too clustered (high homophily)

**Risk:** Echo chamber, redundant information

**Solution:** Deliberately connect across categories

**Track:**
```bash
./scripts/newco_cli.py network analyze
```

Look at homophily index. If > 0.7:
- Seek cross-category connections
- Attend events outside your usual circle
- Ask for intros to different industries

### 6. Influence Through Association

**Strategy:** Connect with high-influence contacts

**Command:**
```bash
./scripts/newco_cli.py network influence
```

**Tactic:**
- Build relationships with high-influence contacts
- Ask for endorsements, not just intros
- "Social proof" effect
- "[High influence person] recommended I reach out..."

---

## Academic Foundation

### Key Papers & Books

**Structural Holes:**
- Burt, R. S. (1992). *Structural Holes: The Social Structure of Competition*
- Burt, R. S. (2004). "Structural Holes and Good Ideas"

**Weak Ties:**
- Granovetter, M. (1973). "The Strength of Weak Ties"
- Granovetter, M. (1983). "The Strength of Weak Ties: A Network Theory Revisited"

**Centrality:**
- Freeman, L. C. (1977). "A Set of Measures of Centrality Based on Betweenness"
- Freeman, L. C. (1978). "Centrality in Social Networks: Conceptual Clarification"
- Bonacich, P. (1987). "Power and Centrality: A Family of Measures"

**Homophily:**
- McPherson, M., Smith-Lovin, L., & Cook, J. M. (2001). "Birds of a Feather: Homophily in Social Networks"

**Small World Networks:**
- Milgram, S. (1967). "The Small World Problem"
- Watts, D. J., & Strogatz, S. H. (1998). "Collective Dynamics of 'Small-World' Networks"
- Watts, D. J. (1999). *Small Worlds: The Dynamics of Networks Between Order and Randomness*

**General Network Theory:**
- Wasserman, S., & Faust, K. (1994). *Social Network Analysis: Methods and Applications*
- Borgatti, S. P., et al. (2018). *Analyzing Social Networks*
- Barabási, A. L. (2016). *Network Science*

### Core Principles Applied

**1. Structural Holes Principle**
- Non-redundant contacts = information advantage
- Brokerage positions = value creation
- Network constraint = measure of opportunity

**2. Weak Ties Principle**
- Weak ties bridge to new networks
- Strong ties provide redundant information
- Optimal network has mix of both

**3. Small World Principle**
- "Six degrees of separation"
- 2-degree network reach is sweet spot for intros
- Clustering + short paths = small world

**4. Preferential Attachment**
- "Rich get richer" in networks
- Connect with well-connected people
- Network effects compound

**5. Homophily Principle**
- Similar people cluster together
- Breaking clusters = accessing new markets
- Diversity = competitive advantage

---

## GTM Strategy Integration

### Week 1-2: Map Your Network
```bash
# Add all known relationships
./scripts/newco_cli.py relationship add [id1] [id2] --strength [0-1]

# Analyze network
./scripts/newco_cli.py network analyze

# Identify multipliers
./scripts/newco_cli.py network multipliers
```

### Week 3-4: Activate Network Multipliers
- Focus on Tier 0 (network multipliers)
- Request specific warm intros
- Leverage their structural position

### Week 5-8: Leverage Weak Ties
- Reactivate weak ties (haven't spoken in 6+ months)
- Explore new networks through weak tie bridges
- Lower competition (unexpected approach)

### Week 9-12: Broker Connections
- Make valuable introductions yourself
- Build social capital
- Strengthen your own network position

---

## Best Practices

**1. Map relationships as you go**
- Add each new connection immediately
- Update tie strength quarterly
- Note relationship type and mutual connections

**2. Run network analysis monthly**
- Track how your network evolves
- Identify new multipliers as relationships strengthen
- Monitor homophily to avoid clustering

**3. Prioritize by multiplier score, not just tier**
- Network structure matters more than titles
- One strong multiplier > many weak contacts

**4. Balance strong and weak ties**
- Strong ties: trust, warm intros, advice
- Weak ties: novel info, new networks, opportunities

**5. Seek structural hole positions**
- Connect disconnected groups
- Broker valuable introductions
- Increase your own network value

**6. Track your betweenness over time**
- Goal: Become a broker yourself
- Build bridges between communities
- Create value through connections

---

## Measuring Success

### Network Health Metrics

**1. Network Multiplier Count**
- Goal: 5+ contacts with multiplier score > 0.5
- Track quarterly

**2. Structural Holes Access**
- Goal: Average > 0.6 across top 20 contacts
- High access = diverse, non-redundant network

**3. Homophily Index**
- Goal: < 0.5 (diverse network)
- If > 0.7: Actively seek cross-category connections

**4. Weak Tie Ratio**
- Goal: 40-60% weak ties, 40-60% strong/medium
- Too many weak ties = no trust foundation
- Too many strong ties = redundant, clustered

**5. Two-Degree Network Reach**
- Goal: 100+ contacts reachable within 2 degrees
- Measure of total network potential

---

## Troubleshooting

**"All my contacts have low multiplier scores"**
- You need to add more relationships to the system
- Multiplier scores require network graph data
- Start mapping who knows whom

**"My network has high homophily"**
- All your contacts are in the same category
- Solution: Deliberately seek cross-category connections
- Attend events outside your usual circle

**"Can't find warm intro paths"**
- Need more relationship data
- Ask contacts: "Who do you know at [target company]?"
- Map mutual connections

**"Everyone has similar influence scores"**
- Normal for small networks
- Becomes more differentiated with 50+ contacts and relationships
- Focus on relative rankings

---

## Next Steps

1. **Map your current network**
   ```bash
   ./scripts/newco_cli.py relationship add [id1] [id2] --strength [0-1]
   ```

2. **Run initial analysis**
   ```bash
   ./scripts/newco_cli.py network analyze
   ```

3. **Identify your network multipliers**
   ```bash
   ./scripts/newco_cli.py network multipliers
   ```

4. **Prioritize outreach accordingly**
   - Focus on high multiplier score contacts
   - Leverage weak ties for new networks
   - Request warm intros through shortest paths

5. **Track network health monthly**
   - Re-run analysis
   - Monitor homophily
   - Update tie strengths

---

**Remember:** Network structure matters more than network size.

One strategic relationship with a network multiplier who spans structural holes is worth more than 100 connections to people in the same cluster.

**Focus on QUALITY (network position) over QUANTITY (number of contacts).**
