import React from 'react'

const NotFoundPage = () => (
  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', background: '#0a0f1a', color: '#e2e8f0', fontFamily: "'DM Sans', sans-serif" }}>
    <div style={{ textAlign: 'center' }}>
      <h1 style={{ fontSize: 48, fontWeight: 900, color: '#3b82f6' }}>404</h1>
      <p style={{ color: '#64748b' }}>Page not found</p>
      <a href="/" style={{ color: '#3b82f6', fontSize: 13 }}>← Back to NEWCO</a>
    </div>
  </div>
)

export default NotFoundPage
