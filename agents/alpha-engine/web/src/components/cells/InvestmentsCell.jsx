export const QUERY = gql`
  query InvestmentsQuery($fundId: String, $status: InvestmentStatus) {
    investments(fundId: $fundId, status: $status) {
      id type status investDate costBasis currentValue ownership moic irr board leadInvestor
      company { id name sector stage logoUrl }
      fund { id name }
    }
  }
`
export const Loading = () => <div>Loading investments...</div>
export const Empty = () => <div>No investments found</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ investments }) => <div>{investments.length} positions</div>
