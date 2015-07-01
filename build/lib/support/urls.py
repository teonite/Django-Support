#
# TEONITE Support - an application to submit a bug/features from your app/service to YouTrack/Redmine
#
# Copyright (C) 2012-2014 TEONITE
#
from django.conf.urls import patterns, url

from .api.views import NewIssueView

urlpatterns = patterns('',
    url(r'^issues', NewIssueView.as_view()),
)
