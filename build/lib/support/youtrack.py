#
# TEONITE Support - an application to submit a bug/features from your app/service to YouTrack/Redmine
#
# Copyright (C) 2012-2014 TEONITE
#

import urllib2
import base64
import json
import logging

from django.conf import settings
from django.template import Context
from django.template.loader import get_template

log = logging.getLogger('apps.support')


class YouTrackIssue(object):
    id = None
    project_id = None
    type = None
    status = None
    priority = None
    subject = ""
    description = ""
    subsystem = None

    template_name = "default.html"

    def __init__(self, **kwargs):
        try:
            self.template_name = settings.ISSUE_TEMPLATE
        except AttributeError:
            pass

        defaults = settings.YOUTRACK_ISSUE_DEFAULTS
        for key, value in defaults.iteritems():
            setattr(self, key, value)

        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)

    def __getattr__(self, item):
        if item == "tracker_id":
            return self.type

    def to_dict(self):
        ret_dict = {
            'issue': {
                'project_id': self.project_id,
                'type': self.type,
                'subject': self.subject,
                'description': self.description
            }
        }
        if self.subsystem:
            ret_dict['issue']['subsystem'] = self.subsystem

        if self.status:
            ret_dict['issue']['status'] = self.status

        if self.priority:
            ret_dict['issue']['priority'] = self.priority

        return ret_dict

    def save(self, **kwargs):
        #TODO: RedmineIssue should behave like django.model object
        # if not self.id:

        return self
