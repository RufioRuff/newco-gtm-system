import React, { useState, useRef } from 'react'
import { Card, Stat, Badge, TH, TD, ProgressBar, Pill } from 'src/components/ui/CoreUI'
import { useRadarChart, useSparkline } from 'src/hooks/useD3Charts'
import { theme as T, fonts, dealStatusColors } from 'src/lib/theme'
const { sans, mono } = fonts

const MOCK_DEALS = [
  { id: 1, name: 'Apex Ventures III', gp: 'Apex Capital', strategy: 'VENTURE', vintage: 2024, tvpi: '2.8x', irr: '38%', disc: '14%', conviction: 92, status: 'IC_REVIEW', urgency: 'high', sparkline: [20,35,30,45,55,60,78,85,92] },
  { id: 2, name: 'Harbor Secondary Fund', gp: 'Harbor Partners', strategy: 'SECONDARY', vintage: 2023, tvpi: '1.6x', irr: '22%', disc: '28%', conviction: 85, status: 'DUE_DILIGENCE', urgency: 'medium', sparkline: [40,42,50,48,55,62,70,78,85] },
  { id: 3, name: 'Tidal Growth II', gp: 'Tidal Capital', strategy: 'GROWTH', vintage: 2024, tvpi: '1.4x', irr: '18%', disc: '8%', conviction: 78, status: 'SCREENING', urgency: 'low', sparkline: [30,35,40,38,45,50,55,68,78] },
  { id: 4, name: 'Meridian Buyout V', gp: 'Meridian PE', strategy: 'BUYOUT', vintage: 2023, tvpi: '1.9x', irr: '24%', disc: '18%', conviction: 88, status: 'NEGOTIATION', urgency: 'high', sparkline: [50,55,48,60,65,72,80,84,88] },
  { id: 5, name: 'Vanguard Co-Invest A', gp: 'Vanguard GP', strategy: 'CO_INVEST', vintage: 2024, tvpi: '3.1x', irr: '45%', disc: '5%', conviction: 95, status: 'IC_REVIEW', urgency: 'high', sparkline: [60,65,70,75,82,85,88,92,95] },
  { id: 6, name: 'Nova Real Assets II', gp: 'Nova Capital', strategy: 'REAL_ASSETS', vintage: 2024, tvpi: '1.2x', irr: '12%', disc: '22%', conviction: 65, status: 'INITIAL_REVIEW', urgency: 'low', sparkline: [35,38,40,42,45,50,55,58,65] },
]

function MiniRadar({ data, size = 60, color }) {
  const ref = useRef()
  useRadarChart(ref, { data, axes: ['Ret', 'Team', 'Proc', 'Terms', 'Fit'], size, color })
  return <svg ref={ref} width={size} height={size} />
}

function MiniSpark({ data, width = 70, height = 20, color }) {
  const ref = useRef()
  useSparkline(ref, { data, width, height, color })
  return <svg ref={ref} width={width} height={height} />
}

export default function RadarView() {
  const [filter, setFilter] = useState('all')
  const [sortBy, setSortBy] = useState('conviction')
  const filters = ['all', 'IC_REVIEW', 'DUE_DILIGENCE', 'NEGOTIATION', 'SCREENING']

  const filtered = MOCK_DEALS
    .filter(d => filter === 'all' || d.status === filter)
    .sort((a, b) => b.conviction - a.conviction)

  return (
    <div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 10, marginBottom: 16 }}>
        <Stat label="Live Opportunities" value="6" sub="3 high conviction" color={T.accent} trend={12} />
        <Stat label="Strong Buy" value="3" sub="IC review pending" color={T.green} />
        <Stat label="Pipeline NAV" value="$22.5B" sub="Across 6 opportunities" color={T.blue} />
        <Stat label="Avg Conviction" value="84" sub="Composite score" color={T.purple} />
        <Stat label="Avg Discount" value="16%" sub="To NAV" color={T.amber} />
      </div>

      <Card title="Deal Flow Pipeline" subtitle={`${filtered.length} active opportunities`}
        headerRight={
          <div style={{ display: 'flex', gap: 3 }}>
            {filters.map(f => <Pill key={f} label={f === 'all' ? 'All' : f.replace(/_/g, ' ')} active={filter === f} onClick={() => setFilter(f)} />)}
          </div>
        }>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <TH>Fund / GP</TH>
              <TH align="center">Strategy</TH>
              <TH align="center">TVPI</TH>
              <TH align="center">IRR</TH>
              <TH align="center">Disc</TH>
              <TH align="center">Conviction</TH>
              <TH align="center">Trend</TH>
              <TH align="center">Status</TH>
              <TH align="center">Radar</TH>
            </tr>
          </thead>
          <tbody>
            {filtered.map(d => (
              <tr key={d.id} style={{ borderBottom: `1px solid ${T.border}`, cursor: 'pointer' }}
                onMouseEnter={e => e.currentTarget.style.background = T.bgHover}
                onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
                <TD>
                  <div style={{ fontWeight: 700, fontSize: 11 }}>{d.name}</div>
                  <div style={{ fontSize: 9, color: T.textDim }}>{d.gp} · {d.vintage}</div>
                </TD>
                <TD align="center"><Badge color={T.blue} size="xs">{d.strategy}</Badge></TD>
                <TD align="center" mono bold color={T.green}>{d.tvpi}</TD>
                <TD align="center" mono bold color={T.accent}>{d.irr}</TD>
                <TD align="center" mono color={T.amber}>{d.disc}</TD>
                <TD align="center">
                  <div style={{ display: 'flex', alignItems: 'center', gap: 4, justifyContent: 'center' }}>
                    <span style={{ fontFamily: mono, fontWeight: 800, fontSize: 14, color: d.conviction >= 90 ? T.green : d.conviction >= 80 ? T.accent : T.amber }}>{d.conviction}</span>
                    <ProgressBar value={d.conviction} color={d.conviction >= 90 ? T.green : d.conviction >= 80 ? T.accent : T.amber} height={4} />
                  </div>
                </TD>
                <TD align="center"><MiniSpark data={d.sparkline} color={d.conviction >= 85 ? T.green : T.accent} /></TD>
                <TD align="center"><Badge color={dealStatusColors[d.status]} size="xs">{d.status.replace(/_/g, ' ')}</Badge></TD>
                <TD align="center"><MiniRadar data={[d.conviction, d.conviction - 5, d.conviction - 10, d.conviction + 2, d.conviction - 3]} color={T.accent} /></TD>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  )
}
