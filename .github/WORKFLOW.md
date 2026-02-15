# Development Workflow

**Standard workflow for collaborating on NEWCO GTM System**

---

## 📋 Quick Reference

```bash
# 1. Get latest code
git pull

# 2. Create feature branch
git checkout -b feature/your-feature

# 3. Make changes and commit
git add <files>
git commit -m "feat: your change"

# 4. Push branch
git push origin feature/your-feature

# 5. Create Pull Request on GitHub
# 6. Request review
# 7. Address feedback
# 8. Merge when approved
```

---

## 🔄 Detailed Workflow

### 1. Start New Work

**Always start from latest main:**
```bash
# Switch to main
git checkout main

# Get latest changes
git pull origin main

# Create feature branch
git checkout -b feature/network-sorting
```

### 2. Make Changes

**Work in your branch:**
```bash
# Check what branch you're on
git branch

# Make changes to files
# Test your changes
./bin/newco --help
python test_llm_integration.py

# Check what changed
git status
git diff
```

### 3. Commit Changes

**Commit frequently with good messages:**
```bash
# Stage specific files
git add core/scripts/network_analysis.py
git add tests/test_network.py

# Or stage all changes
git add -A

# Commit with message
git commit -m "feat: add network multiplier sorting

- Sort contacts by multiplier score
- Add --sort flag to CLI
- Include tests for sorting logic

Co-Authored-By: Your Name <email@example.com>"
```

### 4. Push to GitHub

**Push your branch:**
```bash
# First time pushing branch
git push -u origin feature/network-sorting

# Subsequent pushes
git push
```

### 5. Create Pull Request

**On GitHub:**
1. Go to https://github.com/RufioRuff/newco-gtm-system
2. Click "Pull Requests"
3. Click "New Pull Request"
4. Select your branch
5. Fill out PR template
6. Click "Create Pull Request"

**PR Template will ask for:**
- Description of changes
- Type of change (feature, bug fix, etc.)
- Testing performed
- Related issues
- Checklist completion

### 6. Request Review

**Get feedback:**
```bash
# Using GitHub CLI
gh pr create --title "Add network sorting" --body "..."

# Request specific reviewer
gh pr edit --add-reviewer username
```

**On GitHub:**
- Click "Reviewers" in sidebar
- Select reviewer
- Add comments on specific lines if needed

### 7. Address Feedback

**Make requested changes:**
```bash
# Make changes based on feedback
# ... edit files ...

# Commit changes
git add <files>
git commit -m "fix: address review feedback

- Update sorting algorithm as suggested
- Add edge case handling
- Improve documentation"

# Push updates
git push
```

**PR updates automatically when you push!**

### 8. Merge

**After approval:**
1. Ensure all checks pass
2. Resolve any conflicts
3. Click "Squash and merge" (recommended)
4. Delete branch after merge

```bash
# After merge, update local main
git checkout main
git pull origin main

# Delete merged branch
git branch -d feature/network-sorting
```

---

## 🌳 Branch Strategy

### Branch Types

**Main Branch:**
- `main` → Production-ready code
- Always deployable
- Protected (requires PR + review)

**Feature Branches:**
- `feature/descriptive-name` → New features
- Example: `feature/linkedin-2fa`

**Bug Fix Branches:**
- `fix/issue-description` → Bug fixes
- Example: `fix/email-template-crash`

**Documentation Branches:**
- `docs/what-updating` → Documentation updates
- Example: `docs/update-network-guide`

**Other Branches:**
- `refactor/area` → Code refactoring
- `test/what-testing` → Test additions
- `chore/maintenance-task` → Maintenance

### Branch Naming

**Good:**
- `feature/network-multiplier-ui`
- `fix/contact-search-bug`
- `docs/linkedin-setup-guide`

**Bad:**
- `my-changes` (too vague)
- `feature` (no description)
- `fix-bug` (which bug?)

---

## 💬 Commit Messages

### Format

```
<type>: <brief description> (max 50 chars)

<detailed explanation of what and why>
<wrap at 72 characters>

<footer with issue references>
```

### Types

- `feat:` → New feature
- `fix:` → Bug fix
- `docs:` → Documentation only
- `style:` → Code style (formatting, no logic change)
- `refactor:` → Code restructuring
- `perf:` → Performance improvement
- `test:` → Adding tests
- `chore:` → Maintenance (dependencies, config)

### Examples

**Feature:**
```
feat: add network multiplier identification

Implement composite scoring algorithm combining:
- Degree centrality (Freeman 1978)
- Betweenness centrality (Freeman 1977)
- Structural holes access (Burt 1992)
- Tie strength (Granovetter 1973)

Add CLI command: ./bin/newco network multipliers

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Bug Fix:**
```
fix: handle missing company field in email templates

Email generation crashed when contact.company was None.
Now uses fallback: "your organization" when company missing.

Added test: test_email_generation_no_company()

Fixes #42
```

**Documentation:**
```
docs: update LinkedIn scraping guide

- Add 2FA setup instructions
- Include troubleshooting section
- Update rate limiting guidance
- Add screenshot of login flow
```

---

## 🔍 Code Review Process

### For Authors

**Before Requesting Review:**
1. Test all changes locally
2. Update relevant documentation
3. Add/update tests
4. Update CHANGELOG.md
5. Self-review your diff
6. Fill out PR template completely

**During Review:**
- Respond to comments within 24 hours
- Ask questions if feedback unclear
- Make requested changes
- Push updates (PR updates automatically)
- Request re-review after changes

**After Approval:**
- Thank reviewer
- Merge PR
- Delete branch
- Update local main

### For Reviewers

**Review Checklist:**
- [ ] Code correctness
- [ ] Tests present and passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No security issues
- [ ] Reasonable performance
- [ ] Follows coding standards
- [ ] No unnecessary complexity

**Providing Feedback:**
1. Start with positive comments
2. Be specific about issues
3. Explain "why" behind suggestions
4. Distinguish between "must fix" vs "nice to have"
5. Offer solutions, not just problems
6. Approve when ready or request changes

---

## 🔄 Keeping Branch Updated

### Sync with Main

**Your branch gets out of date when:**
- Others merge PRs to main
- You've been working for several days
- Merge conflicts appear

**Update your branch:**
```bash
# Option 1: Rebase (cleaner history)
git checkout feature/your-branch
git fetch origin
git rebase origin/main

# If conflicts, resolve them
git add <resolved-files>
git rebase --continue

# Force push (rewrites history)
git push --force-with-lease

# Option 2: Merge (preserves history)
git checkout feature/your-branch
git merge origin/main

# Resolve conflicts if any
git add <resolved-files>
git commit

# Normal push
git push
```

**Recommendation:** Use rebase for cleaner history

### Resolving Merge Conflicts

**When conflicts occur:**
```bash
# Pull latest main
git checkout main
git pull

# Try to merge main into your branch
git checkout feature/your-branch
git merge main

# Git will mark conflicts in files:
<<<<<<< HEAD
Your changes
=======
Changes from main
>>>>>>> main

# Edit files to resolve
# Choose which changes to keep
# Remove conflict markers

# Stage resolved files
git add <resolved-files>

# Complete merge
git commit

# Push
git push
```

---

## 🚦 PR States

### Draft
- Work in progress
- Not ready for review
- Shows you're working on it
- Can request early feedback

**Create draft:**
```bash
gh pr create --draft
```

### Ready for Review
- Code complete
- Tests passing
- Documentation updated
- Ready for feedback

**Mark ready:**
- Click "Ready for review" on GitHub

### Changes Requested
- Reviewer requested modifications
- Address feedback
- Push updates
- Request re-review

### Approved
- Reviewer approved changes
- All checks passing
- Ready to merge

### Merged
- PR merged into main
- Branch can be deleted
- Feature is live

---

## 🎯 Best Practices

### Do's ✅

- **Pull frequently** - Stay up to date with main
- **Commit often** - Small, focused commits
- **Write clear messages** - Explain what and why
- **Test before pushing** - Verify changes work
- **Update docs** - Keep documentation current
- **Review your own PR** - Catch issues before review
- **Respond promptly** - Don't block reviewers
- **Thank reviewers** - Appreciate feedback

### Don'ts ❌

- **Don't commit to main** - Always use branches
- **Don't push broken code** - Test first
- **Don't skip tests** - Add tests for changes
- **Don't ignore feedback** - Address all comments
- **Don't force push shared branches** - Use `--force-with-lease`
- **Don't commit secrets** - No API keys, passwords
- **Don't make huge PRs** - Keep them focused and reviewable

---

## 🛠️ Useful Commands

### Status & Information
```bash
# What branch am I on?
git branch

# What changed?
git status

# Show diff
git diff

# Show commit history
git log --oneline

# Show branches
git branch -a

# Show remotes
git remote -v
```

### Working with Changes
```bash
# Stage files
git add <file>
git add -A  # All changes

# Unstage files
git reset <file>
git reset  # Unstage all

# Discard changes
git checkout -- <file>
git checkout .  # Discard all

# Stash changes temporarily
git stash
git stash pop  # Restore stashed changes
```

### Branches
```bash
# Create branch
git checkout -b feature/new-branch

# Switch branch
git checkout main

# Delete local branch
git branch -d feature/old-branch

# Delete remote branch
git push origin --delete feature/old-branch

# List all branches
git branch -a
```

### Syncing
```bash
# Get latest from remote
git fetch origin

# Pull and merge
git pull origin main

# Push to remote
git push origin feature/branch-name

# Push all branches
git push --all
```

### Fixing Mistakes
```bash
# Undo last commit (keep changes)
git reset HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Change last commit message
git commit --amend

# Revert a commit (creates new commit)
git revert <commit-hash>
```

---

## 📊 Example Workflow

### Scenario: Add New Feature

**Day 1:**
```bash
# Start fresh
git checkout main
git pull

# Create branch
git checkout -b feature/contact-tags

# Make changes
# ... edit files ...

# Test
./bin/newco contact list

# Commit
git add core/scripts/contact_manager.py
git commit -m "feat: add tagging system for contacts"

# Push
git push -u origin feature/contact-tags

# Create draft PR
gh pr create --draft --title "Add contact tagging system"
```

**Day 2:**
```bash
# Continue work
# ... edit more files ...

# Commit again
git add tests/test_tags.py
git add documentation/guides/CONTACT_TAGGING.md
git commit -m "docs: add contact tagging guide and tests"

# Push updates
git push

# Mark PR ready
gh pr ready
gh pr edit --add-reviewer co-founder
```

**Day 3:**
```bash
# Reviewer requested changes
# ... make fixes ...

# Commit fixes
git add core/scripts/contact_manager.py
git commit -m "fix: address review feedback on tag validation"

# Push
git push

# Reviewer approves, merge on GitHub
# Update local main
git checkout main
git pull

# Delete merged branch
git branch -d feature/contact-tags
```

---

## 🆘 Common Issues

### "Merge conflict"
**Solution:**
```bash
# Pull latest main
git checkout main
git pull

# Merge into your branch
git checkout feature/your-branch
git merge main

# Resolve conflicts in files
# Stage resolved files
git add <files>
git commit

# Push
git push
```

### "Pushed to wrong branch"
**Solution:**
```bash
# Create correct branch from current
git branch feature/correct-name

# Reset wrong branch
git checkout wrong-branch
git reset --hard origin/wrong-branch

# Continue on correct branch
git checkout feature/correct-name
```

### "Need to update commit message"
**Solution:**
```bash
# Last commit only (not pushed)
git commit --amend

# Already pushed (creates new commit)
# Just make new commit with fix
```

### "Accidentally committed secrets"
**Solution:**
```bash
# If not pushed yet
git reset HEAD~1
# Remove secret from file
git add <file>
git commit

# If already pushed - contact team immediately
# May need to rotate credentials
```

---

## 📞 Getting Help

**Stuck? Ask for help!**

1. Check this guide
2. Check CONTRIBUTING.md
3. Check COLLABORATION_GUIDE.md
4. Create GitHub Issue with "question" label
5. Tag relevant people

**Common Resources:**
- Git documentation: https://git-scm.com/doc
- GitHub guides: https://guides.github.com
- Pro Git book: https://git-scm.com/book

---

**Happy collaborating! 🚀**

*Last Updated: February 14, 2026*
