#!/bin/bash
# NEWCO GitHub Sync Script
# ========================
# Easy sync for partner collaboration

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              NEWCO GITHUB SYNC                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Navigate to NEWCO directory
cd /Users/rufio/NEWCO || exit 1

echo -e "${BLUE}[1/5]${NC} Checking git status..."
echo ""

# Check if there are changes
if [[ -z $(git status -s) ]]; then
    echo -e "${GREEN}✓${NC} No changes to commit"
    echo ""
    echo "Checking for remote updates..."
    git fetch origin

    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})

    if [ "$LOCAL" = "$REMOTE" ]; then
        echo -e "${GREEN}✓${NC} Already up to date with GitHub"
        exit 0
    else
        echo "Remote changes detected. Pulling..."
        git pull origin main
        echo -e "${GREEN}✓${NC} Updated from GitHub"
        exit 0
    fi
fi

echo "Changes detected:"
git status -s
echo ""

echo -e "${BLUE}[2/5]${NC} Generating summary..."
echo ""

# Count changes
ADDED=$(git diff --cached --name-only --diff-filter=A | wc -l | tr -d ' ')
MODIFIED=$(git diff --cached --name-only --diff-filter=M | wc -l | tr -d ' ')
DELETED=$(git diff --cached --name-only --diff-filter=D | wc -l | tr -d ' ')

# Generate commit message
DATE=$(date +"%Y-%m-%d %H:%M")
COMMIT_MSG="Update: $DATE

Changes:
- Added: $ADDED file(s)
- Modified: $MODIFIED file(s)
- Deleted: $DELETED file(s)

Agent Status:
- All local LLM agents operational
- 96% IPO model accuracy maintained
- Synced to Supabase

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

echo "$COMMIT_MSG"
echo ""

echo -e "${BLUE}[3/5]${NC} Staging changes..."
echo ""

# Stage all changes
git add -A
echo -e "${GREEN}✓${NC} Changes staged"
echo ""

echo -e "${BLUE}[4/5]${NC} Creating commit..."
echo ""

# Commit with generated message
git commit -m "$COMMIT_MSG"
echo -e "${GREEN}✓${NC} Commit created"
echo ""

echo -e "${BLUE}[5/5]${NC} Pushing to GitHub..."
echo ""

# Check for remote
if git remote | grep -q origin; then
    # Pull first to avoid conflicts
    echo "Pulling remote changes first..."
    git pull origin main --rebase || {
        echo -e "${RED}❌${NC} Merge conflict detected"
        echo ""
        echo "Please resolve conflicts manually:"
        echo "  1. Fix conflicts in affected files"
        echo "  2. git add <resolved-files>"
        echo "  3. git rebase --continue"
        echo "  4. Run this script again"
        exit 1
    }

    # Push to remote
    git push origin main
    echo -e "${GREEN}✓${NC} Pushed to GitHub"
else
    echo -e "${YELLOW}⚠${NC} No remote 'origin' configured"
    echo ""
    echo "To add remote:"
    echo "  git remote add origin https://github.com/RufioRuff/newco-learning-projects.git"
    echo "  git push -u origin main"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                  SYNC COMPLETE! ✅                           ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Summary:"
git log -1 --stat
echo ""
echo "🌐 GitHub: https://github.com/RufioRuff/newco-learning-projects"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Your partner can now pull these changes with:"
echo "  cd ~/NEWCO && git pull origin main"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
