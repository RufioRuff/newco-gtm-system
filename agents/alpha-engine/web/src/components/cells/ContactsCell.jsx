export const QUERY = gql`
  query ContactsQuery($tier: ContactTier, $search: String) {
    contacts(tier: $tier, search: $search) {
      id name email title tier type
      reachScore authorityScore velocityScore compositeScore
      lastContactedAt
      companies { company { name } role current }
    }
  }
`
export const Loading = () => <div>Loading contacts...</div>
export const Empty = () => <div>No contacts found</div>
export const Failure = ({ error }) => <div>Error: {error.message}</div>
export const Success = ({ contacts }) => <div>{contacts.length} contacts</div>
