import { db } from 'src/lib/db'

export const contacts = ({ tier, search, limit = 50 }) => {
  const where = {}
  if (tier) where.tier = tier
  if (search) where.name = { contains: search, mode: 'insensitive' }
  return db.contact.findMany({ where, take: limit, orderBy: { compositeScore: 'desc' }, include: { companies: { include: { company: true }, where: { current: true } } } })
}

export const contact = ({ id }) =>
  db.contact.findUnique({ where: { id }, include: { companies: { include: { company: true } } } })

export const networkEdges = ({ contactId }) => {
  const where = contactId ? { OR: [{ sourceId: contactId }, { targetId: contactId }] } : {}
  return db.networkEdge.findMany({ where, include: { source: true, target: true } })
}

export const createContact = ({ input }) => db.contact.create({ data: input })

export const updateContactScores = ({ id, reach, authority, velocity }) => {
  const composite = Math.round(((reach || 0) + (authority || 0) + (velocity || 0)) / 3)
  return db.contact.update({ where: { id }, data: { reachScore: reach, authorityScore: authority, velocityScore: velocity, compositeScore: composite } })
}
