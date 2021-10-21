
# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#

from django.contrib import admin
from innolla.models import Unit, Resource, Room, ActivityTime, Tag, Profile, Assessment, AssessmentQuestion, AssessmentResponse, ProfileTag, SmallGroup


class SysAdminSite(admin.AdminSite):

  def has_permission(self, request):
    return request.user.is_active and request.user.is_staff and request.user.is_superuser

site = SysAdminSite()


class UnitAdmin(admin.ModelAdmin):
  pass


class ResourceAdmin(admin.ModelAdmin):
  pass


class RoomAdmin(admin.ModelAdmin):
  pass


class AssessmentAdmin(admin.ModelAdmin):
  pass


class AssessmentQuestionAdmin(admin.ModelAdmin):
  pass


class AssessmentResponseAdmin(admin.ModelAdmin):
  pass


class ActivityTimeAdmin(admin.ModelAdmin):
  pass


class TagAdmin(admin.ModelAdmin):
  list_display = ('title',)
  # list_filter = ('title', )
  search_fields = ('title', )


class ProfileTagInline(admin.TabularInline):
  model = ProfileTag


class ProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'unit',)
  list_filter = ('unit', )
  search_fields = ('user', )
  inlines = [
    ProfileTagInline,
  ]


class SmallGroupAdmin(admin.ModelAdmin):
  pass


admin.site.register(Unit, UnitAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(AssessmentQuestion, AssessmentQuestionAdmin)
admin.site.register(AssessmentResponse, AssessmentResponseAdmin)
admin.site.register(ActivityTime, ActivityTimeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(SmallGroup, SmallGroupAdmin)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
