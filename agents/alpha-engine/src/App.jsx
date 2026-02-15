import React from 'react'
import { FatalErrorBoundary, RedwoodProvider } from '@redwoodjs/web'
import { AuthProvider, useAuth } from '@redwoodjs/auth-supabase-web'
import { supabase } from './lib/supabase'
import FatalErrorPage from './pages/FatalErrorPage'
import Routes from './Routes'

const App = () => (
  <FatalErrorBoundary page={FatalErrorPage}>
    <RedwoodProvider titleTemplate="%PageTitle | NEWCO V10">
      <AuthProvider client={supabase}>
        <Routes />
      </AuthProvider>
    </RedwoodProvider>
  </FatalErrorBoundary>
)

export default App
