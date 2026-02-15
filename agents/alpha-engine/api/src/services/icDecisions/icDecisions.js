import { db } from 'src/lib/db'
import { context } from '@redwoodjs/graphql-server'

export const icDecisions = ({ status }) => {
  const where = status ? { status } : {}
  return db.iCDecision.findMany({ where, include: { votes: { include: { user: true } }, deal: true }, orderBy: { deadline: 'asc' } })
}

export const icDecision = ({ id }) =>
  db.iCDecision.findUnique({ where: { id }, include: { votes: { include: { user: true } }, deal: true } })

export const castICVote = ({ input }) => {
  return db.iCVote.upsert({
    where: { decisionId_userId: { decisionId: input.decisionId, userId: context.currentUser.id } },
    create: { ...input, userId: context.currentUser.id },
    update: { vote: input.vote, conviction: input.conviction, comment: input.comment },
  })
}

export const updateICStatus = ({ id, status }) =>
  db.iCDecision.update({ where: { id }, data: { status } })
