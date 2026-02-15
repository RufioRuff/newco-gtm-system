// ════════════════════════════════════════════════════
// APP LAYOUT — Main shell with sidebar navigation
// ════════════════════════════════════════════════════
import React, { useState } from 'react'
import {
  Activity, PieChart, Layers, GitBranch, Target,
  TrendingUp, Shield, Users, Bell, Settings, LogOut,
  Menu, X, Search, ChevronRight
} from 'lucide-react'
import { theme as T, fonts } from 'src/lib/theme'
import { useAuth } from 'src/lib/supabase'
import { Avatar } from 'src/components/ui/CoreUI'

const { sans, mono } = fonts

const NAV_ITEMS = [
  { id: 'overview', label: 'Overview', icon: Activity, group: 'core' },
  { id: 'analytics', label: 'Analytics', icon: PieChart, group: 'core' },
  { id: 'funds', label: 'Portfolio', icon: Layers, group: 'portfolio' },
  { id: 'pipeline', label: 'Pipeline', icon: GitBranch, group: 'portfolio' },
  { id: 'secondaries', label: 'Secondaries', icon: Target, group: 'portfolio' },
  { id: 'investor', label: 'Investor View', icon: TrendingUp, group: 'stakeholder' },
  { id: 'compliance', label: 'Compliance', icon: Shield, group: 'stakeholder' },
  { id: 'network', label: 'Network', icon: Users, group: 'intelligence' },
]

const NAV_GROUPS = {
  core: { label: 'CORE', color: T.accent },
  portfolio: { label: 'PORTFOLIO', color: T.blue },
  stakeholder: { label: 'STAKEHOLDER', color: T.green },
  intelligence: { label: 'INTELLIGENCE', color: T.purple },
}

export default function AppLayout({ children, activeView, onViewChange }) {
  const [collapsed, setCollapsed] = useState(false)
  const [showNotifications, setShowNotifications] = useState(false)
  const { user, signOut } = useAuth()

  const sidebarWidth = collapsed ? 56 : 200

  return (
    <div style={{
      display: 'flex',
      minHeight: '100vh',
      background: T.bg,
      color: T.text,
      fontFamily: sans,
    }}>
      {/* ═══ SIDEBAR ═══ */}
      <aside style={{
        width: sidebarWidth,
        flexShrink: 0,
        background: T.bgCard,
        borderRight: `1px solid ${T.border}`,
        display: 'flex',
        flexDirection: 'column',
        transition: 'width .2s ease',
        overflow: 'hidden',
        position: 'fixed',
        top: 0,
        left: 0,
        bottom: 0,
        zIndex: 50,
      }}>
        {/* Logo */}
        <div style={{
          padding: collapsed ? '16px 12px' : '16px',
          borderBottom: `1px solid ${T.border}`,
          display: 'flex',
          alignItems: 'center',
          gap: 10,
        }}>
          <div style={{
            width: 32, height: 32, borderRadius: 8,
            background: T.gradientAccent,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 14, fontWeight: 900, color: '#fff',
            flexShrink: 0,
          }}>
            ET
          </div>
          {!collapsed && (
            <div>
              <div style={{ fontSize: 13, fontWeight: 800, color: T.accent, lineHeight: 1 }}>NEWCO</div>
              <div style={{ fontSize: 8, color: T.textDim, letterSpacing: 1.5 }}>EVIL TWIN CAPITAL</div>
            </div>
          )}
          <button
            onClick={() => setCollapsed(p => !p)}
            style={{
              marginLeft: 'auto', background: 'transparent', border: 'none',
              cursor: 'pointer', padding: 4, display: 'flex', opacity: 0.5,
            }}
          >
            {collapsed ? <Menu size={14} color={T.textMuted} /> : <X size={14} color={T.textMuted} />}
          </button>
        </div>

        {/* Navigation */}
        <nav style={{ flex: 1, overflowY: 'auto', padding: '8px 6px' }}>
          {Object.entries(NAV_GROUPS).map(([groupId, group]) => {
            const items = NAV_ITEMS.filter(i => i.group === groupId)
            return (
              <div key={groupId} style={{ marginBottom: 12 }}>
                {!collapsed && (
                  <div style={{
                    fontSize: 8, fontWeight: 700, color: group.color,
                    letterSpacing: 1.5, padding: '4px 10px', marginBottom: 2,
                  }}>
                    {group.label}
                  </div>
                )}
                {items.map(item => {
                  const isActive = activeView === item.id
                  const Icon = item.icon
                  return (
                    <button
                      key={item.id}
                      onClick={() => onViewChange(item.id)}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 10,
                        width: '100%',
                        padding: collapsed ? '8px 0' : '7px 10px',
                        justifyContent: collapsed ? 'center' : 'flex-start',
                        background: isActive ? `${group.color}12` : 'transparent',
                        color: isActive ? group.color : T.textMuted,
                        border: isActive ? `1px solid ${group.color}30` : '1px solid transparent',
                        borderRadius: 6,
                        cursor: 'pointer',
                        fontFamily: sans,
                        fontSize: 11,
                        fontWeight: isActive ? 700 : 400,
                        transition: 'all .1s',
                      }}
                      title={collapsed ? item.label : undefined}
                    >
                      <Icon size={15} />
                      {!collapsed && <span>{item.label}</span>}
                      {isActive && !collapsed && (
                        <ChevronRight size={11} style={{ marginLeft: 'auto', opacity: 0.5 }} />
                      )}
                    </button>
                  )
                })}
              </div>
            )
          })}
        </nav>

        {/* Bottom: User + Settings */}
        <div style={{
          padding: collapsed ? '8px 6px' : '12px',
          borderTop: `1px solid ${T.border}`,
        }}>
          {!collapsed && user && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
              <Avatar name={user.email} size={24} />
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 10, fontWeight: 600, color: T.text, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {user.user_metadata?.name || user.email}
                </div>
                <div style={{ fontSize: 8, color: T.textDim }}>GP</div>
              </div>
            </div>
          )}
          <div style={{ display: 'flex', gap: 4, justifyContent: collapsed ? 'center' : 'flex-start' }}>
            <button onClick={() => setShowNotifications(p => !p)} style={{ padding: 6, background: 'transparent', border: 'none', cursor: 'pointer' }}>
              <Bell size={14} color={T.textDim} />
            </button>
            <button style={{ padding: 6, background: 'transparent', border: 'none', cursor: 'pointer' }}>
              <Settings size={14} color={T.textDim} />
            </button>
            <button onClick={signOut} style={{ padding: 6, background: 'transparent', border: 'none', cursor: 'pointer' }}>
              <LogOut size={14} color={T.textDim} />
            </button>
          </div>
        </div>
      </aside>

      {/* ═══ MAIN CONTENT ═══ */}
      <main style={{
        flex: 1,
        marginLeft: sidebarWidth,
        transition: 'margin-left .2s ease',
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
      }}>
        {/* Top bar */}
        <header style={{
          position: 'sticky',
          top: 0,
          zIndex: 40,
          padding: '8px 20px',
          background: T.bgGlass,
          backdropFilter: 'blur(12px)',
          borderBottom: `1px solid ${T.border}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{ fontSize: 14, fontWeight: 800, color: T.text }}>
              {NAV_ITEMS.find(i => i.id === activeView)?.label || 'Dashboard'}
            </span>
            <span style={{ fontSize: 9, color: T.textDim, fontFamily: mono, padding: '1px 6px', background: T.bgAccent, borderRadius: 3 }}>
              LIVE
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <span style={{ fontSize: 9, color: T.textDim, fontFamily: mono }}>
              {new Date().toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}
            </span>
          </div>
        </header>

        {/* Page content */}
        <div style={{ flex: 1, padding: '16px 20px', maxWidth: 1400 }}>
          {children}
        </div>

        {/* Footer */}
        <footer style={{
          padding: '12px 20px',
          borderTop: `1px solid ${T.border}`,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <span style={{ fontSize: 8, color: T.textDim }}>NEWCO Platform v10.0 · Evil Twin Capital</span>
          <span style={{ fontSize: 8, color: T.textDim, fontFamily: mono }}>Powered by Omniscient AI</span>
        </footer>
      </main>
    </div>
  )
}
