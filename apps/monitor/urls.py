#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.monitor.views',

    url(r'^index/$', 'index'),
    url(r'^edit/$', 'edit'),
    url('$', 'index'),
)
