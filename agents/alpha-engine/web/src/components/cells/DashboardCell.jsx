import { Card, Stat, Badge, Skeleton } from 'src/components/ui/CoreUI'
import { theme as T } from 'src/lib/theme'

export const QUERY = gql`
  query DashboardMetricsQuery {
    dashboardMetrics {
      portfolio {
        totalAum
        fundCount
        activeDeals
        wtdTvpi
        wtdIrr
        totalCommitted
        totalUnfunded
        totalDistributed
        topQuartilePct
      }
      recentActivity {
        id type title description createdAt
        user { name }
      }
      urgentTasks {
        id title status priority dueDate
      }
      pendingDecisions {
        id title type amount deadline status compositeScore
      }
      upcomingExits {
        id type status exitValuation probability expectedDate
        company { name sector }
      }
      latestInsights {
        id agentName type title content confidence createdAt
      }
    }
  }
`
export const Loading = () => (
  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
    {[...Array(8)].map((_, i) => <Skeleton key={i} height={80} radius={10} />)}
  </div>
)
export const Empty = () => <div style={{ color: T.textDim, padding: 40, textAlign: 'center' }}>No data yet. Connect your Supabase instance.</div>
export const Failure = ({ error }) => <div style={{ color: T.red, padding: 20 }}>Error: {error.message}</div>
export const Success = ({ dashboardMetrics }) => {
  const { portfolio: p } = dashboardMetrics
  return <div>{/* Rendered by DashboardPage */}</div>
}
