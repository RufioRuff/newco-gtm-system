import { db } from 'src/lib/db'

export const cashflows = ({ fundId, startDate, endDate }) => {
  const where = { fundId }
  if (startDate || endDate) {
    where.date = {}
    if (startDate) where.date.gte = startDate
    if (endDate) where.date.lte = endDate
  }
  return db.cashflow.findMany({ where, orderBy: { date: 'desc' } })
}

export const cashflowSummary = async ({ fundId }) => {
  const flows = await db.cashflow.findMany({ where: { fundId }, orderBy: { date: 'asc' } })
  const totalCalls = flows.filter(f => f.type === 'CAPITAL_CALL').reduce((s, f) => s + Number(f.amount), 0)
  const totalDist = flows.filter(f => f.type === 'DISTRIBUTION').reduce((s, f) => s + Number(f.amount), 0)
  const totalFees = flows.filter(f => ['MGMT_FEE', 'CARRY', 'EXPENSE'].includes(f.type)).reduce((s, f) => s + Number(f.amount), 0)
  return { totalCalls, totalDistributions: totalDist, totalFees, netCashflow: totalDist - totalCalls - totalFees, flowCount: flows.length }
}

export const createCashflow = ({ input }) => db.cashflow.create({ data: input })
