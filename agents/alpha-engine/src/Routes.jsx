import { Router, Route, Set, Private } from '@redwoodjs/router'
import MainLayout from './layouts/MainLayout'

const Routes = () => {
  return (
    <Router>
      <Route path="/login" page={() => import('./pages/LoginPage')} name="login" />
      <Private unauthenticated="login">
        <Set wrap={MainLayout}>
          <Route path="/" page={() => import('./pages/DashboardPage')} name="dashboard" />
          <Route path="/platform" page={() => import('./pages/PlatformPage')} name="platform" />
        </Set>
      </Private>
      <Route notfound page={() => import('./pages/NotFoundPage')} name="notFound" />
    </Router>
  )
}

export default Routes
