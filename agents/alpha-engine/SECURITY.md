# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability in this platform, please report it responsibly:

- Email: security@eviltwin.capital
- Do NOT create a public GitHub issue for security vulnerabilities

## Supported Versions

| Version | Supported |
|---------|-----------|
| V10.x   | ✅        |
| < V10   | ❌        |

## Security Measures

- Supabase Row-Level Security (RLS) on all tables
- Role-based access control: admin, analyst, lp_viewer, board_member
- Data sovereignty tiers (Local → Anonymized → Public)
- Audit trail on all NAV mark changes
- JWT-based authentication with auto-refresh
- CORS and CSP headers configured in Vercel
- No secrets in client bundles

## Data Classification

- **Tier 1 (Local Only)**: Raw emails, deal terms, LP communications
- **Tier 2 (Anonymized)**: Embeddings, semantic queries, aggregated analytics
- **Tier 3 (Public)**: News, market data, public filings
