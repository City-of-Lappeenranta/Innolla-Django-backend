
# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#

import logging
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

LOG = logging.getLogger(__name__)


class TimestampedModel(models.Model):
  created_at = models.DateTimeField(editable=False, default=timezone.now)
  updated_at = models.DateTimeField(editable=False, auto_now=True)

  class Meta:
    abstract = True


class Unit(models.Model):
  title = models.CharField(max_length=50)
  address = models.CharField(max_length=50)
  postal_code = models.CharField(max_length=5)
  city = models.CharField(max_length=15)
  floor_plan = models.ImageField()

  def __str__(self):
    return f'{self.title}'


class ProfileTag(models.Model):
  tag = models.ForeignKey('innolla.Tag', on_delete=models.CASCADE)
  profile = models.ForeignKey('innolla.Profile', on_delete=models.CASCADE)
  created_at = models.DateField(auto_now=True)
  removed_at = models.DateField(null=True, blank=True)


class Tag(models.Model):
  SKILLS = 'skills'
  POINT_OF_INTERESTS = 'point_of_interests'
  DEVELOPMENT_TARGET = 'development_target'
  OTHER = 'other'

  TAG_CATEGORY_CHOICES = [
    (SKILLS, _('skills')),
    (POINT_OF_INTERESTS, _('point of interests')),
    (DEVELOPMENT_TARGET, _('development target')),
    (OTHER, _('other')),
  ]

  title = models.CharField(max_length=200)
  category = models.CharField(choices=TAG_CATEGORY_CHOICES, max_length=200)

  def __str__(self):
    return self.title


class Profile(models.Model):
  user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
  unit = models.ForeignKey('innolla.Unit', related_name='unit_members', null=True, on_delete=models.CASCADE)
  tags = models.ManyToManyField('innolla.Tag', through=ProfileTag, blank=True)
  picture = models.ImageField(null=True, blank=True)


class SmallGroup(models.Model):
  title = models.CharField(max_length=1000)
  unit = models.ForeignKey('innolla.Unit', related_name='groups', null=True, blank=True, on_delete=models.CASCADE)
  profiles = models.ManyToManyField('innolla.Profile', related_name='groups', blank=True)


class Resource(models.Model):
  title = models.CharField(max_length=100, help_text=_('Resource name'))
  count = models.PositiveIntegerField(help_text=_('Resource count'))
  room = models.ForeignKey('innolla.Room', related_name='resources', on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.title}'


class Room(models.Model):
  title = models.CharField(max_length=50)
  unit = models.ForeignKey(Unit, related_name='rooms', on_delete=models.CASCADE)
  image = models.ImageField()
  capacity = models.PositiveIntegerField(help_text=_('Suitable group size for this room'))

  class Meta:
    permissions = [
      ('view_reservable_room', _('Can view reservable room')),
    ]

  def __str__(self):
    return f'{self.unit}, {self.title}'


class ActivitytimeTags(models.Model):
  tag = models.ForeignKey('innolla.Tag', on_delete=models.CASCADE)
  activitytime = models.ForeignKey('innolla.ActivityTime', on_delete=models.CASCADE)
  created_at = models.DateField(auto_now=True)
  removed_at = models.DateField(null=True, default=None)


class ActivityTime(TimestampedModel):
  start_time = models.DateTimeField(null=True, blank=True)
  end_time = models.DateTimeField(null=True, blank=True)
  title = models.CharField(max_length=200, null=False, blank=False)
  participants = models.ManyToManyField(Profile, related_name='activities', blank=True, help_text=_('Activitytime\'s participants'))
  small_groups = models.ManyToManyField(SmallGroup, related_name='activities', blank=True, help_text=_('Activitytime\'s small groups'))
  room = models.ForeignKey(Room, related_name='activities', on_delete=models.CASCADE, null=True, blank=True)
  tags = models.ManyToManyField('innolla.Tag', through=ActivitytimeTags, blank=True)

  def __str__(self):
    if self.room:
      return f'{self.title}, {self.room.title}'
    return f'{self.title}'


class Assessment(TimestampedModel):
  of_child = models.ForeignKey(Profile, related_name='assessments', null=True, blank=False, on_delete=models.SET_NULL)
  of_activity = models.ForeignKey(ActivityTime, related_name='assessments', null=True, blank=False, on_delete=models.SET_NULL)
  rating = models.IntegerField(
    null=True,
    validators=[
      MaxValueValidator(7),
      MinValueValidator(1)
  ])

  class Meta:
    unique_together = ('of_child', 'of_activity')


class AssessmentQuestion(models.Model):
  CHILD = 'child'
  ADULT = 'adult'
  ACTIVITY = 'activity'

  OF_CHOICES = [
    (CHILD, _('child')),
    (ADULT, _('adult')),
    (ACTIVITY, _('activity')),
  ]

  of = models.CharField(choices=OF_CHOICES, max_length=100, default=CHILD)
  text = models.CharField(max_length=5000, null=False, blank=False)


class AssessmentResponse(models.Model):
  CHILD = 'child'
  ADULT = 'adult'
  ACTIVITY = 'activity'

  OF_CHOICES = [
    (CHILD, _('child')),
    (ADULT, _('adult')),
    (ACTIVITY, _('activity')),
  ]

  assessment = models.ForeignKey(Assessment, related_name='responses', null=False, blank=False, on_delete=models.CASCADE)
  question = models.ForeignKey(AssessmentQuestion, related_name='responses', null=True, blank=False, on_delete=models.SET_NULL)
  answer = models.CharField(max_length=5000, null=False, blank=False)
  of = models.CharField(choices=OF_CHOICES, max_length=100, default=CHILD)

  class Meta:
    unique_together = ('assessment', 'question', 'of')



# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
