# NEWCO GTM System Playbook

## Quick Start (First 15 Minutes)

### 1. Setup
```bash
cd ~/NEWCO
```

### 2. View Your Dashboard
```bash
./scripts/newco_cli.py report dashboard
```

### 3. See Today's Tasks
```bash
./scripts/newco_cli.py tasks today
```

### 4. View Top Priorities
```bash
./scripts/newco_cli.py contact prioritize
```

You're ready to start!

---

## Daily Workflow

### Morning Routine (10 minutes)

**1. Check Dashboard**
```bash
./scripts/newco_cli.py report dashboard
```

**2. Review Tasks**
```bash
./scripts/newco_cli.py tasks today
./scripts/newco_cli.py tasks overdue
```

**3. Update Priorities**
Review your top 20 contacts and plan your day:
```bash
./scripts/newco_cli.py contact prioritize
```

### Email Workflow

**Generate a Personalized Email**
```bash
# Auto-detect template based on contact category
./scripts/newco_cli.py email generate <contact_id>

# Use specific template
./scripts/newco_cli.py email generate <contact_id> --template vc_partner

# Save to file
./scripts/newco_cli.py email generate <contact_id> --output email.txt
```

**Preview Before Sending**
```bash
./scripts/newco_cli.py email preview <contact_id>
```

**Log After Sending**
```bash
./scripts/newco_cli.py log email <contact_id> "Your subject line" --sent --notes "Personalized based on their recent fund raise"
```

### Meeting Workflow

**Before Meeting**
1. Review contact details:
```bash
./scripts/newco_cli.py contact show <contact_id>
```

2. Use meeting template (in `templates/meeting/`) to prepare

**After Meeting**
1. Log the meeting:
```bash
./scripts/newco_cli.py log meeting <contact_id> "Initial platform discussion" \
  --outcome "Very positive, interested in learning more" \
  --next-steps "Send deck and schedule follow-up in 2 weeks"
```

2. Update contact status:
```bash
./scripts/newco_cli.py contact update <contact_id> \
  --status "Meeting Completed" \
  --next-action "Send follow-up email with deck" \
  --next-action-date "2026-02-14"
```

3. Send follow-up email (use `templates/follow_up/post_meeting.md`)

### Weekly Planning

**Every Monday Morning**

**1. Generate Weekly Report**
```bash
./scripts/newco_cli.py report weekly
```

**2. Review Pipeline**
```bash
./scripts/newco_cli.py pipeline show
./scripts/newco_cli.py pipeline weekly
```

**3. Plan Week's Tasks**
```bash
./scripts/newco_cli.py tasks week
```

**4. Identify Stale Contacts**
Check contacts you haven't touched in 14+ days and plan re-engagement

---

## Common Commands Reference

### Contact Management

```bash
# List all contacts
./scripts/newco_cli.py contact list

# Filter by tier
./scripts/newco_cli.py contact list --tier 1

# Filter by status
./scripts/newco_cli.py contact list --status "Active Conversation"

# Filter by category
./scripts/newco_cli.py contact list --category "Platform Gatekeeper"

# Search contacts
./scripts/newco_cli.py contact search "Goldman"

# Show contact details
./scripts/newco_cli.py contact show 1

# Update contact
./scripts/newco_cli.py contact update 1 --status "Meeting Scheduled"

# Add new contact
./scripts/newco_cli.py contact add \
  --name "John Doe" \
  --company "Acme Ventures" \
  --title "Partner" \
  --category "VC Partner" \
  --tier 3 \
  --email "john@acme.vc" \
  --linkedin "https://linkedin.com/in/johndoe"
```

### Email Generation

```bash
# Generate email (auto-detect template)
./scripts/newco_cli.py email generate 1

# Generate with specific template
./scripts/newco_cli.py email generate 1 --template platform_gatekeeper

# Preview email
./scripts/newco_cli.py email preview 1

# Batch generate for tier
./scripts/newco_cli.py email batch --tier 1
```

### Activity Logging

```bash
# Log sent email
./scripts/newco_cli.py log email 1 "Subject line" --sent

# Log received email
./scripts/newco_cli.py log email 1 "Re: Follow up" --notes "Positive response"

# Log meeting
./scripts/newco_cli.py log meeting 1 "Initial discussion" \
  --outcome "Positive, wants intro to LPs" \
  --next-steps "Send LP intro email template"

# Log call
./scripts/newco_cli.py log call 1 "Quick intro call"
```

### Pipeline & Reports

```bash
# Show pipeline overview
./scripts/newco_cli.py pipeline show

# This week's metrics
./scripts/newco_cli.py pipeline weekly

# Weekly pipeline report
./scripts/newco_cli.py pipeline report --week 5

# Generate weekly report
./scripts/newco_cli.py report weekly

# Show dashboard
./scripts/newco_cli.py report dashboard

# Export data
./scripts/newco_cli.py report export
```

### Task Management

```bash
# Today's tasks
./scripts/newco_cli.py tasks today

# This week's tasks
./scripts/newco_cli.py tasks week

# Overdue tasks
./scripts/newco_cli.py tasks overdue
```

---

## Email Template Customization

Templates are in `templates/email/`. Each template uses `{{variable}}` syntax for personalization.

**Available Templates:**
- `platform_gatekeeper.md` - For institutional platforms
- `family_office_cio.md` - For family office CIOs
- `vc_partner.md` - For VC partner LP intros
- `foundation_leader.md` - For foundation leaders
- `network_multiplier.md` - For top-tier connectors (requires heavy customization)

**Key Variables:**
- `{{name}}` - Contact first name
- `{{company}}` - Company name
- `{{hook}}` - Personalized opening (auto-generated)
- `{{mutual_connection_mention}}` - Mention of mutual connection (if any)

**To Customize:**
Edit the template file directly, keeping the `{{variable}}` placeholders intact.

---

## Best Practices

### Contact Management
- ✅ Update contact status after every interaction
- ✅ Always add next action and date when logging activity
- ✅ Review and update priority scores weekly
- ✅ Use tags to categorize contacts (e.g., "hot_lead", "needs_follow_up")

### Email Outreach
- ✅ Always preview emails before sending
- ✅ Customize the auto-generated hook for Tier 0-1 contacts
- ✅ Log every email you send (creates activity history)
- ✅ Track responses in notes field

### Meeting Management
- ✅ Use meeting templates in `templates/meeting/` to prepare
- ✅ Log meetings within 24 hours while fresh
- ✅ Always capture next steps and outcomes
- ✅ Schedule follow-up immediately

### Pipeline Hygiene
- ✅ Review pipeline weekly
- ✅ Move stale contacts to appropriate status
- ✅ Archive "Not Interested" contacts but keep history
- ✅ Celebrate wins! Update to "Committed/Closed" when you land an LP

---

## Troubleshooting

### "Contact not found"
- Check the contact ID with `./scripts/newco_cli.py contact list`
- Use `./scripts/newco_cli.py contact search "name"` to find the ID

### "Template not found"
- Verify template exists in `templates/email/`
- Check spelling (use underscore, not spaces)
- Available: `platform_gatekeeper`, `family_office_cio`, `vc_partner`, `foundation_leader`, `network_multiplier`

### Email variables not substituting
- Check that contact has required fields (name, company)
- Update contact with `./scripts/newco_cli.py contact update <id>`

### Dashboard showing zero metrics
- Ensure you're logging activities with `./scripts/newco_cli.py log`
- Check that contacts have dates in correct format (YYYY-MM-DD)

---

## Advanced Features

### Batch Email Generation
Generate emails for all contacts in a tier:
```bash
./scripts/newco_cli.py email batch --tier 1
```

Emails are saved to `reports/emails/` for review before sending.

### Priority Recalculation
The system auto-calculates priority scores based on:
- Tier (0-4)
- Days since last contact
- Current status
- Strategic value

To manually recalculate:
```python
from scripts.automation import AutomationEngine
ae = AutomationEngine()
ae.recalculate_priorities()
```

### Data Export
Export all data to JSON for external tools:
```bash
./scripts/newco_cli.py report export
```

Files saved to `reports/exports/`

---

## Getting Help

- Read the 90-Day Plan: `docs/90_Day_Plan.md`
- Review templates: `templates/`
- Check configuration: `config/config.yaml`

For questions or issues, review this playbook or check the inline help:
```bash
./scripts/newco_cli.py --help
./scripts/newco_cli.py contact --help
```
