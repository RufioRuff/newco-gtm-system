import React, { useState } from 'react'
import { useAuth } from '@redwoodjs/auth-supabase-web'
import { navigate, routes } from '@redwoodjs/router'

const LoginPage = () => {
  const { logIn } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await logIn({ email, password })
      navigate(routes.dashboard())
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', background: '#0a0f1a', fontFamily: "'DM Sans', sans-serif" }}>
      <div style={{ width: 380, padding: 32, background: '#111827', borderRadius: 12, border: '1px solid #1e293b' }}>
        <div style={{ textAlign: 'center', marginBottom: 24 }}>
          <div style={{ width: 48, height: 48, borderRadius: 10, background: 'linear-gradient(135deg, #3b82f6, #60a5fa)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', marginBottom: 12 }}>
            <span style={{ fontSize: 24, fontWeight: 900, color: '#0a0f1a' }}>N</span>
          </div>
          <h1 style={{ fontSize: 22, fontWeight: 800, color: '#e2e8f0', margin: 0 }}>NEWCO V10</h1>
          <p style={{ fontSize: 12, color: '#64748b', marginTop: 4 }}>Intelligence LP Platform</p>
        </div>
        <form onSubmit={handleSubmit}>
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" style={{ width: '100%', padding: '10px 12px', marginBottom: 10, background: '#1a2332', border: '1px solid #1e293b', borderRadius: 6, color: '#e2e8f0', fontSize: 13 }} />
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" style={{ width: '100%', padding: '10px 12px', marginBottom: 16, background: '#1a2332', border: '1px solid #1e293b', borderRadius: 6, color: '#e2e8f0', fontSize: 13 }} />
          {error && <p style={{ color: '#ef4444', fontSize: 12, marginBottom: 10 }}>{error}</p>}
          <button type="submit" style={{ width: '100%', padding: '10px 16px', background: '#3b82f6', border: 'none', borderRadius: 6, color: '#fff', fontSize: 13, fontWeight: 700, cursor: 'pointer' }}>Sign In</button>
        </form>
      </div>
    </div>
  )
}

export default LoginPage
