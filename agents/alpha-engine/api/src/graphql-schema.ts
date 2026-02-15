// ╔══════════════════════════════════════════════════════════════════════════╗
// ║  NEWCO V10 — REDWOODJS GRAPHQL SCHEMA (SDL)                            ║
// ║  api/src/graphql/*.sdl.ts                                              ║
// ╚══════════════════════════════════════════════════════════════════════════╝

// ═══════════════════════════════════════════════════════════════
// api/src/graphql/funds.sdl.ts
// ═══════════════════════════════════════════════════════════════
export const fundsSchema = `
  type GpFirm {
    id: String!
    name: String!
    slug: String
    hqCity: String
    foundedYear: Int
    aumMillions: Float
    strategy: String
    sectorFocus: [String!]
    teamSize: Int
    website: String
    healthScore: Float
    healthFactors: JSON
    funds: [Fund!]!
    evaluations: [GpEvaluation!]!
    referenceCalls: [ReferenceCall!]!
    tags: [String!]
    createdAt: DateTime!
    updatedAt: DateTime!
  }

  type Fund {
    id: String!
    gpFirm: GpFirm!
    name: String!
    vintageYear: Int!
    strategy: String!
    status: String!
    fundSizeMillions: Float
    committedMillions: Float
    calledMillions: Float
    distributedMillions: Float
    navMillions: Float
    unfundedMillions: Float
    tvpi: Float
    dpi: Float
    irr: Float
    pme: Float
    quartile: Int
    mgmtFeeRate: Float
    carryRate: Float
    coInvestRights: Boolean
    advisoryBoardSeat: Boolean
    commitmentDate: Date
    sectorAllocation: JSON
    geoAllocation: JSON
    positions: [FundCompanyPosition!]!
    cashFlows: [CashFlow!]!
    navHistory: [NavHistory!]!
    deals: [Deal!]!
    tags: [String!]
    notes: String
    createdAt: DateTime!
    updatedAt: DateTime!
  }

  type FundCompanyPosition {
    id: String!
    fund: Fund!
    company: PortfolioCompany!
    ownershipPct: Float
    costBasisMillions: Float
    currentValueMillions: Float
    moic: Float
    entryDate: Date
    isLead: Boolean
    boardSeat: Boolean
  }

  type PortfolioCompany {
    id: String!
    name: String!
    sector: String
    subsector: String
    stage: String
    lastValuationMillions: Float
    revenueMillions: Float
    revenueGrowthPct: Float
    employees: Int
    website: String
    description: String
    thesis: String
    moatScore: Float
    publicTicker: String
    exitDate: Date
    exitType: String
    positions: [FundCompanyPosition!]!
    tags: [String!]
    createdAt: DateTime!
  }

  # ── Queries ──
  type Query {
    gpFirms: [GpFirm!]! @requireAuth
    gpFirm(id: String!): GpFirm @requireAuth
    funds(strategy: String, status: String, vintageYear: Int): [Fund!]! @requireAuth
    fund(id: String!): Fund @requireAuth
    portfolioCompanies(sector: String, stage: String): [PortfolioCompany!]! @requireAuth
    portfolioCompany(id: String!): PortfolioCompany @requireAuth
    portfolioSummary: PortfolioSummary! @requireAuth
  }

  type PortfolioSummary {
    totalNav: Float!
    totalCommitted: Float!
    totalCalled: Float!
    totalDistributed: Float!
    weightedIrr: Float!
    weightedTvpi: Float!
    weightedDpi: Float!
    fundCount: Int!
    companyCount: Int!
    activeDealCount: Int!
    unreadSignalCount: Int!
  }

  # ── Mutations ──
  type Mutation {
    createFund(input: CreateFundInput!): Fund! @requireAuth
    updateFund(id: String!, input: UpdateFundInput!): Fund! @requireAuth
    createGpFirm(input: CreateGpFirmInput!): GpFirm! @requireAuth
    updateGpFirm(id: String!, input: UpdateGpFirmInput!): GpFirm! @requireAuth
  }

  input CreateFundInput {
    gpFirmId: String!
    name: String!
    vintageYear: Int!
    strategy: String!
    fundSizeMillions: Float
    committedMillions: Float
    mgmtFeeRate: Float
    carryRate: Float
    coInvestRights: Boolean
    notes: String
  }

  input UpdateFundInput {
    name: String
    status: String
    calledMillions: Float
    distributedMillions: Float
    navMillions: Float
    irr: Float
    quartile: Int
    notes: String
  }

  input CreateGpFirmInput {
    name: String!
    hqCity: String
    foundedYear: Int
    aumMillions: Float
    strategy: String
    sectorFocus: [String!]
  }

  input UpdateGpFirmInput {
    name: String
    aumMillions: Float
    healthScore: Float
    healthFactors: JSON
  }
`

// ═══════════════════════════════════════════════════════════════
// api/src/graphql/deals.sdl.ts
// ═══════════════════════════════════════════════════════════════
export const dealsSchema = `
  type Deal {
    id: String!
    name: String!
    dealType: String!
    signal: String!
    fund: Fund
    gpFirm: GpFirm
    company: PortfolioCompany
    status: String!
    owner: TeamMember

    targetCommitmentMillions: Float
    minCommitmentMillions: Float
    maxCommitmentMillions: Float
    kellyOptimalMillions: Float

    convictionScore: Float
    bayesianScore: Float
    marketScore: Float
    timingScore: Float
    fitScore: Float

    askPricePct: Float
    bidPricePct: Float
    navMillions: Float
    discountPct: Float
    fairValuePct: Float

    irrBase: Float
    irrBull: Float
    irrBear: Float
    tvpiTarget: Float

    urgency: String
    deadline: Date
    expectedCloseDate: Date

    thesis: String
    catalysts: [String!]
    risks: [String!]
    comps: JSON

    icDate: Date
    icStatus: String
    icVotes: [IcVote!]!
    activity: [DealActivity!]!

    source: String
    tags: [String!]
    createdAt: DateTime!
    updatedAt: DateTime!
  }

  type IcVote {
    id: String!
    deal: Deal!
    voter: TeamMember!
    vote: String!
    convictionScore: Int
    rationale: String
    conditions: String
    votedAt: DateTime!
  }

  type DealActivity {
    id: String!
    deal: Deal!
    actor: TeamMember
    action: String!
    oldValue: String
    newValue: String
    note: String
    createdAt: DateTime!
  }

  type Query {
    deals(status: String, dealType: String, signal: String, ownerId: String): [Deal!]! @requireAuth
    deal(id: String!): Deal @requireAuth
    dealPipeline: [Deal!]! @requireAuth
    hotDeals(minConviction: Float): [Deal!]! @requireAuth
  }

  type Mutation {
    createDeal(input: CreateDealInput!): Deal! @requireAuth
    updateDeal(id: String!, input: UpdateDealInput!): Deal! @requireAuth
    castIcVote(input: CastVoteInput!): IcVote! @requireAuth
    addDealNote(dealId: String!, note: String!): DealActivity! @requireAuth
  }

  input CreateDealInput {
    name: String!
    dealType: String!
    fundId: String
    gpFirmId: String
    companyId: String
    ownerId: String
    targetCommitmentMillions: Float
    thesis: String
    catalysts: [String!]
    risks: [String!]
    urgency: String
    deadline: Date
    source: String
  }

  input UpdateDealInput {
    name: String
    signal: String
    status: String
    convictionScore: Float
    bayesianScore: Float
    marketScore: Float
    timingScore: Float
    fitScore: Float
    askPricePct: Float
    bidPricePct: Float
    irrBase: Float
    irrBull: Float
    irrBear: Float
    thesis: String
    catalysts: [String!]
    risks: [String!]
    icDate: Date
    icStatus: String
  }

  input CastVoteInput {
    dealId: String!
    vote: String!
    convictionScore: Int
    rationale: String
    conditions: String
  }
`

// ═══════════════════════════════════════════════════════════════
// api/src/graphql/lps.sdl.ts
// ═══════════════════════════════════════════════════════════════
export const lpsSchema = `
  type Lp {
    id: String!
    name: String!
    lpType: String
    status: String!
    committedMillions: Float
    calledMillions: Float
    distributionsMillions: Float
    contactName: String
    contactEmail: String
    firmName: String
    firmAumMillions: Float
    channel: String
    platformName: String
    advisorName: String
    suitabilityScore: Float
    riskTolerance: String
    accredited: Boolean
    qpStatus: Boolean
    ddqCompleted: Boolean
    kycAmlCompleted: Boolean
    interactions: [LpInteraction!]!
    reports: [LpReport!]!
    tags: [String!]
    notes: String
    source: String
    firstContactDate: Date
    commitmentDate: Date
    createdAt: DateTime!
    updatedAt: DateTime!
  }

  type LpInteraction {
    id: String!
    lp: Lp!
    teamMember: TeamMember
    interactionType: String
    subject: String
    notes: String
    sentiment: String
    followUpDate: Date
    followUpAction: String
    occurredAt: DateTime!
  }

  type LpReport {
    id: String!
    reportType: String
    period: String
    title: String!
    documentUrl: String
    sentAt: DateTime
    openedAt: DateTime
    createdAt: DateTime!
  }

  type LpPipelineSummary {
    totalCommitted: Float!
    totalPipeline: Float!
    lpCount: Int!
    byStatus: JSON!
    byChannel: JSON!
    conversionRate: Float!
  }

  type Query {
    lps(status: String, lpType: String, channel: String): [Lp!]! @requireAuth
    lp(id: String!): Lp @requireAuth
    lpPipeline: LpPipelineSummary! @requireAuth
  }

  type Mutation {
    createLp(input: CreateLpInput!): Lp! @requireAuth
    updateLp(id: String!, input: UpdateLpInput!): Lp! @requireAuth
    logLpInteraction(input: LogInteractionInput!): LpInteraction! @requireAuth
  }

  input CreateLpInput {
    name: String!
    lpType: String
    contactName: String
    contactEmail: String
    firmName: String
    channel: String
    platformName: String
    source: String
  }

  input UpdateLpInput {
    status: String
    committedMillions: Float
    suitabilityScore: Float
    riskTolerance: String
    ddqCompleted: Boolean
    kycAmlCompleted: Boolean
    notes: String
  }

  input LogInteractionInput {
    lpId: String!
    interactionType: String!
    subject: String
    notes: String
    sentiment: String
    followUpDate: Date
    followUpAction: String
  }
`

// ═══════════════════════════════════════════════════════════════
// api/src/graphql/network.sdl.ts
// ═══════════════════════════════════════════════════════════════
export const networkSchema = `
  type Contact {
    id: String!
    name: String!
    email: String
    title: String
    organization: String
    organizationType: String
    tier: String!
    relationshipOwner: TeamMember
    linkedinUrl: String
    location: String
    networkScore: Float
    centralityScore: Float
    influenceScore: Float
    activationPotential: Float
    lastContactDate: Date
    relationshipStrength: String
    source: String
    interactions: [ContactInteraction!]!
    connections: [Contact!]!
    tags: [String!]
    createdAt: DateTime!
    updatedAt: DateTime!
  }

  type ContactInteraction {
    id: String!
    contact: Contact!
    teamMember: TeamMember
    interactionType: String
    channel: String
    subject: String
    notes: String
    sentiment: String
    occurredAt: DateTime!
  }

  type NetworkStats {
    totalContacts: Int!
    tier1Count: Int!
    avgNetworkScore: Float!
    decayingRelationships: Int!
    recentInteractions: Int!
    introPathsAvailable: Int!
  }

  type Query {
    contacts(tier: String, organizationType: String, search: String): [Contact!]! @requireAuth
    contact(id: String!): Contact @requireAuth
    networkStats: NetworkStats! @requireAuth
    findIntroPath(fromId: String!, toId: String!): [Contact!]! @requireAuth
  }

  type Mutation {
    createContact(input: CreateContactInput!): Contact! @requireAuth
    updateContact(id: String!, input: UpdateContactInput!): Contact! @requireAuth
    logContactInteraction(input: LogContactInteractionInput!): ContactInteraction! @requireAuth
  }

  input CreateContactInput {
    name: String!
    email: String
    title: String
    organization: String
    organizationType: String
    tier: String
    relationshipOwnerId: String
    source: String
  }

  input UpdateContactInput {
    tier: String
    networkScore: Float
    relationshipStrength: String
    tags: [String!]
  }

  input LogContactInteractionInput {
    contactId: String!
    interactionType: String!
    channel: String
    subject: String
    notes: String
    sentiment: String
  }
`

// ═══════════════════════════════════════════════════════════════
// api/src/graphql/signals.sdl.ts
// ═══════════════════════════════════════════════════════════════
export const signalsSchema = `
  type Signal {
    id: String!
    signalType: String!
    severity: String!
    title: String!
    description: String
    source: String
    sourceUrl: String
    fund: Fund
    gpFirm: GpFirm
    company: PortfolioCompany
    deal: Deal
    aiSummary: String
    aiImpactScore: Float
    aiActionRequired: Boolean
    aiSuggestedActions: [String!]
    isRead: Boolean!
    isActioned: Boolean!
    actionedBy: TeamMember
    actionTaken: String
    expiresAt: DateTime
    createdAt: DateTime!
  }

  type Query {
    signals(signalType: String, severity: String, unreadOnly: Boolean): [Signal!]! @requireAuth
    signal(id: String!): Signal @requireAuth
    unreadSignalCount: Int! @requireAuth
  }

  type Mutation {
    markSignalRead(id: String!): Signal! @requireAuth
    actionSignal(id: String!, actionTaken: String!): Signal! @requireAuth
    dismissSignal(id: String!): Signal! @requireAuth
  }
`

// ═══════════════════════════════════════════════════════════════
// api/src/graphql/agents.sdl.ts
// ═══════════════════════════════════════════════════════════════
export const agentsSchema = `
  type AgentConfig {
    id: String!
    agentType: String!
    name: String!
    description: String
    isActive: Boolean!
    model: String
    schedule: String
    lastRunAt: DateTime
    runCount: Int
    avgLatencyMs: Int
    errorRate: Float
    recentRuns: [AgentRun!]!
    insights: [AgentInsight!]!
    createdAt: DateTime!
  }

  type AgentRun {
    id: String!
    agent: AgentConfig!
    status: String!
    trigger: String
    tokensUsed: Int
    latencyMs: Int
    error: String
    startedAt: DateTime
    completedAt: DateTime
    createdAt: DateTime!
  }

  type AgentInsight {
    id: String!
    agent: AgentConfig!
    insightType: String
    title: String!
    content: String!
    confidence: Float
    impactScore: Float
    isDismissed: Boolean!
    isActioned: Boolean!
    createdAt: DateTime!
  }

  type Query {
    agents: [AgentConfig!]! @requireAuth
    agent(id: String!): AgentConfig @requireAuth
    agentInsights(agentType: String, dismissed: Boolean): [AgentInsight!]! @requireAuth
  }

  type Mutation {
    triggerAgentRun(agentId: String!, input: JSON): AgentRun! @requireAuth
    toggleAgent(id: String!, active: Boolean!): AgentConfig! @requireAuth
    dismissInsight(id: String!): AgentInsight! @requireAuth
    actionInsight(id: String!): AgentInsight! @requireAuth
  }
`

// ═══════════════════════════════════════════════════════════════
// api/src/graphql/common.sdl.ts
// ═══════════════════════════════════════════════════════════════
export const commonSchema = `
  type TeamMember {
    id: String!
    name: String!
    email: String!
    role: String!
    title: String
    avatarUrl: String
    expertise: [String!]
    isActive: Boolean!
    joinedAt: DateTime
  }

  type SearchResult {
    entityType: String!
    entityId: String!
    name: String!
    description: String
    relevance: Float!
  }

  type Query {
    teamMembers: [TeamMember!]! @requireAuth
    teamMember(id: String!): TeamMember @requireAuth
    globalSearch(query: String!): [SearchResult!]! @requireAuth
  }

  scalar Date
  scalar DateTime
  scalar JSON
`
