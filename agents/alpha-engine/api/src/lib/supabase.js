// ════════════════════════════════════════════
// Supabase Client — Shared across API services
// ════════════════════════════════════════════
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.SUPABASE_URL
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY

if (!supabaseUrl || !supabaseServiceKey) {
  console.warn('⚠️  Supabase credentials not configured. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY.')
}

// Server-side client with service role (bypasses RLS)
export const supabaseAdmin = createClient(supabaseUrl, supabaseServiceKey, {
  auth: { persistSession: false },
})

// Client-side client (respects RLS) — used in web/
export const createSupabaseClient = (anonKey) => {
  return createClient(supabaseUrl, anonKey || process.env.SUPABASE_ANON_KEY)
}

export default supabaseAdmin
