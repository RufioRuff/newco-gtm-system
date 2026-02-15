// ╔══════════════════════════════════════════════════════════════════════════╗
// ║  NEWCO V10 — REACT HOOKS & SUPABASE EDGE FUNCTIONS                     ║
// ║  web/src/hooks/ + supabase/functions/                                  ║
// ╚══════════════════════════════════════════════════════════════════════════╝

// ═══════════════════════════════════════════════════════════════
// web/src/lib/supabase.ts — Client-side Supabase
// ═══════════════════════════════════════════════════════════════

import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  process.env.REDWOOD_ENV_SUPABASE_URL!,
  process.env.REDWOOD_ENV_SUPABASE_ANON_KEY!
)

// Auth helpers
export const signIn = async (email: string, password: string) => {
  const { data, error } = await supabase.auth.signInWithPassword({ email, password })
  if (error) throw error
  return data
}

export const signUp = async (email: string, password: string, metadata: any) => {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: { data: metadata },
  })
  if (error) throw error
  return data
}

export const signOut = () => supabase.auth.signOut()

export const getSession = () => supabase.auth.getSession()


// ═══════════════════════════════════════════════════════════════
// web/src/hooks/usePortfolio.ts
// ═══════════════════════════════════════════════════════════════

import { useState, useEffect, useCallback, useMemo } from 'react'
import { supabase } from '../lib/supabase'

interface UseFundsOptions {
  strategy?: string
  status?: string
  vintageYear?: number
}

export function useFunds(options: UseFundsOptions = {}) {
  const [funds, setFunds] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchFunds = useCallback(async () => {
    setLoading(true)
    let query = supabase
      .from('funds')
      .select(`
        *,
        gp_firms (id, name, slug, health_score)
      `)
      .order('vintage_year', { ascending: false })

    if (options.strategy) query = query.eq('strategy', options.strategy)
    if (options.status) query = query.eq('status', options.status)
    if (options.vintageYear) query = query.eq('vintage_year', options.vintageYear)

    const { data, error: err } = await query
    if (err) setError(err.message)
    else setFunds(data ?? [])
    setLoading(false)
  }, [options.strategy, options.status, options.vintageYear])

  useEffect(() => { fetchFunds() }, [fetchFunds])

  // Real-time subscription
  useEffect(() => {
    const channel = supabase
      .channel('funds-changes')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'funds' }, () => {
        fetchFunds()
      })
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [fetchFunds])

  return { funds, loading, error, refetch: fetchFunds }
}

export function useFund(id: string | null) {
  const [fund, setFund] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    supabase
      .from('funds')
      .select(`
        *,
        gp_firms (*),
        fund_company_positions (
          *,
          portfolio_companies (*)
        ),
        nav_history (*)
      `)
      .eq('id', id)
      .single()
      .then(({ data }) => {
        setFund(data)
        setLoading(false)
      })
  }, [id])

  return { fund, loading }
}

export function usePortfolioSummary() {
  const [summary, setSummary] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetch = async () => {
      const { data: fundsData } = await supabase
        .from('funds')
        .select('nav_millions, committed_millions, called_millions, distributed_millions, irr, tvpi, dpi')
        .in('status', ['invested', 'harvesting', 'committed'])

      const f = fundsData ?? []
      const sum = (key: string) => f.reduce((s: number, r: any) => s + (r[key] || 0), 0)
      const avg = (key: string) => {
        const vals = f.filter((r: any) => r[key] != null)
        return vals.length ? vals.reduce((s: number, r: any) => s + r[key], 0) / vals.length : 0
      }

      const { count: dealCount } = await supabase
        .from('deals')
        .select('id', { count: 'exact', head: true })
        .not('status', 'in', '("fully_realized","declined")')

      const { count: signalCount } = await supabase
        .from('signals')
        .select('id', { count: 'exact', head: true })
        .eq('is_read', false)

      setSummary({
        totalNav: sum('nav_millions'),
        totalCommitted: sum('committed_millions'),
        totalCalled: sum('called_millions'),
        totalDistributed: sum('distributed_millions'),
        weightedIrr: avg('irr'),
        weightedTvpi: avg('tvpi'),
        weightedDpi: avg('dpi'),
        fundCount: f.length,
        activeDealCount: dealCount ?? 0,
        unreadSignalCount: signalCount ?? 0,
      })
      setLoading(false)
    }
    fetch()
  }, [])

  return { summary, loading }
}


// ═══════════════════════════════════════════════════════════════
// web/src/hooks/useDeals.ts
// ═══════════════════════════════════════════════════════════════

interface UseDealsOptions {
  status?: string
  dealType?: string
  signal?: string
  ownerId?: string
}

export function useDeals(options: UseDealsOptions = {}) {
  const [deals, setDeals] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  const fetchDeals = useCallback(async () => {
    setLoading(true)
    let query = supabase
      .from('deals')
      .select(`
        *,
        team_members!deals_owner_id_fkey (id, name),
        gp_firms (id, name),
        funds (id, name)
      `)
      .order('conviction_score', { ascending: false })

    if (options.status) query = query.eq('status', options.status)
    if (options.dealType) query = query.eq('deal_type', options.dealType)
    if (options.signal) query = query.eq('signal', options.signal)
    if (options.ownerId) query = query.eq('owner_id', options.ownerId)

    const { data } = await query
    setDeals(data ?? [])
    setLoading(false)
  }, [options.status, options.dealType, options.signal, options.ownerId])

  useEffect(() => { fetchDeals() }, [fetchDeals])

  // Real-time
  useEffect(() => {
    const channel = supabase
      .channel('deals-changes')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'deals' }, () => fetchDeals())
      .subscribe()
    return () => { supabase.removeChannel(channel) }
  }, [fetchDeals])

  const createDeal = async (input: any) => {
    const { data, error } = await supabase.from('deals').insert(input).select().single()
    if (error) throw error
    await fetchDeals()
    return data
  }

  const updateDeal = async (id: string, input: any) => {
    const { data, error } = await supabase.from('deals').update(input).eq('id', id).select().single()
    if (error) throw error
    await fetchDeals()
    return data
  }

  return { deals, loading, refetch: fetchDeals, createDeal, updateDeal }
}

export function useDeal(id: string | null) {
  const [deal, setDeal] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!id) return
    supabase
      .from('deals')
      .select(`
        *,
        team_members!deals_owner_id_fkey (*),
        gp_firms (*),
        funds (*),
        portfolio_companies (*),
        ic_votes (*, team_members (*)),
        deal_activity (*, team_members (*))
      `)
      .eq('id', id)
      .single()
      .then(({ data }) => {
        setDeal(data)
        setLoading(false)
      })
  }, [id])

  return { deal, loading }
}


// ═══════════════════════════════════════════════════════════════
// web/src/hooks/useSignals.ts
// ═══════════════════════════════════════════════════════════════

export function useSignals(unreadOnly = false) {
  const [signals, setSignals] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [unreadCount, setUnreadCount] = useState(0)

  const fetchSignals = useCallback(async () => {
    let query = supabase
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

    if (unreadOnly) query = query.eq('is_read', false)

    const { data } = await query
    setSignals(data ?? [])
    setLoading(false)
  }, [unreadOnly])

  const fetchUnreadCount = useCallback(async () => {
    const { count } = await supabase
      .from('signals')
      .select('id', { count: 'exact', head: true })
      .eq('is_read', false)
    setUnreadCount(count ?? 0)
  }, [])

  useEffect(() => {
    fetchSignals()
    fetchUnreadCount()
  }, [fetchSignals, fetchUnreadCount])

  // Real-time signal updates
  useEffect(() => {
    const channel = supabase
      .channel('signals-realtime')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'signals' }, (payload) => {
        setSignals(prev => [payload.new as any, ...prev])
        setUnreadCount(prev => prev + 1)
      })
      .subscribe()
    return () => { supabase.removeChannel(channel) }
  }, [])

  const markRead = async (id: string) => {
    await supabase.from('signals').update({ is_read: true }).eq('id', id)
    setSignals(prev => prev.map(s => s.id === id ? { ...s, is_read: true } : s))
    setUnreadCount(prev => Math.max(0, prev - 1))
  }

  return { signals, loading, unreadCount, markRead, refetch: fetchSignals }
}


// ═══════════════════════════════════════════════════════════════
// web/src/hooks/useNetwork.ts
// ═══════════════════════════════════════════════════════════════

export function useContacts(search?: string) {
  const [contacts, setContacts] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetch = async () => {
      setLoading(true)
      let query = supabase
        .from('contacts')
        .select(`*, team_members!contacts_relationship_owner_id_fkey (id, name)`)
        .order('network_score', { ascending: false })
        .limit(200)

      if (search) query = query.or(`name.ilike.%${search}%,organization.ilike.%${search}%`)

      const { data } = await query
      setContacts(data ?? [])
      setLoading(false)
    }
    fetch()
  }, [search])

  return { contacts, loading }
}


// ═══════════════════════════════════════════════════════════════
// web/src/hooks/useLps.ts
// ═══════════════════════════════════════════════════════════════

export function useLps(status?: string) {
  const [lps, setLps] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetch = async () => {
      let query = supabase.from('lps').select('*').order('committed_millions', { ascending: false })
      if (status) query = query.eq('status', status)
      const { data } = await query
      setLps(data ?? [])
      setLoading(false)
    }
    fetch()
  }, [status])

  return { lps, loading }
}


// ═══════════════════════════════════════════════════════════════
// web/src/hooks/useAgents.ts
// ═══════════════════════════════════════════════════════════════

export function useAgents() {
  const [agents, setAgents] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    supabase
      .from('agent_configs')
      .select(`
        *,
        agent_runs (id, status, trigger, tokens_used, latency_ms, created_at)
      `)
      .order('name')
      .then(({ data }) => {
        setAgents(data ?? [])
        setLoading(false)
      })
  }, [])

  const triggerRun = async (agentId: string) => {
    const { data } = await supabase
      .from('agent_runs')
      .insert({
        agent_id: agentId,
        status: 'pending',
        trigger: 'manual',
        started_at: new Date().toISOString(),
      })
      .select()
      .single()

    // Call the edge function
    await supabase.functions.invoke('run-agent', {
      body: { runId: data?.id, agentId },
    })

    return data
  }

  return { agents, loading, triggerRun }
}

export function useAgentInsights() {
  const [insights, setInsights] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    supabase
      .from('agent_insights')
      .select(`
        *,
        agent_configs (id, name, agent_type)
      `)
      .eq('is_dismissed', false)
      .order('created_at', { ascending: false })
      .limit(50)
      .then(({ data }) => {
        setInsights(data ?? [])
        setLoading(false)
      })
  }, [])

  // Real-time insights
  useEffect(() => {
    const channel = supabase
      .channel('insights-realtime')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'agent_insights' }, (payload) => {
        setInsights(prev => [payload.new as any, ...prev])
      })
      .subscribe()
    return () => { supabase.removeChannel(channel) }
  }, [])

  const dismiss = async (id: string) => {
    await supabase.from('agent_insights').update({ is_dismissed: true }).eq('id', id)
    setInsights(prev => prev.filter(i => i.id !== id))
  }

  return { insights, loading, dismiss }
}


// ═══════════════════════════════════════════════════════════════
// web/src/hooks/useGlobalSearch.ts
// ═══════════════════════════════════════════════════════════════

export function useGlobalSearch() {
  const [results, setResults] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const search = useCallback(async (query: string) => {
    if (query.length < 2) {
      setResults([])
      return
    }
    setLoading(true)
    const { data } = await supabase.rpc('search_all', { query })
    setResults(data ?? [])
    setLoading(false)
  }, [])

  return { results, loading, search }
}


// ═══════════════════════════════════════════════════════════════
// web/src/hooks/useCashFlows.ts
// ═══════════════════════════════════════════════════════════════

export function useCashFlows(fundId?: string) {
  const [flows, setFlows] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetch = async () => {
      let query = supabase
        .from('cash_flows')
        .select(`*, funds (id, name)`)
        .order('flow_date', { ascending: false })
      if (fundId) query = query.eq('fund_id', fundId)
      const { data } = await query
      setFlows(data ?? [])
      setLoading(false)
    }
    fetch()
  }, [fundId])

  return { flows, loading }
}

export function useNavHistory(fundId?: string) {
  const [history, setHistory] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetch = async () => {
      const table = fundId ? 'nav_history' : 'portfolio_nav_history'
      let query = supabase.from(table).select('*').order('report_date', { ascending: true })
      if (fundId) query = query.eq('fund_id', fundId)
      const { data } = await query
      setHistory(data ?? [])
      setLoading(false)
    }
    fetch()
  }, [fundId])

  return { history, loading }
}


// ═══════════════════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════
//  SUPABASE EDGE FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════
// supabase/functions/run-agent/index.ts
// Executes an AI agent run using Claude API
// ═══════════════════════════════════════════════════════════════

/*
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import Anthropic from 'https://esm.sh/@anthropic-ai/sdk'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: corsHeaders })

  try {
    const { runId, agentId } = await req.json()

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    )

    // Get agent config
    const { data: agent } = await supabase
      .from('agent_configs')
      .select('*')
      .eq('id', agentId)
      .single()

    if (!agent) throw new Error('Agent not found')

    // Update run status
    await supabase.from('agent_runs').update({ status: 'running' }).eq('id', runId)

    // Build context based on agent type
    let contextData = {}
    switch (agent.agent_type) {
      case 'sentinel':
        // Fetch recent signals, portfolio changes, market data
        const { data: recentSignals } = await supabase
          .from('signals')
          .select('*')
          .order('created_at', { ascending: false })
          .limit(20)
        const { data: fundUpdates } = await supabase
          .from('funds')
          .select('name, nav_millions, irr, tvpi, status')
          .in('status', ['invested', 'harvesting'])
        contextData = { recentSignals, fundUpdates }
        break

      case 'persona_panel':
        // Fetch deal details for IC simulation
        const { data: activeDeals } = await supabase
          .from('deals')
          .select('*, ic_votes(*)')
          .in('status', ['diligence', 'ic_review'])
        contextData = { activeDeals }
        break

      case 'living_thesis':
        // Fetch all investment theses and recent market data
        const { data: theses } = await supabase
          .from('deals')
          .select('name, thesis, catalysts, risks, conviction_score')
          .not('status', 'in', '("declined","fully_realized")')
        contextData = { theses }
        break

      case 'capital_optimizer':
        // Fetch full portfolio for optimization
        const { data: portfolio } = await supabase
          .from('funds')
          .select('*, gp_firms(name, strategy)')
          .in('status', ['invested', 'harvesting', 'committed'])
        const { data: pacingModels } = await supabase
          .from('pacing_models')
          .select('*')
          .eq('is_active', true)
        contextData = { portfolio, pacingModels }
        break

      case 'network_mapper':
        // Fetch network graph data
        const { data: networkContacts } = await supabase
          .from('contacts')
          .select('id, name, tier, network_score, relationship_strength, last_contact_date')
          .order('network_score', { ascending: false })
          .limit(100)
        contextData = { networkContacts }
        break

      default:
        break
    }

    // Call Claude API
    const anthropic = new Anthropic({ apiKey: Deno.env.get('ANTHROPIC_API_KEY')! })

    const startTime = Date.now()
    const response = await anthropic.messages.create({
      model: agent.model || 'claude-sonnet-4-5-20250929',
      max_tokens: agent.max_tokens || 4096,
      temperature: agent.temperature || 0.7,
      system: agent.system_prompt || `You are ${agent.name}, an AI agent for the NEWCO V10 VC platform.`,
      messages: [
        {
          role: 'user',
          content: `Analyze the following data and generate insights:\n\n${JSON.stringify(contextData, null, 2)}\n\nProvide your analysis as a JSON array of insights, each with: title, content, insightType (recommendation|alert|analysis|prediction), confidence (0-100), impactScore (0-100).`,
        },
      ],
    })

    const latencyMs = Date.now() - startTime
    const tokensUsed = response.usage.input_tokens + response.usage.output_tokens
    const outputText = response.content[0].type === 'text' ? response.content[0].text : ''

    // Parse insights from response
    let insights = []
    try {
      const jsonMatch = outputText.match(/\[[\s\S]*\]/)
      if (jsonMatch) insights = JSON.parse(jsonMatch[0])
    } catch {
      // If parsing fails, create a single insight from the full response
      insights = [{
        title: `${agent.name} Analysis`,
        content: outputText,
        insightType: 'analysis',
        confidence: 80,
        impactScore: 60,
      }]
    }

    // Store insights
    for (const insight of insights) {
      await supabase.from('agent_insights').insert({
        agent_id: agentId,
        run_id: runId,
        insight_type: insight.insightType || 'analysis',
        title: insight.title,
        content: insight.content,
        confidence: insight.confidence,
        impact_score: insight.impactScore,
      })
    }

    // Update run as completed
    await supabase.from('agent_runs').update({
      status: 'completed',
      output: { insights: insights.length, raw: outputText.substring(0, 1000) },
      tokens_used: tokensUsed,
      latency_ms: latencyMs,
      completed_at: new Date().toISOString(),
    }).eq('id', runId)

    // Update agent stats
    await supabase.from('agent_configs').update({
      last_run_at: new Date().toISOString(),
      run_count: agent.run_count + 1,
      avg_latency_ms: Math.round(
        ((agent.avg_latency_ms || 0) * agent.run_count + latencyMs) / (agent.run_count + 1)
      ),
    }).eq('id', agentId)

    return new Response(
      JSON.stringify({ success: true, insights: insights.length }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    // Update run as failed
    const { runId } = await req.json().catch(() => ({ runId: null }))
    if (runId) {
      const supabase = createClient(
        Deno.env.get('SUPABASE_URL')!,
        Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
      )
      await supabase.from('agent_runs').update({
        status: 'failed',
        error: error.message,
        completed_at: new Date().toISOString(),
      }).eq('id', runId)
    }

    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
*/


// ═══════════════════════════════════════════════════════════════
// supabase/functions/daily-snapshot/index.ts
// Daily portfolio NAV snapshot + materialized view refresh
// ═══════════════════════════════════════════════════════════════

/*
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async () => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // Snapshot portfolio NAV
  await supabase.rpc('snapshot_portfolio_nav')

  // Refresh materialized views
  await supabase.rpc('refresh_materialized_views')

  // Run scheduled agents
  const { data: scheduledAgents } = await supabase
    .from('agent_configs')
    .select('id')
    .eq('is_active', true)
    .not('schedule', 'is', null)

  for (const agent of scheduledAgents ?? []) {
    const { data: run } = await supabase
      .from('agent_runs')
      .insert({
        agent_id: agent.id,
        status: 'pending',
        trigger: 'scheduled',
        started_at: new Date().toISOString(),
      })
      .select()
      .single()

    if (run) {
      await supabase.functions.invoke('run-agent', {
        body: { runId: run.id, agentId: agent.id },
      })
    }
  }

  return new Response(JSON.stringify({ success: true }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
*/


// ═══════════════════════════════════════════════════════════════
// supabase/functions/process-document/index.ts
// AI-powered document processing (OCR, extraction, summarization)
// ═══════════════════════════════════════════════════════════════

/*
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import Anthropic from 'https://esm.sh/@anthropic-ai/sdk'

serve(async (req) => {
  const { documentId } = await req.json()

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  const { data: doc } = await supabase
    .from('documents')
    .select('*')
    .eq('id', documentId)
    .single()

  if (!doc) return new Response(JSON.stringify({ error: 'Document not found' }), { status: 404 })

  // Download file from Supabase Storage
  const { data: fileData } = await supabase.storage
    .from('documents')
    .download(doc.storage_path)

  if (!fileData) return new Response(JSON.stringify({ error: 'File not found' }), { status: 404 })

  // Convert to base64 for Claude
  const base64 = btoa(String.fromCharCode(...new Uint8Array(await fileData.arrayBuffer())))

  const anthropic = new Anthropic({ apiKey: Deno.env.get('ANTHROPIC_API_KEY')! })

  const systemPrompt = `You are a document analyst for NEWCO, a VC fund-of-funds.
Extract key information from this document and provide:
1. A concise summary (2-3 sentences)
2. Key data points as structured JSON (fund name, NAV, IRR, TVPI, DPI, key terms, dates)
3. Any red flags or notable items

Respond with JSON: { summary: string, extractedData: object, redFlags: string[] }`

  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    system: systemPrompt,
    messages: [{
      role: 'user',
      content: [
        {
          type: 'document',
          source: { type: 'base64', media_type: doc.file_type === 'pdf' ? 'application/pdf' : 'image/png', data: base64 },
        },
        { type: 'text', text: `Analyze this ${doc.category || 'document'} titled "${doc.name}". Extract all key data.` },
      ],
    }],
  })

  const outputText = response.content[0].type === 'text' ? response.content[0].text : ''
  let parsed = { summary: outputText, extractedData: {}, redFlags: [] }
  try {
    const jsonMatch = outputText.match(/\{[\s\S]*\}/)
    if (jsonMatch) parsed = JSON.parse(jsonMatch[0])
  } catch {}

  // Update document with AI analysis
  await supabase.from('documents').update({
    ai_summary: parsed.summary,
    ai_extracted_data: parsed.extractedData,
    ai_processed_at: new Date().toISOString(),
  }).eq('id', documentId)

  return new Response(JSON.stringify({ success: true, ...parsed }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
*/
