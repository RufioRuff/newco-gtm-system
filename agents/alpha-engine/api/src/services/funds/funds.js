// ════════════════════════════════════════════════════
// FUND SERVICE — Core portfolio management
// ════════════════════════════════════════════════════
import { db } from 'src/lib/db'
import { requireAuth } from 'src/lib/auth'

export const funds = ({ status, strategy }) => {
  const where = {}
  if (status) where.status = status
  if (strategy) where.strategy = strategy
  return db.fund.findMany({
    where,
    orderBy: { vintage: 'desc' },
    include: { commitments: true },
  })
}

export const fund = ({ id }) => {
  return db.fund.findUnique({
    where: { id },
    include: {
      commitments: true,
      investments: { include: { company: true } },
      valuations: { orderBy: { asOfDate: 'desc' }, take: 12 },
      gpScorecard: true,
      gpHealthChecks: { orderBy: { checkDate: 'desc' }, take: 4 },
    },
  })
}

export const createFund = ({ input }) => {
  requireAuth({ roles: ['ADMIN', 'GP'] })
  return db.fund.create({ data: input })
}

export const updateFund = ({ id, input }) => {
  requireAuth({ roles: ['ADMIN', 'GP'] })
  return db.fund.update({ where: { id }, data: input })
}

export const deleteFund = ({ id }) => {
  requireAuth({ roles: ['ADMIN'] })
  return db.fund.delete({ where: { id } })
}

export const fundValuations = ({ fundId }) => {
  return db.fundValuation.findMany({
    where: { fundId },
    orderBy: { asOfDate: 'desc' },
  })
}

// Nested resolvers
export const Fund = {
  commitments: (_obj, { root }) =>
    db.fund.findUnique({ where: { id: root.id } }).commitments(),
  investments: (_obj, { root }) =>
    db.fund.findUnique({ where: { id: root.id } }).investments({ include: { company: true } }),
  cashflows: (_obj, { root }) =>
    db.fund.findUnique({ where: { id: root.id } }).cashflows({ orderBy: { date: 'desc' } }),
  valuations: (_obj, { root }) =>
    db.fund.findUnique({ where: { id: root.id } }).valuations({ orderBy: { asOfDate: 'desc' } }),
  gpScorecard: (_obj, { root }) =>
    db.fund.findUnique({ where: { id: root.id } }).gpScorecard(),
  gpHealthChecks: (_obj, { root }) =>
    db.fund.findUnique({ where: { id: root.id } }).gpHealthChecks({ orderBy: { checkDate: 'desc' } }),
}
