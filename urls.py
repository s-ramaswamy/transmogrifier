#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

from transmogrifier.settings import MEDIA_ROOT
from messportal import urls

admin.autodiscover()

urlpatterns = patterns('', url(r'^media/(?P<path>.*)$',
                       'django.views.static.serve',
                       {'document_root': MEDIA_ROOT}), url(r'^admin/',
                       include(admin.site.urls)), url(r'^',
                       include('transmogrifier.messportal.urls')))

