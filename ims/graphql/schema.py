import graphene
import graphql_jwt
from members.graphql.query import MemberQueries
from members.graphql.mutation import MemberMutation


class Query(MemberQueries):
    pass


class Mutation(MemberMutation):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
