import { db } from 'src/lib/db'

export const gpScorecards = () =>
  db.gPScorecard.findMany({ include: { fund: true }, orderBy: { compositeScore: 'desc' } })

export const gpScorecard = ({ fundId }) =>
  db.gPScorecard.findUnique({ where: { fundId }, include: { fund: true } })

export const gpHealthChecks = ({ fundId }) =>
  db.gPHealthCheck.findMany({ where: { fundId }, orderBy: { checkDate: 'desc' } })
