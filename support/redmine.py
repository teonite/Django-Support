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

__author__ = 'Krzysztof Krzysztofik'

log = logging.getLogger('apps.support')


class RedmineIssue(object):
    id = None
    project_id = None
    tracker_id = None
    status_id = None
    priority_id = None
    subject = ""
    description = ""
    category_id = None
    extra = None

    template_name = "default.html"

    def __init__(self, **kwargs):
        try:
            self.template_name = settings.ISSUE_TEMPLATE
        except AttributeError:
            pass

        defaults = settings.REDMINE_ISSUE_DEFAULTS
        for key, value in defaults.iteritems():
            setattr(self, key, value)

        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        ret_dict = {
            'issue': {
                'project_id': self.project_id,
                'tracker_id': self.tracker_id,
                'subject': self.subject,
                'description': self.description,
                'extra': self.extra,
            }
        }
        if self.category_id:
            ret_dict['issue']['category_id'] = self.category_id

        if self.status_id:
            ret_dict['issue']['status_id'] = self.status_id

        if self.priority_id:
            ret_dict['issue']['priority_id'] = self.priority_id

        return ret_dict

    def to_json(self, format_redmine=True):
        ret_dict = self.to_dict()

        if self.extra and format_redmine:
            context = {
                'description': self.description,
                'extra': self.extra,
            }

            template = get_template(self.template_name)
            context = Context(context)
            ret_dict['issue']['description'] = template.render(context)
            del(ret_dict['issue']['extra'])

        return json.dumps(ret_dict)

    def save(self, **kwargs):
        #TODO: RedmineIssue should behave like django.model object
        # if not self.id:

        return self


class BadMethodException(Exception):
    pass


def _add_auth_header(request):
    if len(settings.REDMINE_API_KEY):
        request.add_header("X-Redmine-API-Key", settings.REDMINE_API_KEY)
        return request

    base64string = base64.standard_b64encode(
        '%s:%s' % (settings.REDMINE_USER, settings.REDMINE_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    return request


def request_redmine(what, **kwargs):
    method = kwargs.pop('method', 'get').lower()
    data = kwargs.pop('data', None)

    if method not in ['get', 'post']:
        raise BadMethodException('Method not supported. Currently only "GET" and "POST" are supported')

    req_str = "%s/%s.json" % (settings.REDMINE_ADDRESS, what)

    if len(kwargs):
        req_str += '?'
        for key, value in kwargs.iteritems():
            req_str += "%s=%s&" % (key, value)

    log.debug("Request start.")
    log.debug("Request string: %s" % req_str)

    request = urllib2.Request(req_str)

    if method == 'post':
        request.data = data
        request.add_header('Content-Type', 'application/json')
        request.get_method = lambda: 'POST'

    request = _add_auth_header(request)
    open_request = urllib2.urlopen(request)
    if method == 'post':
        response_code = open_request.getcode()
        if response_code != 201:
            return {'response_code': response_code}

    json_str = open_request.readlines()

    log.debug("Request end.")
    json_str = ''.join(json_str)  # list -> str

    log.debug("Decoding JSON.")
    return json.loads(json_str)