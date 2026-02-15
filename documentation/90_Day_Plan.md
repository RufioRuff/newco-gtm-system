# NEWCO 90-Day Blitz Execution Plan

## Overview

**Goal:** Execute systematic outreach to 324+ contacts to secure first LP commitments and establish platform relationships for NEWCO Fund I.

**Target:** $50M Fund I with 10-15 LP commitments by end of Q1

**Timeline:** 12 weeks (90 days)

---

## Weekly Breakdown

### Weeks 1-2: Foundation & Warm Intros

**Objectives:**
- Activate network multipliers (Tier 0)
- Request warm introductions
- Research and prepare personalized outreach

**Key Targets:**
1. **Bob Burlinson** (Network Multiplier)
   - Request intros to Goldman contacts
   - Discuss Omniscient partnership angle

2. **Ken Wallace** (Network Multiplier)
   - Request intros to JPM contacts
   - Explore co-investment opportunities

3. **Matthew Goldman** (Network Multiplier)
   - Request intros to family offices
   - Discuss platform strategy

**Actions:**
```bash
# Generate personalized emails
./scripts/newco_cli.py email generate <bob_id> --template network_multiplier
./scripts/newco_cli.py email generate <ken_id> --template network_multiplier
./scripts/newco_cli.py email generate <matthew_id> --template network_multiplier

# Log outreach
./scripts/newco_cli.py log email <id> "Strategic partnership discussion" --sent

# Track follow-ups
./scripts/newco_cli.py tasks week
```

**Success Metrics:**
- 5 warm intro requests sent
- 2 platform gatekeeper meetings scheduled
- Research completed on all Tier 1 contacts

---

### Weeks 3-4: Platform Gatekeepers & Early Meetings

**Objectives:**
- Meet with platform gatekeepers
- Position NEWCO for future platform inclusion
- Build institutional credibility

**Key Targets:**

**Platform Gatekeepers (Tier 1):**
1. **Alistair Savides** (Hamilton Lane)
2. **John Goldstein** (Hamilton Lane)
3. **Dianna Seaver** (Goldman Sachs)
4. **Brett Wilson** (Goldman Sachs)
5. **Michael Anders** (JP Morgan)

**Email Template:**
```bash
./scripts/newco_cli.py email generate <id> --template platform_gatekeeper
```

**Meeting Prep:**
Use `templates/meeting/platform_pitch.md`

**Post-Meeting:**
```bash
./scripts/newco_cli.py log meeting <id> "Platform discussion" \
  --outcome "[positive/neutral/negative]" \
  --next-steps "[follow-up action]"
```

**Success Metrics:**
- 15-20 meeting requests sent
- 10+ meetings scheduled
- 5+ meetings completed
- 2 LP introductions received

---

### Weeks 5-6: Family Office Blitz

**Objectives:**
- Pitch family offices on liquid VC vehicle
- Highlight 1.25% fee structure advantage
- Schedule deep-dive conversations

**Key Targets:**

**Family Office CIOs (Tier 2):**
1. **Marie Young** (Threshold Family Office)
2. **Eric Alt** (PagnatoKarp)
3. **Conor Malloy** (Dowling Capital)
4. **Meg Alvarado** (Lagunita Family Office)
5. **Rob McReynolds** (Cook Family Office)

**Email Template:**
```bash
./scripts/newco_cli.py email generate <id> --template family_office_cio
```

**Meeting Prep:**
Use `templates/meeting/lp_pitch.md`

**Key Talking Points:**
- Quarterly liquidity vs. 10-year lockups
- 1.25% fee = 40% cost savings vs. 2/20
- Emerging manager alpha (300-500 bps)
- Diversified portfolio (15-20 managers)

**Success Metrics:**
- 10+ family office meetings
- 5+ active conversations
- 2 soft commitments
- $5-10M in preliminary interest

---

### Weeks 7-8: VC Partner LP Introductions

**Objectives:**
- Request LP intros from 96 VC partners
- Offer co-investment opportunities
- Leverage Omniscient platform value-add

**Strategy:**
Focus on VC partners with:
- Active LP fundraising (recently closed funds)
- Strong LP relationships
- Potential co-investment interest

**Batch Approach:**
```bash
# Generate batch emails for VC partners
./scripts/newco_cli.py email batch --category "VC Partner"
```

**Email Template:**
```bash
./scripts/newco_cli.py email generate <id> --template vc_partner
```

**Success Metrics:**
- 50+ VC partner emails sent
- 20+ positive responses
- 10+ LP introductions received
- 5+ warm LP intros

---

### Weeks 9-10: Foundation & Institutional Push

**Objectives:**
- Pitch foundations on mission-aligned vehicle
- Highlight emerging manager diversity
- Emphasize Berkeley ecosystem ties

**Key Targets:**

**Foundation Leaders (Tier 3):**
1. **Jessica Mancini** (Barr Foundation)
2. **Jim Canales** (Barr Foundation)
3. **Tom Reis** (W.K. Kellogg Foundation)
4. **Rip Rapson** (Kresge Foundation)

**Email Template:**
```bash
./scripts/newco_cli.py email generate <id> --template foundation_leader
```

**Customization:**
- Emphasize mission alignment
- Highlight impact + returns
- Showcase emerging manager diversity stats

**Success Metrics:**
- 8+ foundation meetings
- 4+ active conversations
- 2 soft commitments
- $10-15M in preliminary interest

---

### Weeks 11-12: Close First Commitments

**Objectives:**
- Convert soft commitments to hard commitments
- Schedule second meetings with warm leads
- Finalize first close

**Key Actions:**

**1. Second Meetings**
```bash
# Identify contacts in "Active Conversation" status
./scripts/newco_cli.py contact list --status "Active Conversation"

# Schedule follow-up meetings
# Use templates/meeting/lp_pitch.md for deep dive
```

**2. Send Commitment Letters**
- Draft and send commitment letters
- Schedule IC presentations if needed
- Answer due diligence questions

**3. Track Closes**
```bash
# Update to Committed/Closed
./scripts/newco_cli.py contact update <id> --status "Committed/Closed"

# Log the commitment
./scripts/newco_cli.py log meeting <id> "Commitment finalized" \
  --outcome "Committed $[amount]" \
  --next-steps "Send closing docs"
```

**Success Metrics:**
- 5-10 LP commitments
- $10-25M first close
- 2 platform relationships established
- 20+ active pipeline conversations for Fund II

---

## Weekly Routine

### Every Monday
```bash
# Generate weekly report
./scripts/newco_cli.py report weekly

# Review pipeline
./scripts/newco_cli.py pipeline show

# Check this week's tasks
./scripts/newco_cli.py tasks week

# Update priorities
./scripts/newco_cli.py contact prioritize
```

### Every Friday
```bash
# Review this week's metrics
./scripts/newco_cli.py pipeline weekly

# Identify stale contacts
./scripts/newco_cli.py contact list --status "Initial Outreach Sent"

# Plan next week's outreach
./scripts/newco_cli.py tasks week
```

### Daily
```bash
# Check today's tasks
./scripts/newco_cli.py tasks today

# View dashboard
./scripts/newco_cli.py report dashboard

# Log all activities immediately
```

---

## Key Performance Indicators (KPIs)

### Overall (90 Days)
- **Emails Sent:** 150+
- **Meetings Completed:** 50+
- **Active Conversations:** 25+
- **LP Commitments:** 5-10
- **Capital Committed:** $10-25M

### By Week
| Week | Emails | Meetings | Active Convos | Commits |
|------|--------|----------|---------------|---------|
| 1-2  | 10-15  | 2-3      | 2-3           | 0       |
| 3-4  | 20-25  | 5-7      | 5-7           | 0       |
| 5-6  | 15-20  | 8-10     | 10-12         | 1-2     |
| 7-8  | 50-60  | 6-8      | 15-18         | 2-3     |
| 9-10 | 15-20  | 8-10     | 20-22         | 3-5     |
| 11-12| 10-15  | 10-12    | 25+           | 5-10    |

### Track Weekly
```bash
./scripts/newco_cli.py pipeline report --week [week_number]
```

---

## Sample Email Sequences

### Platform Gatekeeper Sequence

**Initial Email (Day 1):**
```bash
./scripts/newco_cli.py email generate <id> --template platform_gatekeeper
```

**Follow-up 1 (Day 7):**
Subject: "Re: Educational meeting: Emerging VC manager trends"

"Hi [Name], wanted to follow up on my note from last week. Still interested in 20 minutes to discuss emerging manager landscape and fee transparency trends. Would [specific dates] work?"

**Follow-up 2 (Day 14):**
Subject: "Quick question on emerging manager platforms"

"Hi [Name], I understand you're busy. Quick question: Would [Company] ever consider a liquid VC fund-of-funds for platform inclusion? Happy to send a brief overview if helpful."

### Family Office Sequence

**Initial Email (Day 1):**
```bash
./scripts/newco_cli.py email generate <id> --template family_office_cio
```

**Follow-up 1 (Day 7):**
"Hi [Name], following up on NEWCO. We've had strong interest from several family offices attracted by the 1.25% fee structure. Would love to get [Family Office] perspective. 30 minutes this week or next?"

**Follow-up 2 (Day 14):**
"Hi [Name], last attempt! Given [Family Office]'s focus on [specific strategy], thought NEWCO could be a fit. I'll be in [their city] next week - coffee?"

---

## Emergency Troubleshooting

### If Meetings Aren't Converting
- Revisit email personalization
- Request feedback: "What would make this more relevant to you?"
- Leverage warm intros more aggressively
- Adjust pitch based on feedback

### If Pipeline Stalls Mid-Way
- Re-engage stale contacts with new angle
- Host webinar or group presentation
- Share case studies or updated materials
- Offer smaller pilot commitment

### If Closing Is Slow
- Create urgency: "First close deadline approaching"
- Offer early LP benefits or better terms
- Schedule in-person meetings if possible
- Bring in references from committed LPs

---

## Resources

**Templates:**
- Email: `templates/email/`
- Meetings: `templates/meeting/`
- Follow-ups: `templates/follow_up/`

**Documents:**
- Playbook: `docs/PLAYBOOK.md`
- One-Pager: `docs/NEWCO_One_Pager.md`

**Commands:**
```bash
# See all available commands
./scripts/newco_cli.py --help

# Quick dashboard check
./scripts/newco_cli.py report dashboard
```

---

## Success Checklist

**Week 2:**
- [ ] 5 warm intro requests sent
- [ ] Top 20 contacts researched and personalized
- [ ] 2 platform meetings scheduled

**Week 4:**
- [ ] 20+ meeting requests sent
- [ ] 10+ meetings completed
- [ ] 5+ active conversations
- [ ] 2+ LP intros received

**Week 6:**
- [ ] 10+ family office meetings
- [ ] 5+ active conversations
- [ ] 2 soft commitments

**Week 8:**
- [ ] 50+ VC partner emails sent
- [ ] 10+ LP intros received
- [ ] 4+ platform convos active

**Week 10:**
- [ ] 8+ foundation meetings
- [ ] 20+ active conversations total
- [ ] 4+ soft commitments

**Week 12:**
- [ ] 5-10 LP commitments
- [ ] $10-25M committed
- [ ] 25+ active pipeline for future closes
- [ ] 2 platform relationships established

---

**Remember:** This is a marathon, not a sprint. Consistency beats intensity. Log every activity, follow up relentlessly, and celebrate small wins!
