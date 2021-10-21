
# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#

from django.contrib.auth import logout
import graphene
import graphql_jwt
import innolla.queries as query
import innolla.mutations as mutation


class LogOutMutation(graphene.Mutation):
  logged_out = graphene.Boolean()

  def mutate(self, info):
    logged_out = False
    try:
      logout(info.context)
      logged_out = True
    except:
      pass
    return LogOutMutation(logged_out=logged_out)


class Query(query.Query, graphene.ObjectType):
  # This class will inherit from multiple Queries
  # as we begin to add more apps to our project
  pass

class Mutation(mutation.Mutation, graphene.ObjectType, ):
  token_auth = graphql_jwt.ObtainJSONWebToken.Field()
  verify_token = graphql_jwt.Verify.Field()
  refresh_token = graphql_jwt.Refresh.Field()
  logout_mutation = LogOutMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
