// ╔══════════════════════════════════════════════════════════════════════════╗
// ║  NEWCO V10 — PROJECT CONFIGURATION & DEPLOYMENT                        ║
// ║  redwood.toml + vercel.json + .env + package.json                      ║
// ╚══════════════════════════════════════════════════════════════════════════╝


// ═══════════════════════════════════════════════════════════════
// redwood.toml
// ═══════════════════════════════════════════════════════════════

/*
[web]
  title = "NEWCO V10 — AI Safety & Trust VC Intelligence Platform"
  port = 8910
  apiUrl = "/.redwood/functions"
  includeEnvironmentVariables = [
    "REDWOOD_ENV_SUPABASE_URL",
    "REDWOOD_ENV_SUPABASE_ANON_KEY"
  ]

[api]
  port = 8911

[browser]
  open = true

[generate]
  tests = true
  stories = true

[notifications]
  versionUpdates = ["latest"]
*/


// ═══════════════════════════════════════════════════════════════
// vercel.json
// ═══════════════════════════════════════════════════════════════

const vercelConfig = {
  "framework": "redwoodjs",
  "buildCommand": "yarn rw deploy vercel",
  "outputDirectory": "web/dist",
  "devCommand": "yarn rw dev",
  "installCommand": "yarn install",
  "regions": ["sfo1"],
  "functions": {
    "api/src/functions/**/*.{js,ts}": {
      "memory": 1024,
      "maxDuration": 30
    }
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "*" },
        { "key": "Access-Control-Allow-Methods", "value": "GET, POST, PUT, DELETE, OPTIONS" },
        { "key": "Access-Control-Allow-Headers", "value": "Content-Type, Authorization" }
      ]
    }
  ],
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}


// ═══════════════════════════════════════════════════════════════
// .env (template — never commit actual values)
// ═══════════════════════════════════════════════════════════════

const envTemplate = `
# ── Supabase ──
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
REDWOOD_ENV_SUPABASE_URL=https://your-project.supabase.co
REDWOOD_ENV_SUPABASE_ANON_KEY=eyJ...

# ── Database (Supabase Postgres direct) ──
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres

# ── Anthropic (for AI agents) ──
ANTHROPIC_API_KEY=sk-ant-...

# ── Auth ──
SESSION_SECRET=your-session-secret-min-32-chars

# ── GitHub (for CI/CD) ──
GITHUB_REPO=evil-twin-capital/newco-v10
GITHUB_TOKEN=ghp_...

# ── Vercel ──
VERCEL_TOKEN=...
VERCEL_ORG_ID=...
VERCEL_PROJECT_ID=...

# ── External APIs ──
PITCHBOOK_API_KEY=...
PREQIN_API_KEY=...
OPENAI_API_KEY=sk-...    # backup model for non-critical tasks
`


// ═══════════════════════════════════════════════════════════════
// package.json (web workspace)
// ═══════════════════════════════════════════════════════════════

const webPackageJson = {
  "name": "newco-v10-web",
  "version": "10.0.0",
  "private": true,
  "dependencies": {
    "@redwoodjs/forms": "^7.0.0",
    "@redwoodjs/router": "^7.0.0",
    "@redwoodjs/web": "^7.0.0",
    "@supabase/supabase-js": "^2.45.0",
    "d3": "^7.9.0",
    "framer-motion": "^11.5.0",
    "lucide-react": "^0.263.1",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "recharts": "^2.12.0",
    "date-fns": "^3.6.0",
    "zustand": "^4.5.0"
  },
  "devDependencies": {
    "@types/d3": "^7.4.0",
    "@types/react": "^18.3.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.5.0"
  }
}


// ═══════════════════════════════════════════════════════════════
// package.json (api workspace)
// ═══════════════════════════════════════════════════════════════

const apiPackageJson = {
  "name": "newco-v10-api",
  "version": "10.0.0",
  "private": true,
  "dependencies": {
    "@redwoodjs/api": "^7.0.0",
    "@redwoodjs/graphql-server": "^7.0.0",
    "@supabase/supabase-js": "^2.45.0",
    "@anthropic-ai/sdk": "^0.30.0",
    "graphql": "^16.9.0",
    "graphql-tag": "^2.12.0",
    "jsonwebtoken": "^9.0.0",
    "zod": "^3.23.0"
  }
}


// ═══════════════════════════════════════════════════════════════
// GitHub Actions CI/CD Pipeline
// .github/workflows/deploy.yml
// ═══════════════════════════════════════════════════════════════

const githubActionsWorkflow = `
name: NEWCO V10 Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  SUPABASE_URL: \${{ secrets.SUPABASE_URL }}
  SUPABASE_ANON_KEY: \${{ secrets.SUPABASE_ANON_KEY }}
  SUPABASE_SERVICE_ROLE_KEY: \${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}
  DATABASE_URL: \${{ secrets.DATABASE_URL }}
  ANTHROPIC_API_KEY: \${{ secrets.ANTHROPIC_API_KEY }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'yarn'
      - run: yarn install --frozen-lockfile
      - run: yarn rw lint
      - run: yarn rw test --no-watch
      - run: yarn rw type-check

  deploy-preview:
    needs: test
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'yarn'
      - run: yarn install --frozen-lockfile
      - name: Deploy to Vercel Preview
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: \${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: \${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: \${{ secrets.VERCEL_PROJECT_ID }}

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'yarn'
      - run: yarn install --frozen-lockfile

      - name: Run DB Migrations
        run: |
          npx supabase db push --linked

      - name: Deploy Edge Functions
        run: |
          npx supabase functions deploy run-agent
          npx supabase functions deploy daily-snapshot
          npx supabase functions deploy process-document

      - name: Deploy to Vercel Production
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: \${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: \${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: \${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'

      - name: Refresh Materialized Views
        run: |
          npx supabase db execute --sql "SELECT refresh_materialized_views();"
`


// ═══════════════════════════════════════════════════════════════
// Supabase Config
// supabase/config.toml
// ═══════════════════════════════════════════════════════════════

const supabaseConfig = `
[project]
id = "newco-v10"

[api]
enabled = true
port = 54321
schemas = ["public"]
extra_search_path = ["public"]
max_rows = 1000

[db]
port = 54322
major_version = 15

[studio]
enabled = true
port = 54323

[auth]
enabled = true
site_url = "http://localhost:8910"
additional_redirect_urls = ["https://newco-v10.vercel.app"]
jwt_expiry = 3600
enable_signup = false  # invite-only

[auth.email]
enable_signup = true
double_confirm_changes = true
enable_confirmations = true

[storage]
enabled = true
file_size_limit = "50MiB"

[realtime]
enabled = true

[functions]
verify_jwt = true

[analytics]
enabled = true
`


// ═══════════════════════════════════════════════════════════════
// PROJECT DIRECTORY STRUCTURE
// ═══════════════════════════════════════════════════════════════

const directoryStructure = `
newco-v10/
├── redwood.toml
├── package.json
├── vercel.json
├── .env
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── api/
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── lib/
│   │   │   ├── supabase.ts          # Supabase client (admin + user)
│   │   │   ├── helpers.ts           # Query helpers, case conversion
│   │   │   └── auth.ts              # Auth decoder for Supabase JWT
│   │   ├── graphql/
│   │   │   ├── funds.sdl.ts         # Fund & GP GraphQL types
│   │   │   ├── deals.sdl.ts         # Deal pipeline & IC types
│   │   │   ├── lps.sdl.ts           # LP management types
│   │   │   ├── network.sdl.ts       # Contact & network types
│   │   │   ├── signals.sdl.ts       # Signal intelligence types
│   │   │   ├── agents.sdl.ts        # Omniscient AI agent types
│   │   │   └── common.sdl.ts        # Shared types (TeamMember, Search)
│   │   ├── services/
│   │   │   ├── funds/
│   │   │   │   ├── funds.ts         # Fund CRUD + portfolio summary
│   │   │   │   └── funds.test.ts
│   │   │   ├── deals/
│   │   │   │   ├── deals.ts         # Deal pipeline + IC votes
│   │   │   │   └── deals.test.ts
│   │   │   ├── lps/
│   │   │   │   ├── lps.ts           # LP CRM + interactions
│   │   │   │   └── lps.test.ts
│   │   │   ├── network/
│   │   │   │   ├── network.ts       # Contact management + graph
│   │   │   │   └── network.test.ts
│   │   │   ├── signals/
│   │   │   │   ├── signals.ts       # Signal CRUD + real-time
│   │   │   │   └── signals.test.ts
│   │   │   ├── agents/
│   │   │   │   ├── agents.ts        # Agent config + runs + insights
│   │   │   │   └── agents.test.ts
│   │   │   ├── cashflows/
│   │   │   │   └── cashflows.ts     # Cash flow tracking + NAV history
│   │   │   ├── gpEvaluations/
│   │   │   │   └── gpEvaluations.ts # GP scorecard + reference calls
│   │   │   ├── platform/
│   │   │   │   └── platform.ts      # Platform apps + battlecards
│   │   │   └── search/
│   │   │       └── search.ts        # Global fuzzy search
│   │   └── functions/
│   │       └── graphql.ts           # GraphQL handler
│   └── db/
│       └── schema.sql               # Supabase migration (source of truth)
│
├── web/
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── App.tsx                  # Root app with auth provider
│   │   ├── Routes.tsx               # RedwoodJS router
│   │   ├── lib/
│   │   │   ├── supabase.ts          # Client-side Supabase
│   │   │   └── formatters.ts        # Currency, date, number formatters
│   │   ├── hooks/
│   │   │   ├── usePortfolio.ts      # Fund & portfolio hooks
│   │   │   ├── useDeals.ts          # Deal pipeline hooks
│   │   │   ├── useSignals.ts        # Real-time signal hooks
│   │   │   ├── useNetwork.ts        # Contact & network hooks
│   │   │   ├── useLps.ts            # LP management hooks
│   │   │   ├── useAgents.ts         # AI agent hooks
│   │   │   ├── useCashFlows.ts      # Cash flow & NAV hooks
│   │   │   └── useGlobalSearch.ts   # Global search hook
│   │   ├── components/
│   │   │   ├── ui/                  # Shared UI primitives
│   │   │   │   ├── Badge.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Stat.tsx
│   │   │   │   ├── Table.tsx
│   │   │   │   ├── Section.tsx
│   │   │   │   └── Charts/
│   │   │   │       ├── SparkLine.tsx
│   │   │   │       ├── DonutChart.tsx
│   │   │   │       ├── AreaChart.tsx
│   │   │   │       ├── HeatGrid.tsx
│   │   │   │       └── D3/
│   │   │   │           ├── Treemap.tsx
│   │   │   │           ├── JCurve.tsx
│   │   │   │           ├── Sankey.tsx
│   │   │   │           ├── Sunburst.tsx
│   │   │   │           ├── Chord.tsx
│   │   │   │           ├── NetworkGraph.tsx
│   │   │   │           └── Scatter.tsx
│   │   │   ├── layout/
│   │   │   │   ├── TopBar.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── CommandPalette.tsx
│   │   │   ├── overview/
│   │   │   │   └── OverviewDashboard.tsx
│   │   │   ├── analytics/
│   │   │   │   └── AlphaEngine.tsx   # 26-view analytics mega-component
│   │   │   ├── portfolio/
│   │   │   │   ├── FoFDashboard.tsx
│   │   │   │   ├── FundDetail.tsx
│   │   │   │   └── PositionDetail.tsx
│   │   │   ├── pipeline/
│   │   │   │   ├── DealPipeline.tsx
│   │   │   │   ├── DealDetail.tsx
│   │   │   │   └── IcVotePanel.tsx
│   │   │   ├── secondaries/
│   │   │   │   └── SecondariesMarket.tsx
│   │   │   ├── investors/
│   │   │   │   └── PublicMarketView.tsx
│   │   │   ├── lps/
│   │   │   │   ├── LPManagement.tsx
│   │   │   │   └── LPDetail.tsx
│   │   │   ├── network/
│   │   │   │   ├── NetworkDashboard.tsx
│   │   │   │   ├── ContactDetail.tsx
│   │   │   │   └── IntroPathFinder.tsx
│   │   │   ├── decision/
│   │   │   │   └── DecisionScienceEngine.tsx
│   │   │   ├── signals/
│   │   │   │   └── SignalsIntelligence.tsx
│   │   │   ├── ingest/
│   │   │   │   └── DataIngestion.tsx
│   │   │   └── agents/
│   │   │       ├── OmniscientHQ.tsx
│   │   │       ├── AgentDetail.tsx
│   │   │       └── InsightsPanel.tsx
│   │   └── pages/
│   │       ├── HomePage/
│   │       ├── LoginPage/
│   │       └── NotFoundPage/
│   └── public/
│       └── favicon.svg
│
├── supabase/
│   ├── config.toml
│   ├── migrations/
│   │   └── 20260212_initial_schema.sql
│   ├── seed.sql
│   └── functions/
│       ├── run-agent/
│       │   └── index.ts
│       ├── daily-snapshot/
│       │   └── index.ts
│       └── process-document/
│           └── index.ts
│
└── scripts/
    ├── seed-data.ts                 # Comprehensive seed data script
    └── refresh-views.ts             # Materialized view refresh
`

export { vercelConfig, envTemplate, webPackageJson, apiPackageJson, githubActionsWorkflow, supabaseConfig, directoryStructure }
