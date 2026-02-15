// ════════════════════════════════════════════════════
// CORE UI COMPONENTS — Shared across all views
// ════════════════════════════════════════════════════
import React from 'react'
import { theme as T, fonts } from 'src/lib/theme'

const { sans, mono } = fonts

// ═══ STAT CARD ═══
export function Stat({ label, value, icon: Icon, sub, color, trend, onClick }) {
  return (
    <div
      onClick={onClick}
      style={{
        background: T.bgCard,
        borderRadius: 10,
        padding: '12px 14px',
        border: `1px solid ${T.border}`,
        cursor: onClick ? 'pointer' : 'default',
        transition: 'all .15s',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Accent glow */}
      <div style={{
        position: 'absolute', top: 0, left: 0, right: 0, height: 2,
        background: `linear-gradient(90deg, transparent, ${color || T.accent}40, transparent)`,
      }}/>

      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: 9, color: T.textDim, fontWeight: 600, textTransform: 'uppercase', letterSpacing: 0.8, fontFamily: sans, marginBottom: 4 }}>
            {label}
          </div>
          <div style={{ fontSize: 22, fontWeight: 800, fontFamily: mono, color: color || T.accent, lineHeight: 1 }}>
            {value}
          </div>
          {sub && (
            <div style={{ fontSize: 9, color: T.textMuted, marginTop: 3, fontFamily: sans }}>
              {trend && <span style={{ color: trend > 0 ? T.green : T.red, marginRight: 4 }}>{trend > 0 ? '↑' : '↓'}{Math.abs(trend)}%</span>}
              {sub}
            </div>
          )}
        </div>
        {Icon && (
          <div style={{
            width: 32, height: 32, borderRadius: 8,
            background: `${color || T.accent}12`,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <Icon size={16} color={color || T.accent} />
          </div>
        )}
      </div>
    </div>
  )
}

// ═══ CARD ═══
export function Card({ title, subtitle, children, actions, accentColor, style, headerRight, noPad }) {
  const accent = accentColor || T.accent
  return (
    <div style={{
      background: T.bgCard,
      borderRadius: 10,
      border: `1px solid ${T.border}`,
      overflow: 'hidden',
      ...style,
    }}>
      {title && (
        <div style={{
          padding: '10px 14px',
          borderBottom: `1px solid ${T.border}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: `${accent}04`,
        }}>
          <div>
            <div style={{ fontSize: 12, fontWeight: 700, color: T.text, fontFamily: sans }}>{title}</div>
            {subtitle && <div style={{ fontSize: 9, color: T.textMuted, marginTop: 1 }}>{subtitle}</div>}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            {headerRight}
            {actions}
          </div>
        </div>
      )}
      <div style={{ padding: noPad ? 0 : '10px 14px' }}>
        {children}
      </div>
    </div>
  )
}

// ═══ TABLE COMPONENTS ═══
export function TH({ children, align = 'left', width, sortable, sorted, onSort }) {
  return (
    <th
      onClick={sortable ? onSort : undefined}
      style={{
        textAlign: align,
        padding: '6px 8px',
        fontSize: 9,
        fontWeight: 700,
        color: sorted ? T.accent : T.textDim,
        textTransform: 'uppercase',
        letterSpacing: 0.6,
        fontFamily: sans,
        borderBottom: `1px solid ${T.border}`,
        cursor: sortable ? 'pointer' : 'default',
        userSelect: 'none',
        whiteSpace: 'nowrap',
        width,
      }}
    >
      {children}
      {sorted && <span style={{ marginLeft: 3 }}>{sorted === 'asc' ? '↑' : '↓'}</span>}
    </th>
  )
}

export function TD({ children, align = 'left', mono: isMono, bold, color, style: customStyle }) {
  return (
    <td style={{
      textAlign: align,
      padding: '7px 8px',
      fontSize: 11,
      fontFamily: isMono ? mono : sans,
      fontWeight: bold ? 700 : 400,
      color: color || T.text,
      ...customStyle,
    }}>
      {children}
    </td>
  )
}

// ═══ BADGE ═══
export function Badge({ children, color, variant = 'filled', size = 'sm' }) {
  const isOutline = variant === 'outline'
  const padMap = { xs: '1px 4px', sm: '2px 7px', md: '3px 10px' }
  const sizeMap = { xs: 8, sm: 9, md: 10 }

  return (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: 3,
      padding: padMap[size],
      fontSize: sizeMap[size],
      fontWeight: 700,
      fontFamily: sans,
      borderRadius: 4,
      background: isOutline ? 'transparent' : `${color || T.accent}15`,
      color: color || T.accent,
      border: `1px solid ${color || T.accent}${isOutline ? '40' : '30'}`,
      whiteSpace: 'nowrap',
    }}>
      {children}
    </span>
  )
}

// ═══ PILL / TAG ═══
export function Pill({ label, color, active, onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: '3px 10px',
        fontSize: 9,
        fontWeight: active ? 700 : 500,
        background: active ? `${color || T.accent}15` : 'transparent',
        color: active ? (color || T.accent) : T.textMuted,
        border: `1px solid ${active ? (color || T.accent) + '40' : T.border}`,
        borderRadius: 4,
        cursor: 'pointer',
        fontFamily: sans,
        transition: 'all .1s',
        whiteSpace: 'nowrap',
      }}
    >
      {label}
    </button>
  )
}

// ═══ SECTION HEADER ═══
export function SectionHeader({ title, subtitle, action, icon: Icon, color }) {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: 10,
      paddingBottom: 6,
      borderBottom: `1px solid ${T.border}`,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        {Icon && <Icon size={16} color={color || T.accent} />}
        <div>
          <div style={{ fontSize: 14, fontWeight: 700, color: T.text, fontFamily: sans }}>{title}</div>
          {subtitle && <div style={{ fontSize: 10, color: T.textMuted }}>{subtitle}</div>}
        </div>
      </div>
      {action}
    </div>
  )
}

// ═══ EMPTY STATE ═══
export function EmptyState({ icon: Icon, title, description, action }) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '40px 20px',
      textAlign: 'center',
    }}>
      {Icon && <Icon size={40} color={T.textDim} style={{ marginBottom: 12, opacity: 0.4 }} />}
      <div style={{ fontSize: 14, fontWeight: 700, color: T.textMuted, marginBottom: 4 }}>{title}</div>
      {description && <div style={{ fontSize: 11, color: T.textDim, maxWidth: 300, lineHeight: 1.4 }}>{description}</div>}
      {action && <div style={{ marginTop: 12 }}>{action}</div>}
    </div>
  )
}

// ═══ LOADING SKELETON ═══
export function Skeleton({ width = '100%', height = 16, radius = 4 }) {
  return (
    <div style={{
      width,
      height,
      borderRadius: radius,
      background: `linear-gradient(90deg, ${T.bgAccent} 25%, ${T.bgHover} 50%, ${T.bgAccent} 75%)`,
      backgroundSize: '200% 100%',
      animation: 'shimmer 1.5s infinite',
    }} />
  )
}

// ═══ PROGRESS BAR ═══
export function ProgressBar({ value, max = 100, color, height = 6, showLabel }) {
  const pct = Math.min((value / max) * 100, 100)
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, width: '100%' }}>
      <div style={{
        flex: 1, height, background: T.bgAccent, borderRadius: height / 2, overflow: 'hidden',
      }}>
        <div style={{
          width: `${pct}%`, height: '100%',
          background: color || T.accent,
          borderRadius: height / 2,
          transition: 'width .3s ease',
        }} />
      </div>
      {showLabel && (
        <span style={{ fontSize: 9, fontFamily: mono, color: color || T.accent, fontWeight: 700, minWidth: 32, textAlign: 'right' }}>
          {Math.round(pct)}%
        </span>
      )}
    </div>
  )
}

// ═══ AVATAR ═══
export function Avatar({ name, src, size = 28, color }) {
  const initials = name?.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase() || '?'
  const bgColor = color || T.accent

  if (src) {
    return <img src={src} alt={name} style={{ width: size, height: size, borderRadius: size / 2, objectFit: 'cover' }} />
  }

  return (
    <div style={{
      width: size, height: size, borderRadius: size / 2,
      background: `${bgColor}20`,
      color: bgColor,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontSize: size * 0.36, fontWeight: 700, fontFamily: sans,
    }}>
      {initials}
    </div>
  )
}

// ═══ TOOLTIP WRAPPER ═══
export function Tooltip({ children, content, position = 'top' }) {
  const [show, setShow] = React.useState(false)
  return (
    <div
      style={{ position: 'relative', display: 'inline-flex' }}
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
    >
      {children}
      {show && content && (
        <div style={{
          position: 'absolute',
          [position === 'top' ? 'bottom' : 'top']: '100%',
          left: '50%',
          transform: 'translateX(-50%)',
          marginBottom: position === 'top' ? 6 : 0,
          marginTop: position === 'bottom' ? 6 : 0,
          padding: '4px 8px',
          background: T.bgCard,
          border: `1px solid ${T.border}`,
          borderRadius: 4,
          fontSize: 9,
          color: T.textMuted,
          whiteSpace: 'nowrap',
          zIndex: 100,
          boxShadow: T.shadow,
          fontFamily: sans,
          pointerEvents: 'none',
        }}>
          {content}
        </div>
      )}
    </div>
  )
}
