import { db } from 'src/lib/db'

export const companies = ({ sector, search }) => {
  const where = {}
  if (sector) where.sector = sector
  if (search) where.name = { contains: search, mode: 'insensitive' }
  return db.company.findMany({ where, orderBy: { lastValuation: 'desc' }, take: 100 })
}

export const company = ({ id }) =>
  db.company.findUnique({ where: { id }, include: { investments: { include: { fund: true } }, exitEvents: true, fundingRounds: { orderBy: { date: 'desc' } } } })
