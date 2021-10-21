from django.contrib.auth.models import User

class IsAuthenticated(object):
  @staticmethod
  def has_permission(context):
    return context.user and context.user.is_authenticated


class CanViewUser(object):
  @staticmethod
  def has_permission(context):
    return context.user and context.user.has_perm('auth.view_user')
