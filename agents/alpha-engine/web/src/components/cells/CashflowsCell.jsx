export const QUERY = gql`
  query CashflowsQuery($fundId: String!) {
    cashflows(fundId: $fundId) {
      id fundId type amount date description category isProjected
    }
    cashflowSummary(fundId: $fundId)
  }
`
export const Loading = () => <div>Loading cashflows...</div>
export const Empty = () => <div>No cashflows</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ cashflows, cashflowSummary }) => <div>{cashflows.length} flows</div>
