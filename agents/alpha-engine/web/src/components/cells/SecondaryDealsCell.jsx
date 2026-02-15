export const QUERY = gql`
  query SecondaryDealsQuery($status: DealStatus) {
    secondaryDeals(status: $status) {
      id name category status askPrice bidPrice nav discountToNav
      tvpi vintage fairValue irrBase irrBull irrBear
      thesis catalysts risks deadline
      fund { id name gpName }
      icDecision { id status compositeScore }
    }
  }
`
export const Loading = () => <div>Loading deals...</div>
export const Empty = () => <div>No secondary deals</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ secondaryDeals }) => <div>{secondaryDeals.length} deals</div>
