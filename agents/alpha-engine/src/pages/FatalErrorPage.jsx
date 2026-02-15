import React from 'react'

const FatalErrorPage = () => (
  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', background: '#0a0f1a', color: '#e2e8f0', fontFamily: "'DM Sans', sans-serif" }}>
    <div style={{ textAlign: 'center', maxWidth: 400 }}>
      <h1 style={{ fontSize: 24, fontWeight: 800, color: '#ef4444' }}>Something went wrong</h1>
      <p style={{ color: '#64748b', fontSize: 13 }}>The platform encountered an unexpected error. Please refresh or contact the team.</p>
      <button onClick={() => window.location.reload()} style={{ padding: '8px 16px', background: '#3b82f6', border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer', fontSize: 13, fontWeight: 600 }}>Refresh</button>
    </div>
  </div>
)

export default FatalErrorPage
