export const QUERY = gql`
  query GPScorecardsQuery {
    gpScorecards {
      id fundId returnsScore teamScore processScore termsScore fitScore compositeScore
      factorScores strengths concerns thesis benchmarkRank
      fund { id name gpName strategy vintage }
    }
  }
`
export const Loading = () => <div>Loading GP scorecards...</div>
export const Empty = () => <div>No scorecards</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ gpScorecards }) => <div>{gpScorecards.length} scorecards</div>
