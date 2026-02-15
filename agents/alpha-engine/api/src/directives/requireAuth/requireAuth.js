import { createValidatorDirective } from '@redwoodjs/graphql-server'
import { requireAuth as appRequireAuth } from 'src/lib/auth'

export const schema = gql`
  directive @requireAuth(roles: [String]) on FIELD_DEFINITION
`
const validate = ({ directiveArgs }) => {
  appRequireAuth({ roles: directiveArgs?.roles })
}
const requireAuth = createValidatorDirective(schema, validate)
export default requireAuth
