export const QUERY = gql`
  query NetworkQuery {
    networkSummary {
      totalNodes totalEdges dualLpCustomer estimatedAum platformReach
      topContacts { id name tier compositeScore }
    }
    networkEdges {
      id sourceId targetId relationshipType strength
      source { id name tier compositeScore }
      target { id name tier compositeScore }
    }
  }
`
export const Loading = () => <div>Loading network...</div>
export const Empty = () => <div>No network data</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ networkSummary, networkEdges }) => <div>{networkSummary.totalNodes} nodes</div>
