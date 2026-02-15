import { db } from 'src/lib/db'

export const exitEvents = ({ status }) => {
  const where = status ? { status } : {}
  return db.exitEvent.findMany({ where, include: { company: true }, orderBy: { expectedDate: 'asc' } })
}

export const exitEvent = ({ id }) =>
  db.exitEvent.findUnique({ where: { id }, include: { company: true } })

export const ExitEvent = {
  company: (_obj, { root }) => db.exitEvent.findUnique({ where: { id: root.id } }).company(),
}
