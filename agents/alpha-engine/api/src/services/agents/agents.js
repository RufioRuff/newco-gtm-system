import { db } from 'src/lib/db'

export const agentRuns = ({ agentName, limit = 20 }) => {
  const where = agentName ? { agentName } : {}
  return db.agentRun.findMany({ where, take: limit, orderBy: { startedAt: 'desc' } })
}

export const aiInsights = ({ type, limit = 20 }) => {
  const where = type ? { type } : {}
  return db.aIInsight.findMany({ where, take: limit, orderBy: { createdAt: 'desc' } })
}

export const triggerAgent = async ({ input }) => {
  const run = await db.agentRun.create({
    data: { agentName: input.agentName, status: 'running', triggeredBy: 'manual', input: input.input },
  })
  // In production, this triggers Supabase Edge Function or background job
  // For now, mark as queued
  return run
}
