export const QUERY = gql`
  query PlatformDealsQuery($status: PlatformStatus) {
    platformDeals(status: $status) {
      id platformName status contactName aum advisorCount
      minimumInvest targetClose estimatedAum probability nextAction
    }
  }
`
export const Loading = () => <div>Loading platforms...</div>
export const Empty = () => <div>No platform deals</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ platformDeals }) => <div>{platformDeals.length} platforms</div>
