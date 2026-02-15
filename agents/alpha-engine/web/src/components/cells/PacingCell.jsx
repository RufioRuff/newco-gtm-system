export const QUERY = gql`
  query PacingPlansQuery {
    pacingPlans {
      id year targetCommit actualCommit strategy vintageTarget jCurveData
    }
  }
`
export const Loading = () => <div>Loading pacing...</div>
export const Empty = () => <div>No pacing plans</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ pacingPlans }) => <div>{pacingPlans.length} plans</div>
