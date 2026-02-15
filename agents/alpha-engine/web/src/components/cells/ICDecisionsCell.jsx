export const QUERY = gql`
  query ICDecisionsQuery($status: ICStatus) {
    icDecisions(status: $status) {
      id title type amount deadline status compositeScore
      scores thesis keyRisks mitigants
      votes { id vote conviction comment user { name } }
      deal { id name category askPrice bidPrice nav }
    }
  }
`
export const Loading = () => <div>Loading IC decisions...</div>
export const Empty = () => <div>No pending decisions</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ icDecisions }) => <div>{icDecisions.length} decisions</div>
