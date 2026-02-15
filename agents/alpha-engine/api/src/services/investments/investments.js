import { db } from 'src/lib/db'

export const investments = ({ fundId, status }) => {
  const where = {}
  if (fundId) where.fundId = fundId
  if (status) where.status = status
  return db.investment.findMany({ where, include: { company: true, fund: true }, orderBy: { investDate: 'desc' } })
}

export const investment = ({ id }) =>
  db.investment.findUnique({ where: { id }, include: { company: true, fund: true } })

export const createInvestment = ({ input }) =>
  db.investment.create({ data: input })

export const updateInvestmentValue = ({ id, currentValue, moic }) =>
  db.investment.update({ where: { id }, data: { currentValue, moic } })

export const Investment = {
  fund: (_obj, { root }) => db.investment.findUnique({ where: { id: root.id } }).fund(),
  company: (_obj, { root }) => db.investment.findUnique({ where: { id: root.id } }).company(),
}
