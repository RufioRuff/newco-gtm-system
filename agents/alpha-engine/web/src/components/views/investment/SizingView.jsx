import React, { useState } from 'react'
import { Card, Stat, Badge, TH, TD, ProgressBar } from 'src/components/ui/CoreUI'
import { theme as T, fonts } from 'src/lib/theme'
const { sans, mono } = fonts

const POSITIONS = [
  { id: 1, fund: 'Apex III', allocation: 18, kelly: 22, current: '$2.7M', target: '$3.3M', gap: '+$600K', risk: 'low' },
  { id: 2, fund: 'Harbor Secondary', allocation: 12, kelly: 15, current: '$1.8M', target: '$2.25M', gap: '+$450K', risk: 'medium' },
  { id: 3, fund: 'Meridian V', allocation: 15, kelly: 14, current: '$2.25M', target: '$2.1M', gap: '-$150K', risk: 'low' },
  { id: 4, fund: 'Vanguard Co-Inv', allocation: 8, kelly: 12, current: '$1.2M', target: '$1.8M', gap: '+$600K', risk: 'high' },
  { id: 5, fund: 'Tidal Growth', allocation: 10, kelly: 8, current: '$1.5M', target: '$1.2M', gap: '-$300K', risk: 'medium' },
]

export default function SizingView() {
  return (
    <div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 10, marginBottom: 16 }}>
        <Stat label="Total Allocated" value="$15M" sub="63% of fund" color={T.accent} />
        <Stat label="Kelly Optimal" value="$16.2M" sub="68% recommended" color={T.green} />
        <Stat label="Rebalance Gap" value="$1.2M" sub="Under-allocated" color={T.amber} />
        <Stat label="Positions" value="5" sub="Active allocations" color={T.blue} />
      </div>
      <Card title="Position Sizing Matrix" subtitle="Kelly-optimal vs current allocation">
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead><tr><TH>Fund</TH><TH align="center">Current %</TH><TH align="center">Kelly %</TH><TH align="center">Current $</TH><TH align="center">Target $</TH><TH align="center">Gap</TH><TH align="center">Risk</TH></tr></thead>
          <tbody>
            {POSITIONS.map(p => (
              <tr key={p.id} style={{ borderBottom: `1px solid ${T.border}` }}>
                <TD bold>{p.fund}</TD>
                <TD align="center" mono>{p.allocation}%</TD>
                <TD align="center" mono color={T.green}>{p.kelly}%</TD>
                <TD align="center" mono>{p.current}</TD>
                <TD align="center" mono color={T.accent}>{p.target}</TD>
                <TD align="center" mono color={p.gap.startsWith('+') ? T.green : T.red}>{p.gap}</TD>
                <TD align="center"><Badge color={p.risk === 'high' ? T.red : p.risk === 'medium' ? T.amber : T.green} size="xs">{p.risk}</Badge></TD>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  )
}
