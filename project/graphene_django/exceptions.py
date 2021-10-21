from django.utils.translation import ugettext_lazy as _

from graphql import GraphQLError as BaseGraphQLError


class GraphQLError(BaseGraphQLError):
  message = _("An error occurred")

  def __init__(self, *args, message=None, **kwags):
    if message is None:
      message = self.message
    super(GraphQLError, self).__init__(message, *args, **kwags)


class PermissionDenied(GraphQLError):
  message = _("You do not have permission to perform this action")


class DeleteError(GraphQLError):
  message = _("Couldn't delete this item")
