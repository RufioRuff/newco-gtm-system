import { db } from 'src/lib/db'

export const platformDeals = ({ status }) => {
  const where = status ? { status } : {}
  return db.platformDeal.findMany({ where, orderBy: { targetClose: 'asc' } })
}
