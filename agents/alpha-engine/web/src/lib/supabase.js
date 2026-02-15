// ════════════════════════════════════════════════════
// Supabase Client — Web (browser) side
// Respects Row Level Security
// ════════════════════════════════════════════════════
import { createClient } from '@supabase/supabase-js'
import { useState, useEffect, createContext, useContext } from 'react'

const supabaseUrl = process.env.SUPABASE_URL || ''
const supabaseAnonKey = process.env.SUPABASE_ANON_KEY || ''

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// ═══ Auth Context ═══
const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setUser(session?.user ?? null)
      setLoading(false)
    })

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session)
        setUser(session?.user ?? null)
        setLoading(false)
      }
    )

    return () => subscription.unsubscribe()
  }, [])

  const signIn = async (email, password) => {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) throw error
    return data
  }

  const signInWithOAuth = async (provider) => {
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider,
      options: { redirectTo: `${window.location.origin}/auth/callback` },
    })
    if (error) throw error
    return data
  }

  const signOut = async () => {
    const { error } = await supabase.auth.signOut()
    if (error) throw error
  }

  const value = { user, session, loading, signIn, signInWithOAuth, signOut }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}

// ═══ Realtime Hook ═══
export function useRealtimeSubscription(table, callback, filter) {
  useEffect(() => {
    let channel = supabase
      .channel(`realtime:${table}`)
      .on('postgres_changes', { event: '*', schema: 'public', table, ...filter }, callback)
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [table, callback])
}

// ═══ Data Hooks ═══
export function useSupabaseQuery(table, query = {}) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let mounted = true
    setLoading(true)

    let q = supabase.from(table).select(query.select || '*')
    if (query.order) q = q.order(query.order.column, { ascending: query.order.ascending ?? false })
    if (query.limit) q = q.limit(query.limit)
    if (query.eq) Object.entries(query.eq).forEach(([k, v]) => { q = q.eq(k, v) })
    if (query.in) Object.entries(query.in).forEach(([k, v]) => { q = q.in(k, v) })

    q.then(({ data, error }) => {
      if (mounted) {
        setData(data)
        setError(error)
        setLoading(false)
      }
    })

    return () => { mounted = false }
  }, [table, JSON.stringify(query)])

  return { data, loading, error, refetch: () => setLoading(true) }
}

export default supabase
