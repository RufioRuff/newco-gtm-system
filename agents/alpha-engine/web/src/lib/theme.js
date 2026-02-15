// ════════════════════════════════════════════════════
// NEWCO THEME SYSTEM — Institutional Dark UI
// Evil Twin Capital · Design Tokens
// ════════════════════════════════════════════════════

export const fonts = {
  sans: "'SF Pro Display', -apple-system, BlinkMacSystemFont, system-ui, sans-serif",
  mono: "'SF Mono', 'Fira Code', 'JetBrains Mono', monospace",
  display: "'SF Pro Display', system-ui, sans-serif",
}

export const theme = {
  // Backgrounds
  bg: '#0B0E11',
  bgCard: '#12161B',
  bgAccent: '#181D24',
  bgHover: '#1E242C',
  bgGlass: 'rgba(18, 22, 27, 0.85)',

  // Borders
  border: '#232A34',
  borderSubtle: '#1A2029',
  borderActive: '#2A3340',

  // Text
  text: '#E8ECF1',
  textMuted: '#8B95A5',
  textDim: '#5A6577',
  textBright: '#FFFFFF',

  // Accent palette
  accent: '#FF6B35',        // Evil Twin signature orange
  accentBg: 'rgba(255, 107, 53, 0.08)',
  accentHover: '#FF8855',

  // Semantic colors
  green: '#34D399',
  greenBg: 'rgba(52, 211, 153, 0.08)',
  blue: '#60A5FA',
  blueBg: 'rgba(96, 165, 250, 0.08)',
  purple: '#A78BFA',
  purpleBg: 'rgba(167, 139, 250, 0.08)',
  amber: '#FBBF24',
  amberBg: 'rgba(251, 191, 36, 0.08)',
  red: '#F87171',
  redBg: 'rgba(248, 113, 113, 0.08)',
  gold: '#F59E0B',
  cyan: '#22D3EE',
  pink: '#F472B6',

  // Gradients
  gradientAccent: 'linear-gradient(135deg, #FF6B35 0%, #FF8855 100%)',
  gradientCard: 'linear-gradient(180deg, #181D24 0%, #12161B 100%)',
  gradientGlow: 'radial-gradient(ellipse at 50% 0%, rgba(255,107,53,0.08) 0%, transparent 60%)',

  // Shadows
  shadow: '0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2)',
  shadowLg: '0 10px 40px rgba(0,0,0,0.4)',
  shadowGlow: '0 0 20px rgba(255,107,53,0.15)',

  // Spacing
  radius: '8px',
  radiusLg: '12px',
  radiusSm: '4px',
}

// Chart color palette for D3/Recharts
export const chartColors = [
  '#FF6B35', '#60A5FA', '#34D399', '#A78BFA',
  '#FBBF24', '#F87171', '#22D3EE', '#F472B6',
  '#818CF8', '#FB923C', '#4ADE80', '#E879F9',
]

// Tier colors for network visualization
export const tierColors = {
  PLATFORM: '#FF6B35',
  CAPITAL: '#34D399',
  MULTIPLIER: '#A78BFA',
  INSTITUTIONAL: '#60A5FA',
  BERKELEY: '#FBBF24',
  TEAM: '#22D3EE',
  GENERAL: '#8B95A5',
}

// Fund strategy colors
export const strategyColors = {
  VENTURE: '#FF6B35',
  GROWTH: '#60A5FA',
  BUYOUT: '#34D399',
  SECONDARY: '#A78BFA',
  CO_INVEST: '#FBBF24',
  FUND_OF_FUNDS: '#22D3EE',
  REAL_ASSETS: '#F472B6',
  CREDIT: '#818CF8',
}

// Health status colors
export const healthColors = {
  HEALTHY: '#34D399',
  WATCH: '#FBBF24',
  ALERT: '#F87171',
  CRITICAL: '#EF4444',
}

// Deal status colors
export const dealStatusColors = {
  SCREENING: '#8B95A5',
  INITIAL_REVIEW: '#60A5FA',
  DUE_DILIGENCE: '#A78BFA',
  IC_REVIEW: '#FBBF24',
  NEGOTIATION: '#FF6B35',
  CLOSED: '#34D399',
  PASSED: '#5A6577',
  LOST: '#F87171',
}

export default theme
