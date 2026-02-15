// ════════════════════════════════════════════════════
// DASHBOARD SERVICE — Aggregate metrics for overview
// ════════════════════════════════════════════════════
import { db } from 'src/lib/db'

export const dashboardMetrics = async () => {
  const [portfolio, network, recentActivity, urgentTasks, pendingDecisions, upcomingExits, latestInsights] =
    await Promise.all([
      getPortfolioSummary(),
      getNetworkSummary(),
      db.activity.findMany({ orderBy: { createdAt: 'desc' }, take: 20, include: { user: true } }),
      db.task.findMany({ where: { status: 'pending', priority: { lte: 2 } }, orderBy: { dueDate: 'asc' }, take: 10 }),
      db.iCDecision.findMany({ where: { status: 'PENDING' }, include: { votes: true }, orderBy: { deadline: 'asc' } }),
      db.exitEvent.findMany({ where: { status: { in: ['RUMORED', 'ANNOUNCED', 'IN_PROGRESS'] } }, include: { company: true }, orderBy: { expectedDate: 'asc' }, take: 10 }),
      db.aIInsight.findMany({ where: { isActioned: false }, orderBy: { createdAt: 'desc' }, take: 10 }),
    ])

  return { portfolio, networkSummary: network, recentActivity, urgentTasks, pendingDecisions, upcomingExits, latestInsights }
}

export const portfolioSummary = () => getPortfolioSummary()

async function getPortfolioSummary() {
  const activeFunds = await db.fund.findMany({
    where: { status: { in: ['ACTIVE', 'HARVESTING', 'COMMITTED'] } },
    include: {
      commitments: true,
      valuations: { orderBy: { asOfDate: 'desc' }, take: 1 },
    },
  })

  const totalAum = activeFunds.reduce((sum, f) => sum + (f.valuations[0]?.nav || 0), 0)
  const totalCommitted = activeFunds.reduce((sum, f) =>
    sum + f.commitments.reduce((s, c) => s + Number(c.amount), 0), 0)
  const totalUnfunded = activeFunds.reduce((sum, f) =>
    sum + f.commitments.reduce((s, c) => s + Number(c.unfunded), 0), 0)
  const totalDistributed = activeFunds.reduce((sum, f) =>
    sum + (f.valuations[0]?.distributed || 0), 0)

  const tvpis = activeFunds.filter(f => f.tvpiNet).map(f => Number(f.tvpiNet))
  const irrs = activeFunds.filter(f => f.irrNet).map(f => Number(f.irrNet))
  const topQuartile = activeFunds.filter(f => f.quartile === 1).length

  const activeDeals = await db.secondaryDeal.count({
    where: { status: { in: ['SCREENING', 'INITIAL_REVIEW', 'DUE_DILIGENCE', 'IC_REVIEW', 'NEGOTIATION'] } },
  })

  return {
    totalAum,
    fundCount: activeFunds.length,
    activeDeals,
    wtdTvpi: tvpis.length ? tvpis.reduce((a, b) => a + b, 0) / tvpis.length : 0,
    wtdIrr: irrs.length ? irrs.reduce((a, b) => a + b, 0) / irrs.length : 0,
    totalCommitted,
    totalUnfunded,
    totalDistributed,
    topQuartilePct: activeFunds.length ? (topQuartile / activeFunds.length) * 100 : 0,
  }
}

async function getNetworkSummary() {
  const [totalNodes, totalEdges, topContacts] = await Promise.all([
    db.contact.count(),
    db.networkEdge.count(),
    db.contact.findMany({
      orderBy: { compositeScore: 'desc' },
      take: 15,
      where: { compositeScore: { not: null } },
    }),
  ])

  const dualLpCustomer = await db.contact.count({
    where: { tier: { in: ['PLATFORM', 'CAPITAL'] } },
  })

  return {
    totalNodes,
    totalEdges,
    dualLpCustomer,
    estimatedAum: 0, // Computed from enrichment data
    platformReach: 0,
    topContacts,
  }
}
