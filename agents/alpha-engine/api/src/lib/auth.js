import { AuthenticationError, ForbiddenError } from '@redwoodjs/graphql-server'
import { supabaseAdmin } from './supabase'

export const getCurrentUser = async (session) => {
  if (!session?.id) return null
  try {
    const { data: user } = await supabaseAdmin
      .from('users')
      .select('*')
      .eq('supabase_id', session.id)
      .single()
    return user
  } catch (e) {
    return null
  }
}

export const isAuthenticated = () => {
  return !!context.currentUser
}

export const hasRole = (roles) => {
  if (!isAuthenticated()) return false
  const userRole = context.currentUser?.role
  if (typeof roles === 'string') return userRole === roles
  return roles.includes(userRole)
}

export const requireAuth = ({ roles } = {}) => {
  if (!isAuthenticated()) throw new AuthenticationError('Not authenticated')
  if (roles && !hasRole(roles)) throw new ForbiddenError('Insufficient permissions')
}
