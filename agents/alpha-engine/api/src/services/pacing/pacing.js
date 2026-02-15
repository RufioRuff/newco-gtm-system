import { db } from 'src/lib/db'

export const pacingPlans = () => db.pacingPlan.findMany({ orderBy: { year: 'desc' } })
export const pacingPlan = ({ year }) => db.pacingPlan.findUnique({ where: { year } })
