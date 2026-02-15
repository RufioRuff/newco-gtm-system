export const QUERY = gql`
  query AgentRunsQuery($agentName: String) {
    agentRuns(agentName: $agentName, limit: 20) {
      id agentName status triggeredBy output tokensUsed costUsd durationMs error startedAt completedAt
    }
    aiInsights(limit: 10) {
      id agentName type title content confidence entityType entityId isActioned createdAt
    }
  }
`
export const Loading = () => <div>Loading agents...</div>
export const Empty = () => <div>No agent runs</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ agentRuns, aiInsights }) => <div>{agentRuns.length} runs, {aiInsights.length} insights</div>
