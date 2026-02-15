import { db } from 'src/lib/db'

export const secondaryDeals = ({ status }) => {
  const where = status ? { status } : {}
  return db.secondaryDeal.findMany({ where, include: { fund: true, icDecision: { include: { votes: true } } }, orderBy: { createdAt: 'desc' } })
}

export const secondaryDeal = ({ id }) =>
  db.secondaryDeal.findUnique({ where: { id }, include: { fund: true, icDecision: { include: { votes: { include: { user: true } } } } } })

export const createSecondaryDeal = ({ input }) => db.secondaryDeal.create({ data: input })
export const updateDealStatus = ({ id, status }) => db.secondaryDeal.update({ where: { id }, data: { status } })
