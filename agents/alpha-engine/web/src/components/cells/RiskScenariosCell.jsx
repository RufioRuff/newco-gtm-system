export const QUERY = gql`
  query RiskScenariosQuery {
    riskScenarios {
      id name category probability severity navImpactPct description mitigants affectedFunds results
    }
  }
`
export const Loading = () => <div>Loading risk scenarios...</div>
export const Empty = () => <div>No scenarios</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ riskScenarios }) => <div>{riskScenarios.length} scenarios</div>
