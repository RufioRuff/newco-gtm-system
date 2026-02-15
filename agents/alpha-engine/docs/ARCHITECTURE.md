# NEWCO V10 Architecture

## System Overview

```
┌──────────────────────────────────────────────────────────────┐
│                         CLIENT                                │
│  React 18 + D3.js + Lucide Icons                             │
│  Single-file AlphaEngine.jsx (15,124 lines)                  │
│  30+ views, 96 click handlers, 6 D3 visualizations           │
│  Hosted on Vercel Edge Network                                │
└────────────────────┬─────────────────────────────────────────┘
                     │ GraphQL / REST
┌────────────────────▼─────────────────────────────────────────┐
│                     API LAYER                                 │
│  RedwoodJS GraphQL API                                        │
│  ├── SDL Schema Definitions                                   │
│  ├── Service Resolvers                                        │
│  ├── Auth Middleware (Supabase JWT validation)                │
│  └── Directives (@requireAuth, @skipAuth)                    │
└────────────────────┬─────────────────────────────────────────┘
                     │ PostgreSQL + Realtime
┌────────────────────▼─────────────────────────────────────────┐
│                    DATABASE                                    │
│  Supabase PostgreSQL                                          │
│  ├── 20+ tables with RLS policies                            │
│  ├── Materialized views for analytics                        │
│  ├── Real-time subscriptions                                 │
│  └── Edge Functions (market data, NAV calc, alerts)          │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

```
Intelligence Feeds          Processing              Output Engines
─────────────────           ──────────              ──────────────
Secondary Pricing  ──┐
Hiring Velocity    ──┤
Burn Inference     ──┼──→  Omniscient ML  ──→  Risk-Adjusted NAV
IPO Probability    ──┤     Entity Graph        Rebalancing Signals
Revenue Estimation ──┤     Signal Fusion       Liquidity Alerts
Govt Procurement   ──┘     Bayesian Engine     Concentration Opt.
```

## Key Design Decisions

1. **Single-file Alpha Engine**: All 30+ views in one React component for instant
   tab switching with zero route changes. Trade-off: large file size for maximum
   interactivity and shared state.

2. **Inline CSS-in-JS**: No external stylesheets. Design tokens defined as JS
   constants for full programmatic control and theme consistency.

3. **Custom D3 Components**: Force graph, sunburst, chord diagram, waterfall charts
   all rendered as React components with D3 for calculation only.

4. **Supabase over custom backend**: Row-level security, real-time subscriptions,
   and edge functions reduce custom infrastructure to near-zero.

5. **RedwoodJS GraphQL**: Type-safe API layer with automatic SDL-to-resolver
   generation. Cells pattern for data loading states.
