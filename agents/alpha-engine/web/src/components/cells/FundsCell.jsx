export const QUERY = gql`
  query FundsQuery($status: FundStatus, $strategy: FundStrategy) {
    funds(status: $status, strategy: $strategy) {
      id name shortName gpName strategy vintage fundSize status
      tvpiGross tvpiNet irrGross irrNet dpiNet rvpiNet quartile
      mgmtFeeRate carryRate sector geography
      commitments { id amount unfunded }
    }
  }
`
export const Loading = () => <div>Loading funds...</div>
export const Empty = () => <div>No funds found</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ funds }) => <div>{JSON.stringify(funds.length)} funds loaded</div>
