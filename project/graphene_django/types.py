import graphene_django_optimizer as gql_optimizer

from project.graphene_django.exceptions import PermissionDenied

class OptimizerMixin(object):
  @classmethod
  def get_queryset(cls, qs, info):
    return gql_optimizer.query(super().get_queryset(qs, info), info)


class PermissionClassesTypeMixin(object):
  @classmethod
  def get_queryset(cls, qs, info):
    permissions = cls.permission_classes()

    for permission in permissions:
      if not permission.has_permission(info.context):
        raise PermissionDenied

    return super().get_queryset(qs, info)

  @staticmethod
  def permission_classes():
    raise NotImplementedError
