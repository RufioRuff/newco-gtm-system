// ════════════════════════════════════════════════════
// ALPHA ENGINE NAVIGATION — ViewMap + Tab System
// 26 sub-views with group/workflow/all lenses
// ════════════════════════════════════════════════════
import React, { useState, useEffect, useRef } from 'react'
import { Search, Star, Layers, ChevronRight, Link } from 'lucide-react'
import { theme as T, fonts } from 'src/lib/theme'

const { sans, mono } = fonts

// All 26 analysis views
export const ALPHA_VIEWS = [
  { id: 'radar', label: 'Opportunity Radar', desc: 'Live deal flow scored by conviction × return.', related: ['sizing', 'icmemo', 'seclab'], urgency: 3 },
  { id: 'sizing', label: 'Position Architect', desc: 'Kelly-optimal position sizing with allocation targets.', related: ['radar', 'affe', 'pacing'], urgency: 2 },
  { id: 'emerging', label: 'Emerging Managers', desc: 'Scout emerging GPs with institutional potential.', related: ['gpcard', 'gphealth', 'radar'], urgency: 1 },
  { id: 'comps', label: 'Comp Intelligence', desc: 'Peer benchmarking across fund families.', related: ['alpha', 'gpcard', 'vintage'], urgency: 1 },
  { id: 'icmemo', label: 'IC Decision Matrix', desc: 'Structured IC analysis. Multi-lens conviction scoring.', related: ['radar', 'sizing', 'quant'], urgency: 2 },
  { id: 'liquidity', label: 'Liquidity & Exit', desc: 'Distribution waterfall and exit timeline tracking.', related: ['sizing', 'pacing', 'seclab'], urgency: 1 },
  { id: 'alpha', label: 'Alpha Attribution', desc: 'Decompose returns by source: manager selection, timing, co-invest.', related: ['comps', 'quant', 'gpcard'], urgency: 1 },
  { id: 'gpcard', label: 'GP Scorecard', desc: 'Institutional-grade GP evaluation. 50+ factors.', related: ['emerging', 'gphealth', 'reup'], urgency: 2 },
  { id: 'quant', label: 'Quant Frameworks', desc: 'Bayesian signals, factor analysis, regime detection.', related: ['alpha', 'icmemo', 'sizing'], urgency: 1 },
  { id: 'network', label: 'Network Score', desc: 'Relationship capital intelligence. 4,205 nodes.', related: ['omniscient', 'agents', 'emerging'], urgency: 1 },
  { id: 'pacing', label: 'Pacing & J-Curve', desc: 'Capital commitment pacing by vintage.', related: ['sizing', 'vintage', 'liquidity'], urgency: 2 },
  { id: 'seclab', label: 'Secondary Lab', desc: '400+ transaction pricing framework.', related: ['radar', 'liquidity', 'comps'], urgency: 2 },
  { id: 'reup', label: 'Re-Up & Ref Calls', desc: 'Systematic re-up evaluation with reference calls.', related: ['gpcard', 'gphealth', 'affe'], urgency: 1 },
  { id: 'affe', label: 'Fee Waterfall', desc: 'Total cost transparency. AFFE calculation.', related: ['sizing', 'reup', 'pacing'], urgency: 1 },
  { id: 'vintage', label: 'Vintage Optimizer', desc: 'Commitment pacing calendar by strategy.', related: ['pacing', 'sizing', 'comps'], urgency: 1 },
  { id: 'gphealth', label: 'GP Health Monitor', desc: 'Real-time GP surveillance. AUM, team, drift.', related: ['gpcard', 'reup', 'emerging'], urgency: 2 },
  { id: 'platform', label: 'Platform Pipeline', desc: 'Distribution pipeline. Mercer-Regis framework.', related: ['suitability', 'channel', 'lifecycle'], urgency: 2 },
  { id: 'suitability', label: 'Client Suitability', desc: 'RIA compliance engine. Model portfolio mapping.', related: ['platform', 'endowment', 'lifecycle'], urgency: 1 },
  { id: 'endowment', label: 'Foundation Lens', desc: 'Foundation/endowment allocation frameworks.', related: ['suitability', 'platform', 'channel'], urgency: 1 },
  { id: 'objections', label: 'Advisor Battlecard', desc: '40+ objection responses for RIA conversations.', related: ['platform', 'channel', 'lifecycle'], urgency: 1 },
  { id: 'lifecycle', label: 'Client Lifecycle', desc: 'Full client journey from prospect to reporting.', related: ['platform', 'suitability', 'channel'], urgency: 1 },
  { id: 'channel', label: 'Channel Economics', desc: 'Revenue modeling by distribution channel.', related: ['platform', 'lifecycle', 'objections'], urgency: 1 },
  { id: 'omniscient', label: '⚡ Omniscient HQ', desc: 'AI-Assisted Investing command center.', related: ['agents', 'infra', 'buildmap'], urgency: 3 },
  { id: 'agents', label: 'Agent Orchestra', desc: '8-agent system: Sentinel, Persona Panel, Living Thesis.', related: ['omniscient', 'infra', 'buildmap'], urgency: 2 },
  { id: 'infra', label: 'Infrastructure', desc: 'Mac Studio M4 Max, RedwoodJS, PostgreSQL + Neo4j.', related: ['omniscient', 'buildmap', 'agents'], urgency: 1 },
  { id: 'buildmap', label: 'Build Roadmap', desc: '3-phase roadmap: Vault → Enrichment → Agents.', related: ['omniscient', 'infra', 'agents'], urgency: 2 },
]

// Department groups
export const TAB_GROUPS = [
  { id: 'invest', label: 'Investment Engine', color: T.accent, icon: '📊', desc: 'Ken Wallace', tabs: ['radar', 'sizing', 'emerging', 'comps', 'icmemo', 'liquidity', 'alpha', 'gpcard', 'quant', 'network'] },
  { id: 'ops', label: 'Institutional Ops', color: T.blue, icon: '⚙️', desc: 'Operations', tabs: ['pacing', 'seclab', 'reup', 'affe', 'vintage', 'gphealth'] },
  { id: 'dist', label: 'Distribution', color: T.green, icon: '🏦', desc: 'Bob Burlinson', tabs: ['platform', 'suitability', 'endowment', 'objections', 'lifecycle', 'channel'] },
  { id: 'ai', label: 'Omniscient AI', color: T.purple, icon: '⚡', desc: 'Intelligence', tabs: ['omniscient', 'agents', 'infra', 'buildmap'] },
]

// Cross-cutting workflow lenses
export const WORKFLOWS = [
  { id: 'decisions', label: 'Decisions & IC', icon: '⚖️', color: T.red, tabs: ['radar', 'icmemo', 'sizing', 'quant', 'seclab'], summary: 'Open decisions, conviction scoring, position sizing' },
  { id: 'gp-intel', label: 'GP Intelligence', icon: '🔍', color: T.accent, tabs: ['emerging', 'gpcard', 'gphealth', 'reup', 'alpha'], summary: 'Scout, evaluate, monitor, and attribute returns' },
  { id: 'cashflows', label: 'Cashflows & Pacing', icon: '💰', color: T.green, tabs: ['pacing', 'affe', 'vintage', 'liquidity', 'sizing'], summary: 'Capital commitments, J-curves, fees, vintage' },
  { id: 'risk-scenario', label: 'Risk & Scenarios', icon: '⚡', color: T.amber, tabs: ['quant', 'gphealth', 'liquidity', 'comps', 'alpha'], summary: 'Quantitative risk, exit catalysts, benchmarks' },
  { id: 'distribution', label: 'Distribution & LPs', icon: '🏦', color: T.blue, tabs: ['platform', 'suitability', 'objections', 'lifecycle', 'channel', 'endowment'], summary: 'Platform pipeline and LP management' },
  { id: 'ai-system', label: 'AI & Intelligence', icon: '🤖', color: T.purple, tabs: ['omniscient', 'agents', 'infra', 'buildmap', 'network'], summary: 'Technology platform powering everything' },
]

// KPIs per group
const GROUP_KPIS = {
  invest: [{ l: 'Live Opps', v: '6', c: T.accent }, { l: 'Strong Buy', v: '3', c: T.green }, { l: 'Pipeline', v: '$22.5B', c: T.blue }, { l: 'Avg IRR', v: '28.3%', c: T.accent }],
  ops: [{ l: 'Funds Tracked', v: '8', c: T.blue }, { l: 'Wtd TVPI', v: '1.42x', c: T.green }, { l: 'Fee Drag', v: '1.8%', c: T.amber }, { l: 'Vintage', v: '22-24', c: T.purple }],
  dist: [{ l: 'Platforms', v: '5', c: T.green }, { l: 'Pipeline', v: '$48M', c: T.accent }, { l: 'Advisors', v: '5K+', c: T.blue }, { l: 'Conv', v: '12%', c: T.purple }],
  ai: [{ l: 'Value/mo', v: '$22.3K', c: T.accent }, { l: 'Hours', v: '680+/yr', c: T.green }, { l: 'Agents', v: '4/8', c: T.purple }, { l: 'Phase', v: '1/3', c: T.blue }],
}

export default function AlphaNav({ activeView, onViewChange }) {
  const [navExpanded, setNavExpanded] = useState(false)
  const [navLens, setNavLens] = useState('groups')
  const [cmdOpen, setCmdOpen] = useState(false)
  const [cmdQ, setCmdQ] = useState('')
  const [cmdIdx, setCmdIdx] = useState(0)
  const [favTabs, setFavTabs] = useState(['radar', 'omniscient', 'gpcard', 'platform'])
  const cmdRef = useRef(null)
  const tabScrollRef = useRef(null)

  const activeGroup = TAB_GROUPS.find(g => g.tabs.includes(activeView))
  const [selectedGroupId, setSelectedGroupId] = useState(activeGroup?.id || 'invest')
  const selectedGroup = TAB_GROUPS.find(g => g.id === selectedGroupId)
  const activeViewObj = ALPHA_VIEWS.find(v => v.id === activeView)
  const isFav = favTabs.includes(activeView)

  const allTabIds = ALPHA_VIEWS.map(v => v.id)
  const curIdx = allTabIds.indexOf(activeView)
  const prevTab = curIdx > 0 ? ALPHA_VIEWS[curIdx - 1] : null
  const nextTab = curIdx < ALPHA_VIEWS.length - 1 ? ALPHA_VIEWS[curIdx + 1] : null

  useEffect(() => { if (activeGroup) setSelectedGroupId(activeGroup.id) }, [activeView])

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); setCmdOpen(p => !p); setCmdQ(''); setCmdIdx(0) }
      if (e.key === 'Escape') setCmdOpen(false)
      if (!cmdOpen && !['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)) {
        const tabs = activeGroup?.tabs || allTabIds
        const i = tabs.indexOf(activeView)
        if (e.key === 'ArrowRight' && i < tabs.length - 1) { e.preventDefault(); onViewChange(tabs[i + 1]) }
        if (e.key === 'ArrowLeft' && i > 0) { e.preventDefault(); onViewChange(tabs[i - 1]) }
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [cmdOpen, activeView, activeGroup])

  useEffect(() => { if (cmdOpen && cmdRef.current) cmdRef.current.focus() }, [cmdOpen])

  // Auto-scroll active tab
  useEffect(() => {
    if (tabScrollRef.current) {
      const btn = tabScrollRef.current.querySelector('[data-active="true"]')
      if (btn) btn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' })
    }
  }, [activeView])

  const toggleFav = (id) => setFavTabs(prev => prev.includes(id) ? prev.filter(f => f !== id) : [...prev, id].slice(0, 8))
  const cmdFiltered = cmdQ ? ALPHA_VIEWS.filter(v => v.label.toLowerCase().includes(cmdQ.toLowerCase())) : ALPHA_VIEWS

  return (
    <div style={{ marginBottom: 2 }}>
      {/* Command Palette */}
      {cmdOpen && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: '#000000a0', zIndex: 999, display: 'flex', justifyContent: 'center', paddingTop: 100, backdropFilter: 'blur(4px)' }} onClick={() => setCmdOpen(false)}>
          <div onClick={e => e.stopPropagation()} style={{ width: 520, maxHeight: 460, background: T.bgCard, borderRadius: 14, border: `1px solid ${T.accent}30`, boxShadow: `0 24px 80px #000c`, overflow: 'hidden' }}>
            <div style={{ padding: '14px 18px', borderBottom: `1px solid ${T.border}`, display: 'flex', alignItems: 'center', gap: 10 }}>
              <Search size={18} color={T.accent} />
              <input ref={cmdRef} value={cmdQ} onChange={e => { setCmdQ(e.target.value); setCmdIdx(0) }}
                onKeyDown={e => {
                  if (e.key === 'Enter' && cmdFiltered.length > 0) { onViewChange(cmdFiltered[Math.min(cmdIdx, cmdFiltered.length - 1)].id); setCmdOpen(false) }
                  if (e.key === 'ArrowDown') { e.preventDefault(); setCmdIdx(i => Math.min(i + 1, cmdFiltered.length - 1)) }
                  if (e.key === 'ArrowUp') { e.preventDefault(); setCmdIdx(i => Math.max(i - 1, 0)) }
                }}
                placeholder="Jump to any view…"
                style={{ flex: 1, background: 'transparent', border: 'none', color: T.text, fontSize: 15, fontFamily: sans, outline: 'none', fontWeight: 500 }}
              />
              <span style={{ fontSize: 10, color: T.textDim, padding: '3px 8px', background: T.bgAccent, borderRadius: 4, fontFamily: mono }}>ESC</span>
            </div>
            <div style={{ maxHeight: 380, overflowY: 'auto', padding: 8 }}>
              {TAB_GROUPS.map(g => {
                const gTabs = cmdFiltered.filter(v => g.tabs.includes(v.id))
                if (!gTabs.length) return null
                return (
                  <div key={g.id} style={{ marginBottom: 8 }}>
                    <div style={{ fontSize: 9, fontWeight: 700, color: g.color, textTransform: 'uppercase', padding: '6px 10px', letterSpacing: 1.2 }}>
                      {g.icon} {g.label}
                    </div>
                    {gTabs.map(v => {
                      const isActive = activeView === v.id
                      return (
                        <button key={v.id} onClick={() => { onViewChange(v.id); setCmdOpen(false) }}
                          style={{ display: 'flex', alignItems: 'center', gap: 10, width: '100%', padding: '9px 14px', background: isActive ? T.accentBg : 'transparent', color: isActive ? T.accent : T.text, border: '1px solid transparent', borderRadius: 8, cursor: 'pointer', fontFamily: sans, fontSize: 13, textAlign: 'left' }}>
                          <span style={{ width: 7, height: 7, borderRadius: 4, background: g.color, opacity: 0.5 }} />
                          <span style={{ fontWeight: isActive ? 600 : 400 }}>{v.label}</span>
                          {isActive && <span style={{ marginLeft: 'auto', fontSize: 9, color: T.accent, fontStyle: 'italic' }}>current</span>}
                        </button>
                      )
                    })}
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      )}

      {/* Top bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: navExpanded ? 0 : 6 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <div style={{ display: 'flex', background: T.bgAccent, borderRadius: 8, padding: 2, border: `1px solid ${T.border}`, gap: 1 }}>
            {TAB_GROUPS.map(g => {
              const isActive = selectedGroupId === g.id
              return (
                <button key={g.id} onClick={() => { setSelectedGroupId(g.id); if (!g.tabs.includes(activeView)) onViewChange(g.tabs[0]); if (navExpanded) setNavExpanded(false) }}
                  style={{ display: 'flex', alignItems: 'center', gap: 4, padding: '5px 11px', background: isActive ? T.bgCard : 'transparent', color: isActive ? g.color : T.textMuted, border: isActive ? `1px solid ${g.color}30` : '1px solid transparent', borderRadius: 6, cursor: 'pointer', fontFamily: sans, fontSize: 10, fontWeight: isActive ? 700 : 500, transition: 'all .12s', position: 'relative' }}>
                  <span style={{ fontSize: 12 }}>{g.icon}</span>
                  <span>{g.label}</span>
                  <span style={{ fontSize: 8, color: isActive ? g.color : T.textDim, fontFamily: mono }}>({g.tabs.length})</span>
                </button>
              )
            })}
          </div>
          {!navExpanded && favTabs.length > 0 && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Star size={9} color={T.gold} style={{ opacity: 0.4 }} />
              {favTabs.slice(0, 4).map(fid => {
                const fv = ALPHA_VIEWS.find(v => v.id === fid)
                return fv ? (
                  <button key={fid} onClick={() => onViewChange(fid)}
                    style={{ padding: '2px 8px', fontSize: 9, fontWeight: activeView === fid ? 700 : 400, background: activeView === fid ? `${T.accent}12` : 'transparent', color: activeView === fid ? T.accent : T.textDim, border: 'none', borderRadius: 3, cursor: 'pointer', fontFamily: sans }}>
                    {fv.label.replace('⚡ ', '').split(' ')[0]}
                  </button>
                ) : null
              })}
            </div>
          )}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          <button onClick={() => setNavExpanded(p => !p)}
            style={{ display: 'flex', alignItems: 'center', gap: 5, padding: '5px 12px', background: navExpanded ? `${T.accent}12` : T.bgAccent, border: `1px solid ${navExpanded ? T.accent + '40' : T.border}`, borderRadius: 6, color: navExpanded ? T.accent : T.textMuted, fontSize: 10, cursor: 'pointer', fontFamily: sans, fontWeight: navExpanded ? 700 : 500 }}>
            <Layers size={12} />{navExpanded ? 'Close Map' : 'View Map'}<span style={{ fontSize: 8, color: T.textDim, fontFamily: mono, padding: '1px 4px', background: T.bg, borderRadius: 2 }}>26</span>
          </button>
          <button onClick={() => { setCmdOpen(true); setCmdQ(''); setCmdIdx(0) }}
            style={{ display: 'flex', alignItems: 'center', gap: 5, padding: '5px 12px', background: T.bgAccent, border: `1px solid ${T.border}`, borderRadius: 6, color: T.textMuted, fontSize: 10, cursor: 'pointer', fontFamily: sans }}>
            <Search size={12} />Jump<span style={{ fontSize: 8, fontFamily: mono, padding: '1px 5px', background: T.bg, borderRadius: 2 }}>⌘K</span>
          </button>
        </div>
      </div>

      {/* Expanded ViewMap */}
      {navExpanded && (
        <div style={{ background: T.bgAccent, borderRadius: 10, border: `1px solid ${T.border}`, padding: 12, marginBottom: 8 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
            <div style={{ display: 'flex', background: T.bg, borderRadius: 5, padding: 2, border: `1px solid ${T.border}`, gap: 1 }}>
              {['groups', 'workflows', 'all'].map(lens => (
                <button key={lens} onClick={() => setNavLens(lens)}
                  style={{ padding: '4px 12px', fontSize: 9, fontWeight: navLens === lens ? 700 : 400, background: navLens === lens ? T.bgCard : 'transparent', color: navLens === lens ? T.accent : T.textDim, border: navLens === lens ? `1px solid ${T.accent}30` : '1px solid transparent', borderRadius: 4, cursor: 'pointer', fontFamily: sans }}>
                  {lens === 'groups' ? 'By Department' : lens === 'workflows' ? 'By Workflow' : 'All Views'}
                </button>
              ))}
            </div>
          </div>

          {navLens === 'groups' && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8 }}>
              {TAB_GROUPS.map(g => (
                <div key={g.id}>
                  <div style={{ fontSize: 9, fontWeight: 700, color: g.color, marginBottom: 6, display: 'flex', alignItems: 'center', gap: 4 }}>
                    {g.icon} {g.label}
                  </div>
                  {g.tabs.map(tid => {
                    const tv = ALPHA_VIEWS.find(v => v.id === tid)
                    if (!tv) return null
                    const isActive = activeView === tid
                    return (
                      <button key={tid} onClick={() => { onViewChange(tid); setNavExpanded(false) }}
                        style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '5px 8px', width: '100%', marginBottom: 2, background: isActive ? `${g.color}12` : T.bgCard, border: `1px solid ${isActive ? g.color + '40' : T.border + '60'}`, borderRadius: 5, cursor: 'pointer', fontFamily: sans, textAlign: 'left', borderLeft: `3px solid ${isActive ? g.color : 'transparent'}` }}>
                        <div style={{ flex: 1 }}>
                          <div style={{ fontSize: 10, fontWeight: isActive ? 700 : 500, color: isActive ? g.color : T.text }}>{tv.label.replace('⚡ ', '')}</div>
                          <div style={{ fontSize: 7, color: T.textDim }}>{tv.desc?.slice(0, 50)}</div>
                        </div>
                        {tv.urgency >= 3 && <span style={{ width: 6, height: 6, borderRadius: 3, background: T.red }} />}
                      </button>
                    )
                  })}
                </div>
              ))}
            </div>
          )}

          {navLens === 'workflows' && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8 }}>
              {WORKFLOWS.map(wf => (
                <div key={wf.id} style={{ background: T.bgCard, borderRadius: 8, border: `1px solid ${T.border}`, overflow: 'hidden' }}>
                  <div style={{ padding: '8px 10px', borderBottom: `1px solid ${T.border}60`, background: `${wf.color}06` }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
                      <span style={{ fontSize: 13 }}>{wf.icon}</span>
                      <span style={{ fontSize: 11, fontWeight: 700, color: wf.color }}>{wf.label}</span>
                    </div>
                    <div style={{ fontSize: 8, color: T.textMuted }}>{wf.summary}</div>
                  </div>
                  <div style={{ padding: '4px 6px' }}>
                    {wf.tabs.map(tid => {
                      const tv = ALPHA_VIEWS.find(v => v.id === tid)
                      if (!tv) return null
                      return (
                        <button key={tid} onClick={() => { onViewChange(tid); setNavExpanded(false) }}
                          style={{ display: 'flex', alignItems: 'center', gap: 5, width: '100%', padding: '4px 6px', background: activeView === tid ? `${wf.color}10` : 'transparent', border: 'none', borderRadius: 4, cursor: 'pointer', fontFamily: sans, textAlign: 'left', borderLeft: `2px solid ${activeView === tid ? wf.color : 'transparent'}` }}>
                          <span style={{ fontSize: 10, fontWeight: activeView === tid ? 700 : 400, color: activeView === tid ? wf.color : T.text }}>{tv.label.replace('⚡ ', '')}</span>
                        </button>
                      )
                    })}
                  </div>
                </div>
              ))}
            </div>
          )}

          {navLens === 'all' && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 3 }}>
              {[...ALPHA_VIEWS].sort((a, b) => a.label.localeCompare(b.label)).map(v => {
                const vg = TAB_GROUPS.find(g => g.tabs.includes(v.id))
                const isActive = activeView === v.id
                return (
                  <button key={v.id} onClick={() => { onViewChange(v.id); setNavExpanded(false) }}
                    style={{ display: 'flex', alignItems: 'center', gap: 5, padding: '5px 8px', background: isActive ? `${(vg?.color || T.accent)}10` : T.bgCard, border: `1px solid ${isActive ? (vg?.color || T.accent) + '40' : T.border + '40'}`, borderRadius: 4, cursor: 'pointer', fontFamily: sans, textAlign: 'left' }}>
                    <span style={{ width: 5, height: 5, borderRadius: 3, background: vg?.color || T.accent, opacity: isActive ? 1 : 0.4 }} />
                    <span style={{ fontSize: 10, fontWeight: isActive ? 700 : 400, color: isActive ? (vg?.color || T.accent) : T.text }}>{v.label.replace('⚡ ', '')}</span>
                  </button>
                )
              })}
            </div>
          )}
        </div>
      )}

      {/* Compact strip */}
      {!navExpanded && (
        <>
          <div style={{ display: 'flex', alignItems: 'center', gap: 3, marginBottom: 6 }}>
            <button disabled={!prevTab} onClick={() => prevTab && onViewChange(prevTab.id)} style={{ padding: '4px 3px', background: 'transparent', border: 'none', cursor: prevTab ? 'pointer' : 'default', opacity: prevTab ? 0.5 : 0.12 }}>
              <ChevronRight size={13} color={T.textMuted} style={{ transform: 'rotate(180deg)' }} />
            </button>
            <div ref={tabScrollRef} style={{ display: 'flex', gap: 1, overflow: 'hidden', flex: 1, maskImage: 'linear-gradient(90deg, transparent 0%, black 1.5%, black 98.5%, transparent 100%)' }}>
              {selectedGroup?.tabs.map(tid => {
                const tab = ALPHA_VIEWS.find(v => v.id === tid)
                const isActive = activeView === tid
                return (
                  <button key={tid} data-active={isActive ? 'true' : 'false'} onClick={() => onViewChange(tid)}
                    style={{ padding: '4px 12px', fontSize: 10, fontWeight: isActive ? 700 : 400, background: isActive ? `${selectedGroup.color}15` : 'transparent', color: isActive ? selectedGroup.color : T.textMuted, border: isActive ? `1px solid ${selectedGroup.color}40` : '1px solid transparent', borderRadius: 4, cursor: 'pointer', fontFamily: sans, whiteSpace: 'nowrap', flexShrink: 0, borderBottom: isActive ? `2px solid ${selectedGroup.color}` : '2px solid transparent' }}>
                    {tab?.label}
                  </button>
                )
              })}
            </div>
            <button disabled={!nextTab} onClick={() => nextTab && onViewChange(nextTab.id)} style={{ padding: '4px 3px', background: 'transparent', border: 'none', cursor: nextTab ? 'pointer' : 'default', opacity: nextTab ? 0.5 : 0.12 }}>
              <ChevronRight size={13} color={T.textMuted} />
            </button>
            <span style={{ fontSize: 8, color: T.textDim, fontFamily: mono, padding: '2px 5px', background: T.bgAccent, borderRadius: 3 }}>{curIdx + 1}/{ALPHA_VIEWS.length}</span>
          </div>

          {/* KPI bar */}
          <div style={{ padding: '5px 10px', background: T.bgAccent, borderRadius: 5, border: `1px solid ${T.border}`, marginBottom: 4 }}>
            <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
              <span style={{ fontSize: 8, fontWeight: 700, color: selectedGroup?.color || T.accent, textTransform: 'uppercase', letterSpacing: 0.6 }}>{selectedGroup?.icon} {selectedGroup?.desc}</span>
              <div style={{ width: 1, height: 14, background: T.border }} />
              {(GROUP_KPIS[selectedGroupId] || []).map((kpi, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 3, padding: '0 6px', borderRight: i < 3 ? `1px solid ${T.border}` : 'none' }}>
                  <span style={{ fontSize: 8, color: T.textDim }}>{kpi.l}</span>
                  <span style={{ fontSize: 11, fontWeight: 700, fontFamily: mono, color: kpi.c }}>{kpi.v}</span>
                </div>
              ))}
              <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 5 }}>
                {activeViewObj?.urgency >= 3 && <span style={{ fontSize: 7, padding: '1px 4px', background: T.redBg, color: T.red, borderRadius: 2, fontWeight: 700 }}>URGENT</span>}
                <span style={{ fontSize: 10, fontWeight: 700, color: T.text }}>{activeViewObj?.label}</span>
                <button onClick={() => toggleFav(activeView)} style={{ background: 'transparent', border: 'none', cursor: 'pointer', padding: 2, display: 'flex' }}>
                  <Star size={12} color={isFav ? T.gold : T.textDim} fill={isFav ? T.gold : 'none'} />
                </button>
              </div>
            </div>
            {activeViewObj?.desc && <div style={{ fontSize: 9, color: T.textMuted, lineHeight: 1.2, marginTop: 2 }}>{activeViewObj.desc}</div>}
          </div>

          {/* Progress dots */}
          {selectedGroup && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 2, marginBottom: 8, paddingLeft: 2 }}>
              {selectedGroup.tabs.map((tid, i) => {
                const isActive = activeView === tid
                const isPast = selectedGroup.tabs.indexOf(activeView) > i
                return (
                  <button key={tid} onClick={() => onViewChange(tid)} title={ALPHA_VIEWS.find(v => v.id === tid)?.label}
                    style={{ width: isActive ? 20 : 6, height: 5, borderRadius: 3, background: isActive ? selectedGroup.color : (isPast ? `${selectedGroup.color}50` : T.border), border: 'none', cursor: 'pointer', transition: 'all .2s', padding: 0 }} />
                )
              })}
            </div>
          )}
        </>
      )}

      {/* Related views footer */}
      {activeViewObj?.related?.length > 0 && (
        <div style={{ marginTop: 12, padding: '8px 12px', background: T.bgAccent, borderRadius: 6, border: `1px solid ${T.border}` }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6 }}>
            <Link size={10} color={T.textDim} />
            <span style={{ fontSize: 8, fontWeight: 700, color: T.textDim, textTransform: 'uppercase', letterSpacing: 1 }}>Related</span>
          </div>
          <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
            {activeViewObj.related.map(rid => {
              const rv = ALPHA_VIEWS.find(v => v.id === rid)
              const rg = TAB_GROUPS.find(g => g.tabs.includes(rid))
              if (!rv || !rg) return null
              return (
                <button key={rid} onClick={() => onViewChange(rid)}
                  style={{ display: 'flex', alignItems: 'center', gap: 5, padding: '4px 10px', background: T.bgCard, border: `1px solid ${T.border}`, borderRadius: 4, cursor: 'pointer', fontFamily: sans, fontSize: 10, color: T.text }}>
                  <span style={{ width: 5, height: 5, borderRadius: 3, background: rg.color }} />
                  {rv.label.replace('⚡ ', '')}
                </button>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
