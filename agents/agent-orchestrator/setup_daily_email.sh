#!/bin/bash
# Setup Daily Email Summary for NEWCO
# ====================================

echo "🔧 Setting up NEWCO daily email summary..."
echo ""

# Make script executable
chmod +x /Users/rufio/NEWCO/agent-orchestrator/daily_summary_email.py

# Install cron job for daily 8 AM emails
CRON_JOB="0 8 * * * /usr/bin/python3 /Users/rufio/NEWCO/agent-orchestrator/daily_summary_email.py >> /tmp/newco_daily_email.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "daily_summary_email.py"; then
    echo "✅ Cron job already exists"
else
    # Add cron job
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ Cron job added: Daily email at 8 AM"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  DAILY EMAIL SUMMARY - CONFIGURED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📧 Email: rufioruff@icloud.com"
echo "⏰ Schedule: Daily at 8:00 AM"
echo "📁 Logs: /tmp/newco_daily_email.log"
echo "💾 Saved: /Users/rufio/NEWCO/daily_summaries/"
echo ""
echo "Test now:"
echo "  python3 /Users/rufio/NEWCO/agent-orchestrator/daily_summary_email.py"
echo ""
echo "View cron jobs:"
echo "  crontab -l"
echo ""
echo "Remove cron job:"
echo "  crontab -l | grep -v daily_summary_email.py | crontab -"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup complete!"
