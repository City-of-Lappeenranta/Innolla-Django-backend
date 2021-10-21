import graphene
from django.contrib.auth import get_user_model
from graphene_file_upload.scalars import Upload

from project.graphene_django.mutations import UpsertMutation, DeleteMutation, PermissionClassesMutationMixin
from project.graphene_django.permissions import IsAuthenticated

from innolla.queries import UserNode, ProfileNode, UnitNode, RoomNode, ActivityTimeNode, TagNode, ProfileTagNode, AssessmentNode, AssessmentQuestionNode, AssessmentResponseNode, SmallGroupNode
from innolla.models import Unit, Room, ActivityTime, Tag, Profile, Assessment, AssessmentResponse, AssessmentQuestion, ProfileTag, SmallGroup


User = get_user_model()


class UserUpsert(PermissionClassesMutationMixin, UpsertMutation):
  class Meta:
    model = User
    return_node = UserNode

  class Input:
    id = graphene.ID(required=False)
    username = graphene.String(required=False)
    email = graphene.String(required=False)
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)
    groups = graphene.List(graphene.ID)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class UserDelete(PermissionClassesMutationMixin, DeleteMutation):
  class Meta:
    model = User
    return_node = UserNode

  class Input:
    id = graphene.ID(required=True)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class ProfileUpsert(PermissionClassesMutationMixin, UpsertMutation):
  class Meta:
    model = Profile
    return_node = ProfileNode

  class Input:
    id = graphene.ID(required=False)
    user = graphene.ID(required=False)
    unit = graphene.ID(required=False)
    picture = Upload(required=False)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class ProfileDelete(PermissionClassesMutationMixin, DeleteMutation):
  class Meta:
    model = Profile
    return_node = ProfileNode

  class Input:
    id = graphene.ID(required=True)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class UnitUpsert(PermissionClassesMutationMixin, UpsertMutation):
  class Meta:
    model = Unit
    return_node = UnitNode

  class Input:
    id = graphene.ID(required=False)
    title = graphene.String(required=False)
    address = graphene.String(required=False)
    postal_code = graphene.String(required=False)
    city = graphene.String(required=False)
    floor_plan = Upload(required=False)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class UnitDelete(PermissionClassesMutationMixin, DeleteMutation):
  class Meta:
    model = Unit
    return_node = UnitNode

  class Input:
    id = graphene.ID(required=True)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class RoomUpsert(PermissionClassesMutationMixin, UpsertMutation):
  class Meta:
    model = Room
    return_node = RoomNode

  class Input:
    id = graphene.ID(required=False)
    unit = graphene.ID(required=False)
    title = graphene.String(required=False)
    image = Upload(required=False)
    capacity = graphene.Int(required=False)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class RoomDelete(PermissionClassesMutationMixin, DeleteMutation):
  class Meta:
    model = Room
    return_node = RoomNode

  class Input:
    id = graphene.ID(required=True)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class ActivityTimeUpsert(PermissionClassesMutationMixin, UpsertMutation):
  class Meta:
    model = ActivityTime
    return_node = ActivityTimeNode

  class Input:
    id = graphene.ID(required=False)
    title = graphene.String(required=False)
    start_time = graphene.DateTime(required=False)
    end_time = graphene.DateTime(required=False)
    room = graphene.ID(required=False)
    participants = graphene.List(graphene.ID)
    small_groups = graphene.List(graphene.ID)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class ActivityTimeDelete(PermissionClassesMutationMixin, DeleteMutation):
  class Meta:
    model = ActivityTime
    return_node = ActivityTimeNode

  class Input:
    id = graphene.ID(required=True)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class AssessmentUpsert(PermissionClassesMutationMixin, UpsertMutation):
  class Meta:
    model = Assessment
    return_node = AssessmentNode

  class Input:
    id = graphene.ID(required=False)
    of_child = graphene.ID(required=True)
    of_activity = graphene.ID(required=True)
    rating = graphene.Int(required=False)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class AssessmentDelete(PermissionClassesMutationMixin, DeleteMutation):
  class Meta:
    model = Assessment
    return_node = AssessmentNode

  class Input:
    id = graphene.ID(required=True)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class AssessmentQuestionUpsert(PermissionClassesMutationMixin, UpsertMutation):
  class Meta:
    model = AssessmentQuestion
    return_node = AssessmentQuestionNode

  class Input:
    id = graphene.ID(required=False)
    text = graphene.String(required=False)
    of = graphene.String(required=False)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class AssessmentQuestionDelete(PermissionClassesMutationMixin, DeleteMutation):
  class Meta:
    model = AssessmentQuestion
    return_node = AssessmentQuestionNode

  class Input:
    id = graphene.ID(required=True)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class AssessmentResponseUpsert(PermissionClassesMutationMixin, UpsertMutation):
  class Meta:
    model = AssessmentResponse
    return_node = AssessmentResponseNode

  class Input:
    id = graphene.ID(required=False)
    assessment = graphene.ID(required=False)
    question = graphene.ID(required=False)
    answer = graphene.String(required=False)
    of = graphene.String(required=False)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class AssessmentResponseDelete(PermissionClassesMutationMixin, DeleteMutation):
  class Meta:
    model = AssessmentResponse
    return_node = AssessmentResponseNode

  class Input:
    id = graphene.ID(required=False)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class TagUpsert(PermissionClassesMutationMixin, UpsertMutation):
  class Meta:
    model = Tag
    return_node = TagNode

  class Input:
    id = graphene.ID(required=False)
    title = graphene.String(required=False)
    category = graphene.String(required=False)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class TagDelete(PermissionClassesMutationMixin, DeleteMutation):
  class Meta:
    model = Tag
    return_node = TagNode

  class Input:
    id = graphene.ID(required=True)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class ProfileTagUpsert(PermissionClassesMutationMixin, UpsertMutation):
  class Meta:
    model = ProfileTag
    return_node = ProfileTagNode

  class Input:
    id = graphene.ID(required=False)
    profile = graphene.ID(required=False)
    tag = graphene.ID(required=False)
    removed_at = graphene.Date(required=False)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class ProfileTagDelete(PermissionClassesMutationMixin, DeleteMutation):
  class Meta:
    model = ProfileTag
    return_node = ProfileTagNode

  class Input:
    id = graphene.ID(required=True)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class SmallGroupUpsert(PermissionClassesMutationMixin, UpsertMutation):
  class Meta:
    model = SmallGroup
    return_node = SmallGroupNode

  class Input:
    id = graphene.ID(required=False)
    title = graphene.String(required=True)
    unit = graphene.ID(required=False)
    profiles = graphene.List(graphene.ID)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class SmallGroupDelete(PermissionClassesMutationMixin, DeleteMutation):
  class Meta:
    model = SmallGroup
    return_node = SmallGroupNode

  class Input:
    id = graphene.ID(required=True)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]


class Mutation(graphene.ObjectType):
  upsert_user = UserUpsert.Field()
  delete_user = UserDelete.Field()

  upsert_unit = UnitUpsert.Field()
  delete_unit = UnitDelete.Field()

  upsert_room = RoomUpsert.Field()
  delete_room = RoomDelete.Field()

  upsert_activity_time = ActivityTimeUpsert.Field()
  delete_activity_time = ActivityTimeDelete.Field()

  upsert_tag = TagUpsert.Field()
  delete_tag = TagDelete.Field()

  upsert_profile_tag = ProfileTagUpsert.Field()
  delete_profile_tag = ProfileTagDelete.Field()

  upsert_assessment = AssessmentUpsert.Field()
  delete_assessment = AssessmentDelete.Field()

  upsert_assessment_question = AssessmentQuestionUpsert.Field()
  delete_assessment_question = AssessmentQuestionDelete.Field()

  upsert_assessment_response = AssessmentResponseUpsert.Field()
  delete_assessment_response = AssessmentResponseDelete.Field()

  upsert_profile = ProfileUpsert.Field()
  delete_profile = ProfileDelete.Field()

  upsert_small_group = SmallGroupUpsert.Field()
  delete_small_group = SmallGroupDelete.Field()

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
