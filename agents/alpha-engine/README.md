# NEWCO V10 — Intelligence LP Platform

> **We are not blind LP capital. We are an Intelligence LP.**

NEWCO is an institutional-grade portfolio intelligence platform for a publicly traded venture fund. It transforms 6 proprietary data feeds into 4 strategic output engines, giving LPs and operators real-time visibility into a $193.7M NAV portfolio spanning AI Safety, Trust & Safety, GovTech, and Defense Tech.

![Platform](docs/screenshot-placeholder.png)

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    NEWCO V10                         │
│                                                     │
│  ┌───────────┐  ┌───────────┐  ┌─────────────────┐ │
│  │  React    │  │ RedwoodJS │  │   Supabase      │ │
│  │  Frontend │──│ GraphQL   │──│   PostgreSQL    │ │
│  │  (Vercel) │  │ API Layer │  │   + Edge Fns    │ │
│  └───────────┘  └───────────┘  └─────────────────┘ │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │         Intelligence Data Pipeline            │  │
│  │  Secondary Pricing · Hiring Velocity          │  │
│  │  Burn Inference · IPO Modeling                 │  │
│  │  Revenue Estimation · Govt Procurement        │  │
│  └───────────────────────────────────────────────┘  │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │         Strategic Output Engines              │  │
│  │  Risk-Adjusted NAV · Rebalancing Signals      │  │
│  │  Liquidity Stress · Concentration Optimizer   │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + D3.js | Single-file Alpha Engine with 30+ interactive views |
| **Styling** | Inline CSS-in-JS | Institutional dark theme with design tokens |
| **Charts** | Custom SVG + D3 | Force graphs, sunbursts, chord diagrams, waterfalls |
| **API** | RedwoodJS GraphQL | Type-safe data layer with SDL schema |
| **Database** | Supabase PostgreSQL | Row-level security, real-time subscriptions |
| **Edge Functions** | Supabase Edge | Market data feeds, NAV calculations, alerts |
| **Auth** | Supabase Auth + RLS | Role-based: admin, analyst, lp_viewer, board |
| **Hosting** | Vercel | Edge deployment with ISR |
| **Design** | Figma | Component library synced via tokens |
| **CI/CD** | GitHub Actions | Lint → Test → Deploy pipeline |

## Project Structure

```
newco-platform/
├── src/
│   ├── components/
│   │   └── AlphaEngine.jsx      # Main platform (15,124 lines, 30+ views)
│   ├── hooks/
│   │   └── index.ts             # Custom React hooks + Supabase edge functions
│   ├── lib/
│   │   └── config.ts            # Project configuration + environment setup
│   ├── pages/                   # Route pages (RedwoodJS)
│   └── styles/                  # Design tokens + theme
├── api/
│   ├── src/
│   │   ├── services.ts          # GraphQL resolvers + business logic
│   │   └── graphql-schema.ts    # SDL type definitions
│   └── db/
│       └── schema.sql           # Supabase PostgreSQL schema + RLS policies
├── public/                      # Static assets
├── docs/                        # Documentation
├── package.json
├── redwood.toml                 # RedwoodJS configuration
├── vercel.json                  # Vercel deployment config
├── .env.example                 # Environment variables template
└── README.md
```

## Views (30+)

### 🎯 Investment Intelligence
| View | Description | Interactive Features |
|------|-------------|---------------------|
| **Morning Pulse** | Daily strategic briefing with portfolio signals, calendar, urgency queue | Clickable signals → drill-downs, "What Should I Do Next?" |
| **Deal Radar** | Pipeline screening with multi-mode toggle (pipeline/heatmap/flowchart/thesis) | Mode switching, Monte Carlo links, IC memo generation |
| **IC Memo Generator** | Investment committee documentation with scoring frameworks | Auto-scoring, thesis alignment checks |
| **Position Sizing** | Kelly criterion + Monte Carlo allocation modeling | 5 interactive sliders, real-time recalculation |
| **Monte Carlo** | 10,000-path probability simulation engine | Confidence intervals, VaR/CVaR, scenario toggles |

### 📊 Portfolio Analytics
| View | Description | Interactive Features |
|------|-------------|---------------------|
| **Deep Dive** | Per-company analytics across all holdings | D3 force graph, entity hover cards |
| **NAV Marks** | Independent NAV methodology with GP variance analysis | Mark override sliders, audit trail |
| **Premium/Discount** | Public market premium analysis with ATM modeling | Multi-mode (analysis/sensitivity/history) |
| **IPO Watch** | Exit pipeline with probability modeling | 3 modes (tracker/timeline/NAV calculator), 5 IPO sliders |
| **Concentration** | HHI analysis + efficient frontier optimization | Portfolio optimizer with Sharpe ratio |

### 🏛️ Institutional Operations
| View | Description | Interactive Features |
|------|-------------|---------------------|
| **Capital Markets** | ATM program, buyback, shelf registration management | 3 modes (overview/simulator/buyback) |
| **Compliance** | Regulatory tracking, AFFE, BDC requirements | Status badges, deadline alerts |
| **Board Deck** | Quarterly board presentation generator | Auto-populated from live data |
| **Earnings Prep** | Quarterly call script with Q&A bank | 85 Q&As across 6 categories |
| **War Room** | Live situation management for time-critical events | Real-time status, action items |

### 📡 Distribution & IR
| View | Description | Interactive Features |
|------|-------------|---------------------|
| **IR Command** | Investor relations CRM and communication hub | Engagement scoring, outreach tracking |
| **LP Portal** | Limited partner self-service dashboard | Performance, documents, capital activity |
| **Fund II** | Next fund pipeline and fundraising tracker | Commitment tracking, LP scoring |
| **Shareholder** | Institutional ownership analysis and targeting | Activist defense, proxy advisory |
| **Platform** | Distribution channel strategy and RIA targeting | Suitability matrix, channel analytics |

### 🧠 Omniscient Intelligence
| View | Description | Interactive Features |
|------|-------------|---------------------|
| **Omniscient** | Intelligence LP thesis with 6 data feeds → 4 output engines | Feed status, signal drill-downs, flow diagram |
| **Agent Orchestra** | 8 AI agents with measured ROI and coordination | Agent status, capability mapping |
| **Network** | D3 force-directed relationship graph with 50K+ nodes | Interactive zoom, filtering, entity linking |

## Intelligence LP Data Architecture

### 6 Proprietary Data Inputs
1. **Secondary Pricing Feeds** — 18 platforms, bid/ask on 42 portfolio companies
2. **Hiring Velocity Analytics** — LinkedIn + GitHub reverse-engineered headcount
3. **Burn Multiple Inference** — Triangulated from cap table + hiring + cloud signals
4. **IPO Probability Modeling** — ML model trained on 2,400+ IPOs (82% accuracy)
5. **Revenue Trajectory Estimation** — Web traffic + API usage + job posting fusion
6. **Government Procurement Tracking** — SAM.gov + FPDS, $2.8B tracked contracts

### 4 Strategic Output Engines
1. **Risk-Adjusted NAV Modeling** — Independent marks +2.9% above GP reports
2. **Allocation Rebalancing Signals** — Concentration breach alerts, factor exposure
3. **Liquidity Stress Alerts** — Cash flow modeling under stress scenarios
4. **Concentration Optimization** — Markowitz-adapted portfolio optimizer (+18% Sharpe)

## UX Features

- **Strategic Action Center (SAC)** — Floating urgency bar with prioritized actions
- **Toast Notifications** — Success/info/error feedback on all interactions
- **Entity Hover Cards** — Instant company preview on hover (valuation, NAV, signal)
- **Command Palette** — `⌘K` quick jump to any view with recent history
- **Keyboard Shortcuts** — `←→` tab nav, `1-4` mode switch, `P` pulse, `ESC` cascade close
- **Contextual Quick Actions** — 3 workflow buttons per view
- **ViewNextSteps** — "What's next?" suggestions at bottom of every view
- **Breadcrumb Navigation** — Group → Section → View with active mode indicator
- **Interactive Drill-Downs** — Click any entity for full detail overlay with navigation

## Interactive Elements

| Type | Count |
|------|-------|
| Click handlers | 96 |
| Hover effects | 39 |
| Interactive sliders | 19 |
| Calculator inputs | 24 |
| Mode toggles | 14 |
| Drill-down triggers | 14 |
| Toast notifications | 22 |
| D3 visualizations | 6 |
| Keyboard shortcuts | 8 |

## Getting Started

### Prerequisites
- Node.js 20+
- Supabase account
- Vercel account (for deployment)

### Environment Setup

```bash
# Clone the repo
git clone https://github.com/eviltwin-capital/newco-platform.git
cd newco-platform

# Install dependencies
yarn install

# Copy environment template
cp .env.example .env

# Configure your environment variables
# See .env.example for required values

# Start development server
yarn rw dev
```

### Environment Variables

```env
SUPABASE_URL=your-project-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
DATABASE_URL=postgresql://...
VERCEL_URL=your-deployment-url
```

### Database Setup

```bash
# Apply Supabase schema
psql $DATABASE_URL < api/db/schema.sql

# Or via Supabase dashboard: paste contents of api/db/schema.sql
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## Development

```bash
# Start RedwoodJS dev server (API + Web)
yarn rw dev

# Run the platform standalone (React only)
cd src && npx vite

# Generate new GraphQL types
yarn rw g types

# Database migrations
yarn rw prisma migrate dev
```

## Security

- **Row-Level Security (RLS)** on all Supabase tables
- **Role-based access**: `admin`, `analyst`, `lp_viewer`, `board_member`
- **Data sovereignty tiers**: Local-only (Tier 1), Anonymized (Tier 2), Public (Tier 3)
- **Audit trail** on all NAV mark changes and compliance actions
- No sensitive data in client bundle — all via authenticated API calls

## Performance

- Single-file Alpha Engine: 15,124 lines, ~1.3MB
- Renders 30+ views with zero route changes (instant tab switching)
- D3 visualizations render client-side with requestAnimationFrame
- Supabase real-time subscriptions for live data updates
- Vercel Edge for <50ms TTFB globally

## Contributing

This is a private platform for Evil Twin Capital. Access is restricted to authorized team members.

## License

Proprietary — © 2026 Evil Twin Capital. All rights reserved.

---

**Built with** React · D3.js · RedwoodJS · Supabase · Vercel · Figma
