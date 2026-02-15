export const QUERY = gql`
  query AlphaAttributionQuery {
    alphaAttributions {
      id period totalAlpha managerSelect timingAlpha coInvestAlpha secondaryAlpha
      sharpeRatio infoRatio hitRate details
    }
  }
`
export const Loading = () => <div>Loading attribution...</div>
export const Empty = () => <div>No attribution data</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ alphaAttributions }) => <div>{alphaAttributions.length} periods</div>
