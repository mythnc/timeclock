import graphene
import graphql_jwt

import users.schema


class Query(
    users.schema.Query
):
    pass


class Mutation(
    users.schema.Mutation
):
    obtain_token = graphql_jwt.ObtainJSONWebToken.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)