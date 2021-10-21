
# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#

import graphene
from graphene import relay
from graphql_relay import from_global_id
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from graphene_django import DjangoObjectType, DjangoListField

from project.graphene_django.types import OptimizerMixin, PermissionClassesTypeMixin
from project.graphene_django.permissions import IsAuthenticated

from innolla.models import Unit, Room, ActivityTime, Tag, ProfileTag, Profile, Assessment, AssessmentQuestion, AssessmentResponse, SmallGroup

User = get_user_model()


class TagNode(OptimizerMixin, PermissionClassesTypeMixin, DjangoObjectType):
  class Meta:
    model = Tag
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class ProfileTagNode(OptimizerMixin, PermissionClassesTypeMixin, DjangoObjectType):
  class Meta:
    model = ProfileTag
    interfaces = (graphene.relay.Node, )

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class ProfileNode(OptimizerMixin, PermissionClassesTypeMixin, DjangoObjectType):
  unit = graphene.Field('innolla.queries.UnitNode')
  tags = DjangoListField(TagNode)
  activities = graphene.List('innolla.queries.ActivityTimeNode')
  assessments = graphene.List('innolla.queries.AssessmentNode')

  def resolve_activities(self, info):
    return ActivityTime.objects.all()

  def resolve_assessments(self, info):
    return Assessment.objects.all()

  class Meta:
    model = Profile
    interfaces = (graphene.relay.Node, )

  def resolve_tags(self, info):
    return Tag.objects.filter(profiletag__profile=self)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class PermissionNode(OptimizerMixin, PermissionClassesTypeMixin, DjangoObjectType):
  class Meta:
    model = Permission
    interfaces = (graphene.relay.Node, )

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class GroupNode(OptimizerMixin, PermissionClassesTypeMixin, DjangoObjectType):
  permissions = DjangoListField(PermissionNode)

  class Meta:
    model = Group
    interfaces = (graphene.relay.Node, )

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class UserNode(OptimizerMixin, PermissionClassesTypeMixin, DjangoObjectType):
  groups = DjangoListField(GroupNode)
  profile = graphene.Field(ProfileNode)

  class Meta:
    model = User
    interfaces = (graphene.relay.Node, )
    fields = [
      'id',
      'username',
      'email',
      'first_name',
      'last_name',
      'groups',
      'profile',
    ]

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class AssessmentResponseNode(OptimizerMixin, PermissionClassesTypeMixin, DjangoObjectType):
  class Meta:
    model = AssessmentResponse
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class AssessmentNode(OptimizerMixin, PermissionClassesTypeMixin, DjangoObjectType):
  of_activity = graphene.Field('innolla.queries.ActivityTimeNode')
  responses = DjangoListField(AssessmentResponseNode)

  class Meta:
    model = Assessment
    interfaces = (graphene.relay.Node, )

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class AssessmentQuestionNode(OptimizerMixin, PermissionClassesTypeMixin, DjangoObjectType):
  class Meta:
    model = AssessmentQuestion
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class SmallGroupNode(OptimizerMixin, PermissionClassesTypeMixin, DjangoObjectType):
  title = graphene.String()
  unit = graphene.Field('innolla.queries.UnitNode')
  profiles = DjangoListField(ProfileNode)

  class Meta:
    model = SmallGroup
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    fields = (
      'id',
      'title',
      'unit',
      'profiles',
    )

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class ActivityTimeNode(OptimizerMixin, PermissionClassesTypeMixin, DjangoObjectType):
  participants = DjangoListField(ProfileNode)
  small_groups = DjangoListField('innolla.queries.SmallGroupNode')

  class Meta:
    model = ActivityTime
    interfaces = (graphene.relay.Node, )

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class RoomNode(OptimizerMixin, PermissionClassesTypeMixin, DjangoObjectType):
  image = graphene.String()
  activities = DjangoListField(ActivityTimeNode)
  unit = graphene.Field('innolla.queries.UnitNode')

  class Meta:
    model = Room
    interfaces = (graphene.relay.Node, )

  def resolve_image(self, info):
    if self.image:
      self.image = info.context.build_absolute_uri(self.image.url)
    return self.image

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class UnitNode(OptimizerMixin, PermissionClassesTypeMixin, DjangoObjectType):
  floor_plan = graphene.String()
  rooms = DjangoListField(RoomNode)

  class Meta:
    interfaces = (graphene.relay.Node, )
    model = Unit

  def resolve_floor_plan(self, info):
    if self.floor_plan:
      self.floor_plan = info.context.build_absolute_uri(self.floor_plan.url)
    return self.floor_plan

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class Query(graphene.ObjectType):
  current_user = graphene.Field(UserNode)

  users = DjangoListField(UserNode)
  user = relay.Node.Field(UserNode)

  profiles = DjangoListField(ProfileNode, group=graphene.ID())
  profile = relay.Node.Field(ProfileNode)

  def resolve_profiles(self, info, **kwargs):
    _group = kwargs.get('group', None)
    if _group:
      _, _id = from_global_id(_group)
      return Profile.objects.filter(groups__in=_id)
    return Profile.objects.all()

  units = DjangoListField(UnitNode)
  unit = relay.Node.Field(UnitNode)

  rooms = DjangoListField(RoomNode)
  room = relay.Node.Field(RoomNode)

  activity_times = DjangoListField(ActivityTimeNode)
  activity_time = relay.Node.Field(ActivityTimeNode)

  assessments = DjangoListField(AssessmentNode)
  assessment = relay.Node.Field(AssessmentNode)

  assessment_questions = DjangoListField(AssessmentQuestionNode)
  assessment_question = relay.Node.Field(AssessmentQuestionNode)

  assessment_responses = DjangoListField(AssessmentResponseNode, assessment=graphene.ID())
  assessment_response = relay.Node.Field(AssessmentResponseNode)

  def resolve_assessment_responses(self, info, **kwargs):
    _assessment = kwargs.get('assessment', None)
    if _assessment:
      _, _id = from_global_id(_assessment)
      return AssessmentResponse.objects.filter(assessment=_id)
    return AssessmentResponse.objects.all()

  tags = DjangoListField(TagNode)
  tag = relay.Node.Field(TagNode)

  small_groups = DjangoListField(SmallGroupNode)
  small_group = relay.Node.Field(SmallGroupNode)

  groups = DjangoListField(GroupNode)
  group = relay.Node.Field(GroupNode)

  permissions = DjangoListField(PermissionNode)
  permission = relay.Node.Field(PermissionNode)


  def resolve_current_user(self, info):
    user = info.context.user
    if user.is_anonymous:
      return Exception('Not logged in')
    return user

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
