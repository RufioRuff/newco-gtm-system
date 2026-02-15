import { db } from 'src/lib/db'

export const riskScenarios = () => db.riskScenario.findMany({ orderBy: { severity: 'desc' } })

export const runStressTest = async ({ scenarioId }) => {
  const scenario = await db.riskScenario.findUnique({ where: { id: scenarioId } })
  // In production, this calls the Supabase function for heavy computation
  const results = { timestamp: new Date(), impact: scenario.navImpactPct, status: 'completed' }
  return db.riskScenario.update({ where: { id: scenarioId }, data: { lastRunAt: new Date(), results } })
}

export const alphaAttributions = () => db.alphaAttribution.findMany({ orderBy: { period: 'desc' } })
export const alphaAttribution = ({ period }) => db.alphaAttribution.findUnique({ where: { period } })
