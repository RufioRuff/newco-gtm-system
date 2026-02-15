// ╔══════════════════════════════════════════════════════════════════════════╗
// ║  NEWCO V10 — SUPABASE CLIENT & REDWOODJS SERVICES                      ║
// ║  api/src/lib/supabase.ts + api/src/services/*.ts                       ║
// ╚══════════════════════════════════════════════════════════════════════════╝

// ═══════════════════════════════════════════════════════════════
// api/src/lib/supabase.ts — Supabase Client
// ═══════════════════════════════════════════════════════════════

import { createClient, SupabaseClient } from '@supabase/supabase-js'
import type { Database } from '../types/supabase'

const supabaseUrl = process.env.SUPABASE_URL!
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY!
const supabaseAnonKey = process.env.SUPABASE_ANON_KEY!

// Service client (bypasses RLS — for server-side operations)
export const supabaseAdmin: SupabaseClient<Database> = createClient<Database>(
  supabaseUrl,
  supabaseServiceKey,
  {
    auth: { autoRefreshToken: false, persistSession: false },
    db: { schema: 'public' },
  }
)

// Anon client (respects RLS — for authenticated user context)
export const createUserClient = (accessToken: string): SupabaseClient<Database> =>
  createClient<Database>(supabaseUrl, supabaseAnonKey, {
    global: { headers: { Authorization: `Bearer ${accessToken}` } },
  })

// ═══════════════════════════════════════════════════════════════
// api/src/lib/helpers.ts — Query Helpers
// ═══════════════════════════════════════════════════════════════

export const paginate = (query: any, page = 1, perPage = 50) => {
  const from = (page - 1) * perPage
  const to = from + perPage - 1
  return query.range(from, to)
}

export const handleError = (error: any, context: string) => {
  if (error) {
    console.error(`[NEWCO] ${context}:`, error)
    throw new Error(`${context}: ${error.message}`)
  }
}

export const toCamelCase = (obj: Record<string, any>): Record<string, any> => {
  if (!obj || typeof obj !== 'object') return obj
  if (Array.isArray(obj)) return obj.map(toCamelCase)
  return Object.fromEntries(
    Object.entries(obj).map(([k, v]) => [
      k.replace(/_([a-z])/g, (_, c) => c.toUpperCase()),
      typeof v === 'object' && v !== null ? toCamelCase(v) : v,
    ])
  )
}

export const toSnakeCase = (obj: Record<string, any>): Record<string, any> => {
  if (!obj || typeof obj !== 'object') return obj
  if (Array.isArray(obj)) return obj.map(toSnakeCase)
  return Object.fromEntries(
    Object.entries(obj).map(([k, v]) => [
      k.replace(/[A-Z]/g, (c) => `_${c.toLowerCase()}`),
      typeof v === 'object' && v !== null ? toSnakeCase(v) : v,
    ])
  )
}


// ═══════════════════════════════════════════════════════════════
// api/src/services/funds/funds.ts
// ═══════════════════════════════════════════════════════════════

import { supabaseAdmin, handleError, toCamelCase, toSnakeCase } from 'src/lib/supabase'

export const gpFirms = async () => {
  const { data, error } = await supabaseAdmin
    .from('gp_firms')
    .select('*')
    .order('name')
  handleError(error, 'gpFirms')
  return data?.map(toCamelCase) ?? []
}

export const gpFirm = async ({ id }: { id: string }) => {
  const { data, error } = await supabaseAdmin
    .from('gp_firms')
    .select('*')
    .eq('id', id)
    .single()
  handleError(error, 'gpFirm')
  return toCamelCase(data)
}

export const funds = async ({
  strategy,
  status,
  vintageYear,
}: {
  strategy?: string
  status?: string
  vintageYear?: number
}) => {
  let query = supabaseAdmin
    .from('funds')
    .select(`
      *,
      gp_firms!inner (id, name, slug, health_score)
    `)
    .order('vintage_year', { ascending: false })

  if (strategy) query = query.eq('strategy', strategy)
  if (status) query = query.eq('status', status)
  if (vintageYear) query = query.eq('vintage_year', vintageYear)

  const { data, error } = await query
  handleError(error, 'funds')
  return data?.map(toCamelCase) ?? []
}

export const fund = async ({ id }: { id: string }) => {
  const { data, error } = await supabaseAdmin
    .from('funds')
    .select(`
      *,
      gp_firms (id, name, slug, hq_city, aum_millions, health_score, sector_focus),
      fund_company_positions (
        id, ownership_pct, cost_basis_millions, current_value_millions, moic, entry_date,
        portfolio_companies (id, name, sector, stage, last_valuation_millions)
      ),
      nav_history (id, report_date, nav_millions, tvpi, dpi, irr)
    `)
    .eq('id', id)
    .single()
  handleError(error, 'fund')
  return toCamelCase(data)
}

export const createFund = async ({ input }: { input: any }) => {
  const { data, error } = await supabaseAdmin
    .from('funds')
    .insert(toSnakeCase(input))
    .select()
    .single()
  handleError(error, 'createFund')
  return toCamelCase(data)
}

export const updateFund = async ({ id, input }: { id: string; input: any }) => {
  const { data, error } = await supabaseAdmin
    .from('funds')
    .update(toSnakeCase(input))
    .eq('id', id)
    .select()
    .single()
  handleError(error, 'updateFund')
  return toCamelCase(data)
}

export const portfolioCompanies = async ({
  sector,
  stage,
}: {
  sector?: string
  stage?: string
}) => {
  let query = supabaseAdmin
    .from('portfolio_companies')
    .select('*')
    .order('last_valuation_millions', { ascending: false })

  if (sector) query = query.eq('sector', sector)
  if (stage) query = query.eq('stage', stage)

  const { data, error } = await query
  handleError(error, 'portfolioCompanies')
  return data?.map(toCamelCase) ?? []
}

export const portfolioSummary = async () => {
  const { data: fundsData, error: fundsError } = await supabaseAdmin
    .from('funds')
    .select('nav_millions, committed_millions, called_millions, distributed_millions, irr, tvpi, dpi')
    .in('status', ['invested', 'harvesting', 'committed'])

  handleError(fundsError, 'portfolioSummary.funds')

  const { count: dealCount } = await supabaseAdmin
    .from('deals')
    .select('id', { count: 'exact', head: true })
    .not('status', 'in', '("fully_realized","declined")')

  const { count: signalCount } = await supabaseAdmin
    .from('signals')
    .select('id', { count: 'exact', head: true })
    .eq('is_read', false)

  const { count: companyCount } = await supabaseAdmin
    .from('fund_company_positions')
    .select('company_id', { count: 'exact', head: true })

  const f = fundsData ?? []
  const sum = (arr: any[], key: string) => arr.reduce((s, r) => s + (r[key] || 0), 0)
  const avg = (arr: any[], key: string) => {
    const vals = arr.filter(r => r[key] != null)
    return vals.length ? vals.reduce((s, r) => s + r[key], 0) / vals.length : 0
  }

  return {
    totalNav: sum(f, 'nav_millions'),
    totalCommitted: sum(f, 'committed_millions'),
    totalCalled: sum(f, 'called_millions'),
    totalDistributed: sum(f, 'distributed_millions'),
    weightedIrr: avg(f, 'irr'),
    weightedTvpi: avg(f, 'tvpi'),
    weightedDpi: avg(f, 'dpi'),
    fundCount: f.length,
    companyCount: companyCount ?? 0,
    activeDealCount: dealCount ?? 0,
    unreadSignalCount: signalCount ?? 0,
  }
}


// ═══════════════════════════════════════════════════════════════
// api/src/services/deals/deals.ts
// ═══════════════════════════════════════════════════════════════

export const deals = async ({
  status,
  dealType,
  signal,
  ownerId,
}: {
  status?: string
  dealType?: string
  signal?: string
  ownerId?: string
}) => {
  let query = supabaseAdmin
    .from('deals')
    .select(`
      *,
      team_members!deals_owner_id_fkey (id, name, role),
      gp_firms (id, name),
      funds (id, name, vintage_year)
    `)
    .order('conviction_score', { ascending: false })

  if (status) query = query.eq('status', status)
  if (dealType) query = query.eq('deal_type', dealType)
  if (signal) query = query.eq('signal', signal)
  if (ownerId) query = query.eq('owner_id', ownerId)

  const { data, error } = await query
  handleError(error, 'deals')
  return data?.map(toCamelCase) ?? []
}

export const deal = async ({ id }: { id: string }) => {
  const { data, error } = await supabaseAdmin
    .from('deals')
    .select(`
      *,
      team_members!deals_owner_id_fkey (id, name, role, title),
      gp_firms (id, name, slug, health_score),
      funds (id, name, vintage_year, nav_millions),
      portfolio_companies (id, name, sector, stage, last_valuation_millions),
      ic_votes (
        id, vote, conviction_score, rationale, conditions, voted_at,
        team_members (id, name, role)
      ),
      deal_activity (id, action, old_value, new_value, note, created_at,
        team_members (id, name)
      )
    `)
    .eq('id', id)
    .single()
  handleError(error, 'deal')
  return toCamelCase(data)
}

export const dealPipeline = async () => {
  const { data, error } = await supabaseAdmin
    .from('mv_deal_pipeline')
    .select('*')
  handleError(error, 'dealPipeline')
  return data?.map(toCamelCase) ?? []
}

export const hotDeals = async ({ minConviction = 80 }: { minConviction?: number }) => {
  const { data, error } = await supabaseAdmin
    .from('deals')
    .select(`
      *,
      team_members!deals_owner_id_fkey (id, name),
      gp_firms (id, name),
      funds (id, name)
    `)
    .gte('conviction_score', minConviction)
    .not('status', 'in', '("fully_realized","declined")')
    .order('conviction_score', { ascending: false })
    .limit(10)
  handleError(error, 'hotDeals')
  return data?.map(toCamelCase) ?? []
}

export const createDeal = async ({ input }: { input: any }) => {
  const { data, error } = await supabaseAdmin
    .from('deals')
    .insert(toSnakeCase(input))
    .select()
    .single()
  handleError(error, 'createDeal')

  // Log activity
  await supabaseAdmin.from('deal_activity').insert({
    deal_id: data.id,
    action: 'created',
    new_value: input.name,
  })

  return toCamelCase(data)
}

export const updateDeal = async ({ id, input }: { id: string; input: any }) => {
  const { data, error } = await supabaseAdmin
    .from('deals')
    .update(toSnakeCase(input))
    .eq('id', id)
    .select()
    .single()
  handleError(error, 'updateDeal')
  return toCamelCase(data)
}

export const castIcVote = async ({ input }: { input: any }) => {
  const { data, error } = await supabaseAdmin
    .from('ic_votes')
    .upsert(toSnakeCase(input), { onConflict: 'deal_id,voter_id' })
    .select(`
      *,
      team_members (id, name, role)
    `)
    .single()
  handleError(error, 'castIcVote')
  return toCamelCase(data)
}

export const addDealNote = async ({ dealId, note }: { dealId: string; note: string }) => {
  const { data, error } = await supabaseAdmin
    .from('deal_activity')
    .insert({ deal_id: dealId, action: 'note_added', note })
    .select()
    .single()
  handleError(error, 'addDealNote')
  return toCamelCase(data)
}


// ═══════════════════════════════════════════════════════════════
// api/src/services/lps/lps.ts
// ═══════════════════════════════════════════════════════════════

export const lps = async ({
  status,
  lpType,
  channel,
}: {
  status?: string
  lpType?: string
  channel?: string
}) => {
  let query = supabaseAdmin
    .from('lps')
    .select('*')
    .order('committed_millions', { ascending: false })

  if (status) query = query.eq('status', status)
  if (lpType) query = query.eq('lp_type', lpType)
  if (channel) query = query.eq('channel', channel)

  const { data, error } = await query
  handleError(error, 'lps')
  return data?.map(toCamelCase) ?? []
}

export const lp = async ({ id }: { id: string }) => {
  const { data, error } = await supabaseAdmin
    .from('lps')
    .select(`
      *,
      lp_interactions (id, interaction_type, subject, notes, sentiment, follow_up_date, occurred_at,
        team_members (id, name)
      ),
      lp_reports (id, report_type, period, title, sent_at, opened_at)
    `)
    .eq('id', id)
    .single()
  handleError(error, 'lp')
  return toCamelCase(data)
}

export const lpPipeline = async () => {
  const { data: allLps, error } = await supabaseAdmin
    .from('lps')
    .select('status, lp_type, channel, committed_millions')
  handleError(error, 'lpPipeline')

  const all = allLps ?? []
  const byStatus = all.reduce((acc: any, l) => {
    acc[l.status] = (acc[l.status] || 0) + 1
    return acc
  }, {})
  const byChannel = all.reduce((acc: any, l) => {
    acc[l.channel || 'Unknown'] = (acc[l.channel || 'Unknown'] || 0) + 1
    return acc
  }, {})
  const committed = all.filter(l => l.status === 'invested' || l.status === 're_upping')
  const totalCommitted = committed.reduce((s, l) => s + (l.committed_millions || 0), 0)

  return {
    totalCommitted,
    totalPipeline: all.reduce((s, l) => s + (l.committed_millions || 0), 0),
    lpCount: all.length,
    byStatus,
    byChannel,
    conversionRate: all.length > 0 ? committed.length / all.length : 0,
  }
}

export const createLp = async ({ input }: { input: any }) => {
  const { data, error } = await supabaseAdmin
    .from('lps')
    .insert({ ...toSnakeCase(input), first_contact_date: new Date().toISOString() })
    .select()
    .single()
  handleError(error, 'createLp')
  return toCamelCase(data)
}

export const updateLp = async ({ id, input }: { id: string; input: any }) => {
  const { data, error } = await supabaseAdmin
    .from('lps')
    .update(toSnakeCase(input))
    .eq('id', id)
    .select()
    .single()
  handleError(error, 'updateLp')
  return toCamelCase(data)
}

export const logLpInteraction = async ({ input }: { input: any }) => {
  const { data, error } = await supabaseAdmin
    .from('lp_interactions')
    .insert(toSnakeCase(input))
    .select()
    .single()
  handleError(error, 'logLpInteraction')
  return toCamelCase(data)
}


// ═══════════════════════════════════════════════════════════════
// api/src/services/network/network.ts
// ═══════════════════════════════════════════════════════════════

export const contacts = async ({
  tier,
  organizationType,
  search,
}: {
  tier?: string
  organizationType?: string
  search?: string
}) => {
  let query = supabaseAdmin
    .from('contacts')
    .select(`
      *,
      team_members!contacts_relationship_owner_id_fkey (id, name)
    `)
    .order('network_score', { ascending: false })

  if (tier) query = query.eq('tier', tier)
  if (organizationType) query = query.eq('organization_type', organizationType)
  if (search) query = query.or(`name.ilike.%${search}%,organization.ilike.%${search}%`)

  const { data, error } = await query.limit(200)
  handleError(error, 'contacts')
  return data?.map(toCamelCase) ?? []
}

export const contact = async ({ id }: { id: string }) => {
  const { data, error } = await supabaseAdmin
    .from('contacts')
    .select(`
      *,
      team_members!contacts_relationship_owner_id_fkey (id, name, role),
      contact_interactions (id, interaction_type, channel, subject, notes, sentiment, occurred_at),
      contact_relationships!contact_relationships_contact_a_id_fkey (
        contact_b_id,
        relationship_type,
        strength
      )
    `)
    .eq('id', id)
    .single()
  handleError(error, 'contact')
  return toCamelCase(data)
}

export const networkStats = async () => {
  const { data: allContacts, error } = await supabaseAdmin
    .from('contacts')
    .select('id, tier, network_score, relationship_strength, last_contact_date')
  handleError(error, 'networkStats')

  const all = allContacts ?? []
  const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString()

  const { count: recentInteractions } = await supabaseAdmin
    .from('contact_interactions')
    .select('id', { count: 'exact', head: true })
    .gte('occurred_at', thirtyDaysAgo)

  return {
    totalContacts: all.length,
    tier1Count: all.filter(c => c.tier === 'tier1').length,
    avgNetworkScore: all.length > 0
      ? all.reduce((s, c) => s + (c.network_score || 0), 0) / all.length
      : 0,
    decayingRelationships: all.filter(c => c.relationship_strength === 'Decaying').length,
    recentInteractions: recentInteractions ?? 0,
    introPathsAvailable: 0, // computed by graph analysis
  }
}


// ═══════════════════════════════════════════════════════════════
// api/src/services/signals/signals.ts
// ═══════════════════════════════════════════════════════════════

export const signals = async ({
  signalType,
  severity,
  unreadOnly,
}: {
  signalType?: string
  severity?: string
  unreadOnly?: boolean
}) => {
  let query = supabaseAdmin
    .from('signals')
    .select(`
      *,
      funds (id, name),
      gp_firms (id, name),
      portfolio_companies (id, name),
      deals (id, name)
    `)
    .order('created_at', { ascending: false })
    .limit(100)

  if (signalType) query = query.eq('signal_type', signalType)
  if (severity) query = query.eq('severity', severity)
  if (unreadOnly) query = query.eq('is_read', false)

  const { data, error } = await query
  handleError(error, 'signals')
  return data?.map(toCamelCase) ?? []
}

export const unreadSignalCount = async () => {
  const { count, error } = await supabaseAdmin
    .from('signals')
    .select('id', { count: 'exact', head: true })
    .eq('is_read', false)
  handleError(error, 'unreadSignalCount')
  return count ?? 0
}

export const markSignalRead = async ({ id }: { id: string }) => {
  const { data, error } = await supabaseAdmin
    .from('signals')
    .update({ is_read: true })
    .eq('id', id)
    .select()
    .single()
  handleError(error, 'markSignalRead')
  return toCamelCase(data)
}

export const actionSignal = async ({ id, actionTaken }: { id: string; actionTaken: string }) => {
  const { data, error } = await supabaseAdmin
    .from('signals')
    .update({
      is_actioned: true,
      action_taken: actionTaken,
      actioned_at: new Date().toISOString(),
    })
    .eq('id', id)
    .select()
    .single()
  handleError(error, 'actionSignal')
  return toCamelCase(data)
}


// ═══════════════════════════════════════════════════════════════
// api/src/services/agents/agents.ts
// ═══════════════════════════════════════════════════════════════

export const agents = async () => {
  const { data, error } = await supabaseAdmin
    .from('agent_configs')
    .select(`
      *,
      agent_runs (id, status, trigger, tokens_used, latency_ms, started_at, completed_at)
    `)
    .order('agent_runs.created_at', { ascending: false })
  handleError(error, 'agents')
  return data?.map(toCamelCase) ?? []
}

export const agent = async ({ id }: { id: string }) => {
  const { data, error } = await supabaseAdmin
    .from('agent_configs')
    .select(`
      *,
      agent_runs (id, status, trigger, tokens_used, latency_ms, error, started_at, completed_at, created_at),
      agent_insights (id, insight_type, title, content, confidence, impact_score, is_dismissed, is_actioned, created_at)
    `)
    .eq('id', id)
    .single()
  handleError(error, 'agent')
  return toCamelCase(data)
}

export const triggerAgentRun = async ({ agentId, input }: { agentId: string; input?: any }) => {
  // Create the run record
  const { data: run, error } = await supabaseAdmin
    .from('agent_runs')
    .insert({
      agent_id: agentId,
      status: 'pending',
      trigger: 'manual',
      input: input ?? {},
      started_at: new Date().toISOString(),
    })
    .select()
    .single()
  handleError(error, 'triggerAgentRun')

  // Update agent last_run_at
  await supabaseAdmin
    .from('agent_configs')
    .update({
      last_run_at: new Date().toISOString(),
      run_count: supabaseAdmin.rpc('increment_run_count', { agent_id: agentId }),
    })
    .eq('id', agentId)

  // In production, this would dispatch to a background job (Supabase Edge Function)
  // that calls the Claude API with the agent's system prompt
  // For now, mark as running
  await supabaseAdmin
    .from('agent_runs')
    .update({ status: 'running' })
    .eq('id', run.id)

  return toCamelCase(run)
}

export const agentInsights = async ({
  agentType,
  dismissed,
}: {
  agentType?: string
  dismissed?: boolean
}) => {
  let query = supabaseAdmin
    .from('agent_insights')
    .select(`
      *,
      agent_configs (id, name, agent_type)
    `)
    .order('created_at', { ascending: false })
    .limit(50)

  if (agentType) {
    query = query.eq('agent_configs.agent_type', agentType)
  }
  if (dismissed !== undefined) {
    query = query.eq('is_dismissed', dismissed)
  }

  const { data, error } = await query
  handleError(error, 'agentInsights')
  return data?.map(toCamelCase) ?? []
}


// ═══════════════════════════════════════════════════════════════
// api/src/services/search/search.ts
// ═══════════════════════════════════════════════════════════════

export const globalSearch = async ({ query }: { query: string }) => {
  const { data, error } = await supabaseAdmin.rpc('search_all', { query })
  handleError(error, 'globalSearch')
  return data?.map((r: any) => ({
    entityType: r.entity_type,
    entityId: r.entity_id,
    name: r.name,
    description: r.description,
    relevance: r.relevance,
  })) ?? []
}


// ═══════════════════════════════════════════════════════════════
// api/src/services/cashflows/cashflows.ts
// ═══════════════════════════════════════════════════════════════

export const cashFlows = async ({
  fundId,
  flowType,
  startDate,
  endDate,
}: {
  fundId?: string
  flowType?: string
  startDate?: string
  endDate?: string
}) => {
  let query = supabaseAdmin
    .from('cash_flows')
    .select(`
      *,
      funds (id, name)
    `)
    .order('flow_date', { ascending: false })

  if (fundId) query = query.eq('fund_id', fundId)
  if (flowType) query = query.eq('flow_type', flowType)
  if (startDate) query = query.gte('flow_date', startDate)
  if (endDate) query = query.lte('flow_date', endDate)

  const { data, error } = await query
  handleError(error, 'cashFlows')
  return data?.map(toCamelCase) ?? []
}

export const navTimeline = async ({ fundId }: { fundId?: string }) => {
  let query = fundId
    ? supabaseAdmin.from('nav_history').select('*').eq('fund_id', fundId)
    : supabaseAdmin.from('portfolio_nav_history').select('*')

  const { data, error } = await query.order('report_date', { ascending: true })
  handleError(error, 'navTimeline')
  return data?.map(toCamelCase) ?? []
}


// ═══════════════════════════════════════════════════════════════
// api/src/services/gpEvaluations/gpEvaluations.ts
// ═══════════════════════════════════════════════════════════════

export const gpEvaluations = async ({ gpFirmId }: { gpFirmId: string }) => {
  const { data, error } = await supabaseAdmin
    .from('gp_evaluations')
    .select(`
      *,
      team_members (id, name),
      funds (id, name)
    `)
    .eq('gp_firm_id', gpFirmId)
    .order('evaluation_date', { ascending: false })
  handleError(error, 'gpEvaluations')
  return data?.map(toCamelCase) ?? []
}

export const referenceCalls = async ({ gpFirmId }: { gpFirmId: string }) => {
  const { data, error } = await supabaseAdmin
    .from('reference_calls')
    .select(`
      *,
      team_members (id, name)
    `)
    .eq('gp_firm_id', gpFirmId)
    .order('call_date', { ascending: false })
  handleError(error, 'referenceCalls')
  return data?.map(toCamelCase) ?? []
}


// ═══════════════════════════════════════════════════════════════
// api/src/services/platform/platform.ts
// ═══════════════════════════════════════════════════════════════

export const platformApplications = async () => {
  const { data, error } = await supabaseAdmin
    .from('platform_applications')
    .select('*')
    .order('application_date', { ascending: false })
  handleError(error, 'platformApplications')
  return data?.map(toCamelCase) ?? []
}

export const advisorBattlecards = async ({ category }: { category?: string }) => {
  let query = supabaseAdmin
    .from('advisor_battlecards')
    .select('*')
    .order('effectiveness_score', { ascending: false })

  if (category) query = query.eq('category', category)

  const { data, error } = await query
  handleError(error, 'advisorBattlecards')
  return data?.map(toCamelCase) ?? []
}

// ═══════════════════════════════════════════════════════════════
// PUBLIC MARKETS SERVICES
// ═══════════════════════════════════════════════════════════════

export const stockPrices = async ({ days = 90 }: { days?: number }) => {
  const { data, error } = await supabaseAdmin
    .from('stock_prices')
    .select('*')
    .gte('date', new Date(Date.now() - days * 86400000).toISOString().split('T')[0])
    .order('date', { ascending: false })
  handleError(error, 'stockPrices')
  return data?.map(toCamelCase) ?? []
}

export const latestStockPrice = async () => {
  const { data, error } = await supabaseAdmin
    .from('stock_prices')
    .select('*')
    .order('date', { ascending: false })
    .limit(1)
    .single()
  handleError(error, 'latestStockPrice')
  return data ? toCamelCase(data) : null
}

export const navMarks = async ({ quarter }: { quarter?: string }) => {
  let query = supabaseAdmin
    .from('nav_marks')
    .select(`
      *,
      company:portfolio_companies(*),
      fund:funds(name, vintage_year),
      approver:team_members(name)
    `)
    .order('fair_value', { ascending: false })

  if (quarter) query = query.eq('quarter', quarter)

  const { data, error } = await query
  handleError(error, 'navMarks')
  return data?.map(toCamelCase) ?? []
}

export const fvcMeetings = async () => {
  const { data, error } = await supabaseAdmin
    .from('fvc_meetings')
    .select(`*, chair:team_members(name)`)
    .order('meeting_date', { ascending: false })
  handleError(error, 'fvcMeetings')
  return data?.map(toCamelCase) ?? []
}

export const shareholders = async ({ quarter, type }: { quarter?: string; type?: string }) => {
  let query = supabaseAdmin
    .from('shareholders')
    .select('*')
    .order('shares_held', { ascending: false })

  if (quarter) query = query.eq('filing_quarter', quarter)
  if (type) query = query.eq('institution_type', type)

  const { data, error } = await query
  handleError(error, 'shareholders')
  return data?.map(toCamelCase) ?? []
}

export const shortInterest = async ({ days = 180 }: { days?: number }) => {
  const { data, error } = await supabaseAdmin
    .from('short_interest')
    .select('*')
    .gte('report_date', new Date(Date.now() - days * 86400000).toISOString().split('T')[0])
    .order('report_date', { ascending: false })
  handleError(error, 'shortInterest')
  return data?.map(toCamelCase) ?? []
}

export const secFilings = async ({ status }: { status?: string }) => {
  let query = supabaseAdmin
    .from('sec_filings')
    .select(`
      *,
      preparer:team_members!preparer_id(name),
      reviewer:team_members!reviewer_id(name)
    `)
    .order('filing_deadline', { ascending: true })

  if (status) query = query.eq('status', status)

  const { data, error } = await query
  handleError(error, 'secFilings')
  return data?.map(toCamelCase) ?? []
}

export const atmTransactions = async ({ programName }: { programName?: string }) => {
  let query = supabaseAdmin
    .from('atm_transactions')
    .select('*')
    .order('transaction_date', { ascending: false })

  if (programName) query = query.eq('program_name', programName)

  const { data, error } = await query
  handleError(error, 'atmTransactions')
  return data?.map(toCamelCase) ?? []
}

export const atmSummary = async () => {
  const { data, error } = await supabaseAdmin
    .from('atm_transactions')
    .select('shares_sold, gross_proceeds, net_proceeds, commission, premium_captured')
  handleError(error, 'atmSummary')
  const totals = (data || []).reduce((acc, t) => ({
    totalShares: acc.totalShares + Number(t.shares_sold),
    totalGross: acc.totalGross + Number(t.gross_proceeds),
    totalNet: acc.totalNet + Number(t.net_proceeds),
    totalCommission: acc.totalCommission + Number(t.commission || 0),
    avgPremium: acc.avgPremium + Number(t.premium_captured || 0),
    count: acc.count + 1,
  }), { totalShares: 0, totalGross: 0, totalNet: 0, totalCommission: 0, avgPremium: 0, count: 0 })
  return { ...totals, avgPremium: totals.count > 0 ? totals.avgPremium / totals.count : 0 }
}

export const buybackTransactions = async () => {
  const { data, error } = await supabaseAdmin
    .from('buyback_transactions')
    .select('*')
    .order('transaction_date', { ascending: false })
  handleError(error, 'buybackTransactions')
  return data?.map(toCamelCase) ?? []
}

export const ipoEvents = async ({ status }: { status?: string }) => {
  let query = supabaseAdmin
    .from('ipo_events')
    .select(`
      *,
      company:portfolio_companies(name, sector)
    `)
    .order('probability', { ascending: false })

  if (status) query = query.eq('status', status)

  const { data, error } = await query
  handleError(error, 'ipoEvents')
  return data?.map(toCamelCase) ?? []
}

export const boardMembers = async () => {
  const { data, error } = await supabaseAdmin
    .from('board_members')
    .select('*')
    .eq('active', true)
    .order('is_independent', { ascending: true })
  handleError(error, 'boardMembers')
  return data?.map(toCamelCase) ?? []
}

export const tradingWindow = async () => {
  const { data, error } = await supabaseAdmin
    .from('trading_windows')
    .select('*')
    .gte('end_date', new Date().toISOString().split('T')[0])
    .order('start_date', { ascending: false })
    .limit(1)
    .single()
  handleError(error, 'tradingWindow')
  return data ? toCamelCase(data) : null
}

export const insiderTransactions = async ({ personName }: { personName?: string }) => {
  let query = supabaseAdmin
    .from('insider_transactions')
    .select('*')
    .order('transaction_date', { ascending: false })

  if (personName) query = query.eq('person_name', personName)

  const { data, error } = await query
  handleError(error, 'insiderTransactions')
  return data?.map(toCamelCase) ?? []
}

export const irMeetings = async ({ days = 90 }: { days?: number }) => {
  const { data, error } = await supabaseAdmin
    .from('ir_meetings')
    .select('*')
    .gte('meeting_date', new Date(Date.now() - days * 86400000).toISOString().split('T')[0])
    .order('meeting_date', { ascending: false })
  handleError(error, 'irMeetings')
  return data?.map(toCamelCase) ?? []
}

export const qaBank = async ({ category, status = 'active' }: { category?: string; status?: string }) => {
  let query = supabaseAdmin
    .from('qa_bank')
    .select(`*, owner:team_members(name)`)
    .order('frequency_asked', { ascending: false })

  if (category) query = query.eq('category', category)
  if (status) query = query.eq('status', status)

  const { data, error } = await query
  handleError(error, 'qaBank')
  return data?.map(toCamelCase) ?? []
}

export const governanceMeasures = async () => {
  const { data, error } = await supabaseAdmin
    .from('governance_measures')
    .select('*')
    .order('status', { ascending: true })
  handleError(error, 'governanceMeasures')
  return data?.map(toCamelCase) ?? []
}

export const complianceItems = async ({ status }: { status?: string }) => {
  let query = supabaseAdmin
    .from('compliance_items')
    .select(`*, reviewer:team_members(name)`)
    .order('risk_level', { ascending: true })

  if (status) query = query.eq('status', status)

  const { data, error } = await query
  handleError(error, 'complianceItems')
  return data?.map(toCamelCase) ?? []
}

export const lookThroughExposure = async ({ quarter, sector }: { quarter?: string; sector?: string }) => {
  let query = supabaseAdmin
    .from('look_through_exposure')
    .select('*')
    .order('pct_nav', { ascending: false })

  if (quarter) query = query.eq('quarter', quarter)
  if (sector) query = query.eq('sector', sector)

  const { data, error } = await query
  handleError(error, 'lookThroughExposure')
  return data?.map(toCamelCase) ?? []
}

export const publicMarketsSummary = async () => {
  const [price, si, atm, ipo, window] = await Promise.all([
    latestStockPrice(),
    shortInterest({ days: 1 }),
    atmSummary(),
    ipoEvents({ status: undefined }),
    tradingWindow(),
  ])
  return {
    stockPrice: price,
    shortInterest: si?.[0] ?? null,
    atmProgram: atm,
    ipoCount: ipo?.filter((e: any) => ['s1_prep','s1_filed','confidential_filing','roadshow'].includes(e.status)).length ?? 0,
    tradingWindow: window,
  }
}
