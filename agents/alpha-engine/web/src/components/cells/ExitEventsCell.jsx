export const QUERY = gql`
  query ExitEventsQuery($status: ExitStatus) {
    exitEvents(status: $status) {
      id type status expectedDate actualDate exitValuation navImpact probability catalyst thesis sources
      company { id name sector stage }
    }
  }
`
export const Loading = () => <div>Loading exits...</div>
export const Empty = () => <div>No exit events</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ exitEvents }) => <div>{exitEvents.length} exits</div>
