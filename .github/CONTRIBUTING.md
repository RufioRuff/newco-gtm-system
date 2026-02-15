# Contributing to NEWCO GTM System

Thank you for considering contributing to the NEWCO GTM System! This document provides guidelines and workflows for collaboration.

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Development Workflow](#development-workflow)
3. [Pull Request Process](#pull-request-process)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Documentation](#documentation)
7. [Issue Guidelines](#issue-guidelines)

---

## 🚀 Getting Started

### Prerequisites
```bash
# Python 3.10+
python --version

# Node.js 20+
node --version

# Git
git --version

# GitHub CLI (optional)
gh --version
```

### Initial Setup
```bash
# Clone repository
git clone https://github.com/RufioRuff/newco-gtm-system.git
cd newco-gtm-system

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright (for LinkedIn scraping)
playwright install chromium

# Install Node dependencies (for Alpha Engine)
cd agents/alpha-engine
yarn install
cd ../..

# Verify installation
./bin/newco --help
```

---

## 🔄 Development Workflow

### Branch Strategy

**Main Branch:**
- `main` → Production-ready code
- Protected branch
- Requires pull request review

**Feature Branches:**
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Create bug fix branch
git checkout -b fix/bug-description

# Create documentation branch
git checkout -b docs/what-youre-documenting
```

**Branch Naming:**
- `feature/` → New features
- `fix/` → Bug fixes
- `docs/` → Documentation updates
- `refactor/` → Code refactoring
- `test/` → Test additions/updates
- `chore/` → Maintenance tasks

### Making Changes

**1. Create Branch:**
```bash
git checkout -b feature/my-new-feature
```

**2. Make Changes:**
```bash
# Edit files
# Test changes locally
./bin/newco --help
python test_llm_integration.py
```

**3. Commit Changes:**
```bash
# Stage files
git add <files>

# Commit with descriptive message
git commit -m "Add feature: brief description

- Detailed change 1
- Detailed change 2
- Why this change was made

Co-Authored-By: Your Name <your@email.com>"
```

**4. Push Branch:**
```bash
git push origin feature/my-new-feature
```

**5. Create Pull Request:**
- Go to GitHub repository
- Click "Pull Requests" → "New Pull Request"
- Select your branch
- Fill out PR template
- Request review

---

## 🔍 Pull Request Process

### Before Creating PR

**Checklist:**
- [ ] Code works locally
- [ ] Tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No merge conflicts with main
- [ ] Code follows style guidelines
- [ ] Commit messages are clear

### PR Requirements

**Required:**
1. **Descriptive title** following convention:
   - `feat: add network multiplier sorting`
   - `fix: resolve email template bug`
   - `docs: update LinkedIn guide`

2. **Complete PR template**
   - Description of changes
   - Testing performed
   - Related issues linked

3. **At least 1 approving review**
   - Co-founder or designated reviewer

4. **All CI checks passing** (when CI/CD set up)
   - Tests pass
   - Linting passes
   - Build succeeds

### PR Review Process

**For Authors:**
1. Fill out PR template completely
2. Request specific reviewers
3. Respond to feedback promptly
4. Make requested changes
5. Request re-review after changes

**For Reviewers:**
1. Review within 24-48 hours
2. Check code quality and logic
3. Verify tests exist and pass
4. Check documentation accuracy
5. Consider security implications
6. Approve or request changes
7. Provide constructive feedback

### Merging

**Process:**
1. All reviews approved
2. All CI checks pass
3. No merge conflicts
4. Squash and merge (recommended)
5. Delete feature branch

---

## 📐 Coding Standards

### Python Style

**Follow PEP 8:**
```python
# Good
def calculate_network_multiplier(contact_id, degree=2):
    """
    Calculate network multiplier score for a contact.

    Args:
        contact_id (int): Contact ID
        degree (int): Network degree (default: 2)

    Returns:
        float: Multiplier score (0.0-1.0)
    """
    # Implementation
    pass

# Use descriptive names
contacts_by_tier = filter_contacts(tier=1)

# Use type hints
def get_contact(contact_id: int) -> dict:
    return contact_data
```

**Avoid:**
```python
# Bad
def calc(c,d=2):  # Unclear names
    # No docstring
    pass

# Bad
x = fc(1)  # Unclear variable name
```

### JavaScript/React Style

**Follow Airbnb Style Guide:**
```javascript
// Good
const NetworkMultipliers = ({ contacts }) => {
  const [sortedContacts, setSortedContacts] = useState([]);

  useEffect(() => {
    // Effect logic
  }, [contacts]);

  return (
    <div className="network-multipliers">
      {sortedContacts.map(contact => (
        <ContactCard key={contact.id} contact={contact} />
      ))}
    </div>
  );
};

// Use destructuring
const { name, company, tier } = contact;

// Use meaningful names
const isNetworkMultiplier = score > 0.8;
```

### General Guidelines

- **Write self-documenting code**
- **Add comments for complex logic**
- **Keep functions small and focused**
- **Use meaningful variable names**
- **Avoid magic numbers** (use constants)
- **Handle errors gracefully**
- **Log important events**

---

## ✅ Testing Guidelines

### Test Coverage

**Required:**
- All new features have tests
- Bug fixes include regression tests
- Critical paths tested
- Edge cases covered

### Python Tests

```python
# tests/test_network_analysis.py
import pytest
from core.scripts.network_analysis import calculate_network_multiplier

def test_network_multiplier_calculation():
    """Test network multiplier score calculation."""
    contact_id = 1
    score = calculate_network_multiplier(contact_id)

    assert 0.0 <= score <= 1.0
    assert isinstance(score, float)

def test_network_multiplier_with_no_connections():
    """Test multiplier for contact with no connections."""
    contact_id = 999  # No connections
    score = calculate_network_multiplier(contact_id)

    assert score == 0.0
```

**Run Tests:**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_network_analysis.py

# Run with coverage
pytest --cov=core/scripts
```

### Integration Tests

```bash
# Test CLI commands
./bin/newco contact list
./bin/newco network analyze

# Test LLM integration
python test_llm_integration.py

# Test Alpha Engine
cd agents/alpha-engine
yarn test
```

---

## 📚 Documentation

### Required Documentation

**For New Features:**
1. **Code comments** for complex logic
2. **Docstrings** for all functions/classes
3. **README updates** if public-facing
4. **CHANGELOG.md entry**
5. **User guide** in documentation/

**For Bug Fixes:**
1. **Issue reference** in commit
2. **Test demonstrating fix**
3. **CHANGELOG.md entry**

### Documentation Style

**Python Docstrings:**
```python
def find_warm_intro_path(source_id: int, target_id: int) -> list:
    """
    Find shortest warm introduction path between two contacts.

    Uses breadth-first search to find the shortest path through
    relationship graph, considering tie strength.

    Args:
        source_id (int): Starting contact ID
        target_id (int): Target contact ID

    Returns:
        list: List of contact IDs representing path, or empty if no path

    Raises:
        ValueError: If contact IDs don't exist

    Example:
        >>> path = find_warm_intro_path(1, 50)
        >>> print(path)
        [1, 25, 38, 50]
    """
    # Implementation
```

**Markdown Documentation:**
```markdown
# Feature Name

## Overview
Brief description of what this feature does.

## Usage
```bash
# Example command
./bin/newco network multipliers
```

## Options
- `--tier N` - Filter by tier
- `--min-score X` - Minimum multiplier score

## Examples
### Example 1: Basic Usage
```bash
./bin/newco network multipliers --tier 1
```

## Troubleshooting
Common issues and solutions.
```

### Updating Documentation

**Always update:**
- CHANGELOG.md
- Relevant guide in documentation/
- README.md if feature is user-facing
- Code comments and docstrings
- CLAUDE.md if affects AI assistant usage

---

## 🐛 Issue Guidelines

### Creating Issues

**Good Issue:**
```markdown
**Title:** [BUG] Email template fails for contacts without company

**Description:**
When generating emails for contacts without a company field,
the email generator crashes with KeyError.

**To Reproduce:**
1. Create contact without company: `./bin/newco contact add --name "John" --category "VC"`
2. Try to generate email: `./bin/newco email generate 123`
3. See error

**Expected:** Should use default or skip company mention
**Actual:** Crashes with KeyError: 'company'

**Environment:** macOS 14.0, Python 3.10.0
```

### Issue Labels

- `bug` → Something isn't working
- `enhancement` → New feature or request
- `documentation` → Documentation improvements
- `question` → Further information requested
- `help wanted` → Extra attention needed
- `good first issue` → Good for newcomers
- `priority-high` → Urgent fix needed
- `priority-low` → Can wait

---

## 🤝 Code Review Guidelines

### For Authors

**Before Requesting Review:**
- [ ] Self-review your code
- [ ] Test all changes
- [ ] Update documentation
- [ ] Resolve all conflicts
- [ ] Push latest changes

**During Review:**
- Respond to all comments
- Ask questions if feedback unclear
- Make requested changes promptly
- Be open to suggestions
- Thank reviewers for their time

### For Reviewers

**What to Check:**
1. **Correctness** - Does code work as intended?
2. **Tests** - Are there adequate tests?
3. **Documentation** - Is it documented?
4. **Style** - Follows coding standards?
5. **Security** - Any security concerns?
6. **Performance** - Efficient implementation?
7. **Maintainability** - Easy to understand?

**How to Review:**
- Be constructive and kind
- Explain the "why" behind suggestions
- Acknowledge good work
- Suggest alternatives, don't demand
- Focus on important issues first
- Review within 24-48 hours

---

## 🎯 Commit Message Format

### Format
```
<type>: <short description>

<detailed description>

<footer>
```

### Types
- `feat:` → New feature
- `fix:` → Bug fix
- `docs:` → Documentation
- `style:` → Formatting, no code change
- `refactor:` → Code restructuring
- `test:` → Adding tests
- `chore:` → Maintenance

### Examples

**Good:**
```
feat: add network multiplier identification

- Implement composite scoring algorithm
- Add CLI command `network multipliers`
- Include tie strength weighting
- Based on Bonacich (1987) centrality

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Good:**
```
fix: handle missing company field in email templates

- Add fallback for contacts without company
- Update email templates with conditional
- Add test for edge case
- Fixes #42
```

**Bad:**
```
updated stuff  # Too vague
```

---

## 🚫 What Not to Commit

**Never commit:**
- API keys or credentials
- `.env` files (use `.env.example` instead)
- Large binary files (>10MB)
- Generated files (dist/, build/)
- OS files (.DS_Store, Thumbs.db)
- IDE settings (.vscode/, .idea/)
- Personal data or PII
- Temporary files (*.tmp, *.log)

**Check .gitignore:**
- Review before first commit
- Add patterns as needed
- Keep it updated

---

## 📞 Getting Help

### Questions?

**Check these first:**
1. README.md
2. CHANGELOG.md
3. COLLABORATION_GUIDE.md
4. documentation/
5. Existing Issues

**Still stuck?**
1. Create a GitHub Issue with `question` label
2. Tag relevant files/features
3. Provide context and what you've tried

### Support

- **GitHub Issues** → Bug reports, feature requests
- **Pull Requests** → Code contributions
- **Discussions** → General questions (coming soon)

---

## 🎉 Thank You!

Your contributions make this project better. We appreciate:
- Bug reports and fixes
- Feature suggestions
- Documentation improvements
- Code reviews
- Testing feedback
- Any other help!

**Happy coding! 🚀**

---

*Last Updated: February 14, 2026*
