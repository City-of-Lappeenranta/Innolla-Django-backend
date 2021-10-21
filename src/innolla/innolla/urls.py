
# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from innolla.views import IndexView

urlpatterns = [
  url(r'^$', login_required()(IndexView.as_view()),
    name='innolla_index'),
]


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
