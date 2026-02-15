// NEWCO V10 Design Tokens
// Institutional dark theme inspired by Bloomberg Terminal + modern fintech

export const theme = {
  // Backgrounds
  bg: '#0a0f1a',
  bgCard: '#111827',
  bgAccent: '#1a2332',

  // Text
  text: '#e2e8f0',
  textMuted: '#94a3b8',
  textDim: '#64748b',

  // Accent Colors
  accent: '#3b82f6',    // Primary blue
  accentBg: '#3b82f610',

  // Semantic Colors
  green: '#22c55e',
  red: '#ef4444',
  amber: '#f59e0b',
  blue: '#3b82f6',
  purple: '#a855f7',
  gold: '#eab308',

  // Borders
  border: '#1e293b',

  // Fonts
  sans: "'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif",
  mono: "'JetBrains Mono', 'SF Mono', Consolas, monospace",

  // Spacing
  spacing: {
    xs: 4,
    sm: 8,
    md: 12,
    lg: 16,
    xl: 24,
    xxl: 32,
  },

  // Border Radius
  radius: {
    sm: 4,
    md: 6,
    lg: 8,
    xl: 12,
    full: 9999,
  },

  // Shadows
  shadow: {
    sm: '0 1px 2px rgba(0,0,0,0.2)',
    md: '0 4px 12px rgba(0,0,0,0.3)',
    lg: '0 8px 24px rgba(0,0,0,0.4)',
    accent: '0 2px 8px rgba(59,130,246,0.2)',
  },
} as const

export type Theme = typeof theme
