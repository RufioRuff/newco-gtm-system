// ════════════════════════════════════════════════════
// NEWCO GraphQL Schema — All domains
// RedwoodJS auto-merges .sdl.js files
// ════════════════════════════════════════════════════

export const schema = gql`
  # ═══ SCALARS ═══
  scalar DateTime
  scalar JSON
  scalar Decimal

  # ═══ FUND MANAGEMENT ═══
  type Fund {
    id: String!
    name: String!
    shortName: String
    gpName: String!
    strategy: FundStrategy!
    vintage: Int!
    fundSize: Decimal!
    currency: String!
    status: FundStatus!
    inceptionDate: DateTime
    termYears: Int
    tvpiGross: Decimal
    tvpiNet: Decimal
    irrGross: Decimal
    irrNet: Decimal
    dpiNet: Decimal
    rvpiNet: Decimal
    pme: Decimal
    quartile: Int
    mgmtFeeRate: Decimal
    carryRate: Decimal
    preferredReturn: Decimal
    benchmarkIndex: String
    sector: String
    geography: String
    notes: String
    createdAt: DateTime!
    updatedAt: DateTime!
    commitments: [Commitment!]!
    investments: [Investment!]!
    cashflows: [Cashflow!]!
    valuations: [FundValuation!]!
    gpScorecard: GPScorecard
    gpHealthChecks: [GPHealthCheck!]!
  }

  enum FundStrategy {
    VENTURE
    GROWTH
    BUYOUT
    SECONDARY
    CO_INVEST
    FUND_OF_FUNDS
    REAL_ASSETS
    CREDIT
  }

  enum FundStatus {
    PROSPECTING
    DUE_DILIGENCE
    COMMITTED
    ACTIVE
    HARVESTING
    FULLY_REALIZED
    PASSED
  }

  type FundValuation {
    id: String!
    fundId: String!
    asOfDate: DateTime!
    nav: Decimal!
    totalValue: Decimal!
    paidIn: Decimal!
    distributed: Decimal!
    tvpi: Decimal!
    irr: Decimal
    dpi: Decimal
    createdAt: DateTime!
  }

  # ═══ INVESTMENTS & PORTFOLIO ═══
  type Investment {
    id: String!
    fundId: String!
    companyId: String!
    type: InvestmentType!
    status: InvestmentStatus!
    investDate: DateTime!
    costBasis: Decimal!
    currentValue: Decimal
    ownership: Decimal
    entryValuation: Decimal
    moic: Decimal
    irr: Decimal
    board: Boolean!
    leadInvestor: Boolean!
    notes: String
    fund: Fund!
    company: Company!
  }

  enum InvestmentType {
    PRIMARY
    SECONDARY
    CO_INVEST
    DIRECT
    SPV
    FOLLOW_ON
  }

  enum InvestmentStatus {
    ACTIVE
    PARTIALLY_REALIZED
    FULLY_REALIZED
    WRITTEN_OFF
    MARKED_UP
    MARKED_DOWN
  }

  type Company {
    id: String!
    name: String!
    domain: String
    sector: String
    subSector: String
    stage: String
    foundedYear: Int
    hqCity: String
    hqCountry: String
    description: String
    logoUrl: String
    employeeCount: Int
    lastRaised: Decimal
    lastValuation: Decimal
    isPublic: Boolean!
    investments: [Investment!]!
    exitEvents: [ExitEvent!]!
    fundingRounds: [FundingRound!]!
  }

  # ═══ CASHFLOWS ═══
  type Cashflow {
    id: String!
    fundId: String!
    type: CashflowType!
    amount: Decimal!
    date: DateTime!
    description: String
    category: String
    isProjected: Boolean!
    fund: Fund!
  }

  enum CashflowType {
    CAPITAL_CALL
    DISTRIBUTION
    MGMT_FEE
    CARRY
    EXPENSE
    RECALLABLE
  }

  # ═══ EXITS ═══
  type ExitEvent {
    id: String!
    companyId: String!
    type: ExitType!
    status: ExitStatus!
    expectedDate: DateTime
    actualDate: DateTime
    exitValuation: Decimal
    navImpact: Decimal
    probability: Int
    catalyst: String
    thesis: String
    sources: [String!]!
    company: Company!
  }

  enum ExitType { IPO SPAC MA SECONDARY_SALE TENDER_OFFER BUYBACK LIQUIDATION RECAPITALIZATION }
  enum ExitStatus { RUMORED ANNOUNCED IN_PROGRESS COMPLETED CANCELLED DELAYED }

  type FundingRound {
    id: String!
    companyId: String!
    round: String!
    date: DateTime!
    amountRaised: Decimal!
    preValuation: Decimal
    postValuation: Decimal
    leadInvestor: String
    investors: [String!]!
    company: Company!
  }

  # ═══ SECONDARY DEALS ═══
  type SecondaryDeal {
    id: String!
    fundId: String
    name: String!
    category: String!
    status: DealStatus!
    askPrice: Decimal
    bidPrice: Decimal
    nav: Decimal
    discountToNav: Decimal
    tvpi: Decimal
    vintage: Int
    fairValue: Decimal
    irrBase: Decimal
    irrBull: Decimal
    irrBear: Decimal
    thesis: String
    catalysts: [String!]!
    risks: [String!]!
    deadline: DateTime
    fund: Fund
    icDecision: ICDecision
  }

  enum DealStatus {
    SCREENING
    INITIAL_REVIEW
    DUE_DILIGENCE
    IC_REVIEW
    NEGOTIATION
    CLOSED
    PASSED
    LOST
  }

  # ═══ IC DECISIONS ═══
  type ICDecision {
    id: String!
    dealId: String
    title: String!
    type: String!
    amount: Decimal!
    deadline: DateTime
    status: ICStatus!
    compositeScore: Int
    scores: JSON
    thesis: String
    keyRisks: [String!]!
    mitigants: [String!]!
    votes: [ICVote!]!
    deal: SecondaryDeal
  }

  enum ICStatus { PENDING APPROVED REJECTED DEFERRED WITHDRAWN }

  type ICVote {
    id: String!
    decisionId: String!
    userId: String!
    vote: String!
    conviction: Int
    comment: String
    user: User!
  }

  # ═══ GP EVALUATION ═══
  type GPScorecard {
    id: String!
    fundId: String!
    returnsScore: Decimal
    teamScore: Decimal
    processScore: Decimal
    termsScore: Decimal
    fitScore: Decimal
    compositeScore: Decimal
    factorScores: JSON
    strengths: [String!]!
    concerns: [String!]!
    thesis: String
    benchmarkRank: String
    fund: Fund!
  }

  type GPHealthCheck {
    id: String!
    fundId: String!
    checkDate: DateTime!
    overallStatus: HealthStatus!
    aumStability: Int
    teamRetention: Int
    dealPace: Int
    styleDrift: Int
    lpSentiment: Int
    compliance: Int
    alerts: [String!]!
    signalSources: Int
    fund: Fund!
  }

  enum HealthStatus { HEALTHY WATCH ALERT CRITICAL }

  # ═══ CONTACTS & NETWORK ═══
  type Contact {
    id: String!
    name: String!
    email: String
    phone: String
    title: String
    linkedinUrl: String
    tier: ContactTier!
    type: String
    reachScore: Int
    authorityScore: Int
    velocityScore: Int
    compositeScore: Int
    lastContactedAt: DateTime
    companies: [ContactCompany!]!
  }

  enum ContactTier { PLATFORM CAPITAL MULTIPLIER INSTITUTIONAL BERKELEY TEAM GENERAL }

  type ContactCompany {
    id: String!
    contact: Contact!
    company: Company!
    role: String
    current: Boolean!
  }

  type NetworkEdge {
    id: String!
    sourceId: String!
    targetId: String!
    relationshipType: String!
    strength: Int
    source: Contact!
    target: Contact!
  }

  # ═══ PLATFORM & DISTRIBUTION ═══
  type PlatformDeal {
    id: String!
    platformName: String!
    status: PlatformStatus!
    contactName: String
    aum: Decimal
    advisorCount: Int
    minimumInvest: Decimal
    targetClose: DateTime
    estimatedAum: Decimal
    probability: Int
    nextAction: String
  }

  enum PlatformStatus {
    INITIAL_OUTREACH
    NDA_SIGNED
    DD_IN_PROGRESS
    COMMITTEE_REVIEW
    APPROVED
    LIVE_ON_PLATFORM
    DECLINED
  }

  # ═══ RISK & ALPHA ═══
  type RiskScenario {
    id: String!
    name: String!
    category: String!
    probability: Int
    severity: Int
    navImpactPct: Decimal
    description: String
    mitigants: [String!]!
    affectedFunds: [String!]!
    results: JSON
  }

  type AlphaAttribution {
    id: String!
    period: String!
    totalAlpha: Decimal!
    managerSelect: Decimal
    timingAlpha: Decimal
    coInvestAlpha: Decimal
    secondaryAlpha: Decimal
    sharpeRatio: Decimal
    infoRatio: Decimal
    hitRate: Decimal
    details: JSON
  }

  # ═══ AI SYSTEM ═══
  type AgentRun {
    id: String!
    agentName: String!
    status: String!
    triggeredBy: String
    output: JSON
    tokensUsed: Int
    costUsd: Decimal
    durationMs: Int
    error: String
    startedAt: DateTime!
    completedAt: DateTime
  }

  type AIInsight {
    id: String!
    agentName: String!
    type: String!
    title: String!
    content: String!
    confidence: Int
    entityType: String
    entityId: String
    isActioned: Boolean!
    createdAt: DateTime!
  }

  # ═══ ACTIVITIES & TASKS ═══
  type Activity {
    id: String!
    userId: String
    type: String!
    title: String!
    description: String
    entityType: String
    entityId: String
    metadata: JSON
    createdAt: DateTime!
    user: User
  }

  type Task {
    id: String!
    userId: String!
    title: String!
    description: String
    status: String!
    priority: Int!
    dueDate: DateTime
    entityType: String
    entityId: String
    user: User!
  }

  type Notification {
    id: String!
    userId: String!
    type: String!
    title: String!
    message: String
    isRead: Boolean!
    actionUrl: String
    createdAt: DateTime!
  }

  type User {
    id: String!
    email: String!
    name: String
    role: UserRole!
    avatarUrl: String
  }

  enum UserRole { ADMIN GP LP ANALYST VIEWER }

  # ═══ PACING ═══
  type PacingPlan {
    id: String!
    year: Int!
    targetCommit: Decimal!
    actualCommit: Decimal
    strategy: String
    vintageTarget: JSON
    jCurveData: JSON
  }

  # ═══ AGGREGATE/DASHBOARD TYPES ═══
  type PortfolioSummary {
    totalAum: Decimal!
    fundCount: Int!
    activeDeals: Int!
    wtdTvpi: Decimal!
    wtdIrr: Decimal!
    totalCommitted: Decimal!
    totalUnfunded: Decimal!
    totalDistributed: Decimal!
    topQuartilePct: Decimal!
  }

  type NetworkSummary {
    totalNodes: Int!
    totalEdges: Int!
    dualLpCustomer: Int!
    estimatedAum: Decimal!
    platformReach: Int!
    topContacts: [Contact!]!
  }

  type DashboardMetrics {
    portfolio: PortfolioSummary!
    networkSummary: NetworkSummary!
    recentActivity: [Activity!]!
    urgentTasks: [Task!]!
    pendingDecisions: [ICDecision!]!
    upcomingExits: [ExitEvent!]!
    latestInsights: [AIInsight!]!
  }

  # ═══════════════════════════════════════════
  # QUERIES
  # ═══════════════════════════════════════════

  type Query {
    # Dashboard
    dashboardMetrics: DashboardMetrics! @requireAuth
    portfolioSummary: PortfolioSummary! @requireAuth

    # Funds
    funds(status: FundStatus, strategy: FundStrategy): [Fund!]! @requireAuth
    fund(id: String!): Fund @requireAuth
    fundValuations(fundId: String!): [FundValuation!]! @requireAuth

    # Investments & Companies
    investments(fundId: String, status: InvestmentStatus): [Investment!]! @requireAuth
    investment(id: String!): Investment @requireAuth
    companies(sector: String, search: String): [Company!]! @requireAuth
    company(id: String!): Company @requireAuth

    # Cashflows
    cashflows(fundId: String!, startDate: DateTime, endDate: DateTime): [Cashflow!]! @requireAuth
    cashflowSummary(fundId: String!): JSON! @requireAuth

    # Exits
    exitEvents(status: ExitStatus): [ExitEvent!]! @requireAuth
    exitEvent(id: String!): ExitEvent @requireAuth

    # Secondary Deals
    secondaryDeals(status: DealStatus): [SecondaryDeal!]! @requireAuth
    secondaryDeal(id: String!): SecondaryDeal @requireAuth

    # IC Decisions
    icDecisions(status: ICStatus): [ICDecision!]! @requireAuth
    icDecision(id: String!): ICDecision @requireAuth

    # GP Evaluation
    gpScorecards: [GPScorecard!]! @requireAuth
    gpScorecard(fundId: String!): GPScorecard @requireAuth
    gpHealthChecks(fundId: String!): [GPHealthCheck!]! @requireAuth

    # Contacts & Network
    contacts(tier: ContactTier, search: String, limit: Int): [Contact!]! @requireAuth
    contact(id: String!): Contact @requireAuth
    networkEdges(contactId: String): [NetworkEdge!]! @requireAuth
    networkSummary: NetworkSummary! @requireAuth

    # Platform
    platformDeals(status: PlatformStatus): [PlatformDeal!]! @requireAuth

    # Risk & Alpha
    riskScenarios: [RiskScenario!]! @requireAuth
    alphaAttributions: [AlphaAttribution!]! @requireAuth
    alphaAttribution(period: String!): AlphaAttribution @requireAuth

    # Pacing
    pacingPlans: [PacingPlan!]! @requireAuth
    pacingPlan(year: Int!): PacingPlan @requireAuth

    # AI System
    agentRuns(agentName: String, limit: Int): [AgentRun!]! @requireAuth
    aiInsights(type: String, limit: Int): [AIInsight!]! @requireAuth

    # Activity & Tasks
    activities(entityType: String, limit: Int): [Activity!]! @requireAuth
    tasks(status: String): [Task!]! @requireAuth
    notifications(unreadOnly: Boolean): [Notification!]! @requireAuth
  }

  # ═══════════════════════════════════════════
  # MUTATIONS
  # ═══════════════════════════════════════════

  input CreateFundInput {
    name: String!
    gpName: String!
    strategy: FundStrategy!
    vintage: Int!
    fundSize: Decimal!
    currency: String
    status: FundStatus
    sector: String
    geography: String
    notes: String
  }

  input UpdateFundInput {
    name: String
    status: FundStatus
    tvpiNet: Decimal
    irrNet: Decimal
    dpiNet: Decimal
    quartile: Int
    notes: String
  }

  input CreateInvestmentInput {
    fundId: String!
    companyId: String!
    type: InvestmentType!
    investDate: DateTime!
    costBasis: Decimal!
    ownership: Decimal
    entryValuation: Decimal
    notes: String
  }

  input CreateCashflowInput {
    fundId: String!
    type: CashflowType!
    amount: Decimal!
    date: DateTime!
    description: String
    category: String
    isProjected: Boolean
  }

  input CreateICVoteInput {
    decisionId: String!
    vote: String!
    conviction: Int
    comment: String
  }

  input CreateSecondaryDealInput {
    name: String!
    category: String!
    fundId: String
    askPrice: Decimal
    bidPrice: Decimal
    nav: Decimal
    thesis: String
    catalysts: [String!]
    risks: [String!]
    deadline: DateTime
  }

  input CreateContactInput {
    name: String!
    email: String
    phone: String
    title: String
    tier: ContactTier
    type: String
  }

  input RunAgentInput {
    agentName: String!
    input: JSON
  }

  input CreateTaskInput {
    title: String!
    description: String
    priority: Int
    dueDate: DateTime
    entityType: String
    entityId: String
  }

  type Mutation {
    # Funds
    createFund(input: CreateFundInput!): Fund! @requireAuth(roles: ["ADMIN", "GP"])
    updateFund(id: String!, input: UpdateFundInput!): Fund! @requireAuth(roles: ["ADMIN", "GP"])
    deleteFund(id: String!): Fund! @requireAuth(roles: ["ADMIN"])

    # Investments
    createInvestment(input: CreateInvestmentInput!): Investment! @requireAuth(roles: ["ADMIN", "GP"])
    updateInvestmentValue(id: String!, currentValue: Decimal!, moic: Decimal): Investment! @requireAuth(roles: ["ADMIN", "GP"])

    # Cashflows
    createCashflow(input: CreateCashflowInput!): Cashflow! @requireAuth(roles: ["ADMIN", "GP"])

    # IC Decisions
    castICVote(input: CreateICVoteInput!): ICVote! @requireAuth(roles: ["ADMIN", "GP"])
    updateICStatus(id: String!, status: ICStatus!): ICDecision! @requireAuth(roles: ["ADMIN", "GP"])

    # Secondary Deals
    createSecondaryDeal(input: CreateSecondaryDealInput!): SecondaryDeal! @requireAuth(roles: ["ADMIN", "GP", "ANALYST"])
    updateDealStatus(id: String!, status: DealStatus!): SecondaryDeal! @requireAuth(roles: ["ADMIN", "GP"])

    # Contacts
    createContact(input: CreateContactInput!): Contact! @requireAuth
    updateContactScores(id: String!, reach: Int, authority: Int, velocity: Int): Contact! @requireAuth(roles: ["ADMIN", "GP"])

    # AI Agents
    triggerAgent(input: RunAgentInput!): AgentRun! @requireAuth(roles: ["ADMIN", "GP"])

    # Tasks
    createTask(input: CreateTaskInput!): Task! @requireAuth
    updateTaskStatus(id: String!, status: String!): Task! @requireAuth
    markNotificationRead(id: String!): Notification! @requireAuth

    # Risk
    runStressTest(scenarioId: String!): RiskScenario! @requireAuth(roles: ["ADMIN", "GP"])
  }
`
