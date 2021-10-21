# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from django.conf.urls.static import static
from project import settings

urlpatterns = [
  path('', include('innolla.urls')),
  path('sysadmin/', admin.site.urls),
  path('monitor/', include('health_check.urls')),
  re_path(r'^api/graphiql', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, pretty=True))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Serve static and media files from Django
# Django will disable these automatically when DEBUG = False
urlpatterns += staticfiles_urlpatterns()

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
