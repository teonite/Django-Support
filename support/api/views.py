#
# TEONITE Support - an application to submit a bug/features from your app/service to YouTrack/Redmine 
#
# Copyright (C) 2012-2014 TEONITE
#
import logging
import urllib2
from collections import OrderedDict

from django.http.request import QueryDict
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

from ipware import ip

from youtrack.connection import Connection as YTConnection

from rest_framework.response import Response
from rest_framework import status, permissions, generics, mixins

from .serializers import RedmineIssueSerializer, YouTrackIssueSerializer
from ..redmine import request_redmine

__author__ = 'kkrzysztofik'

log = logging.getLogger('apps.support')


class NewIssueView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RedmineIssueSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer_class()

        log.debug(type(request.DATA))
        if isinstance(request.DATA, QueryDict):
            data = request.DATA.dict()
            new_extra = OrderedDict()
            to_del = []
            for key, value in data.iteritems():
                if key.startswith('extra') and not key.endswith('extra'):
                    log.debug(key)
                    new_key = key.split('[')[1][:-1]
                    new_extra[new_key] = value
                    to_del.append(key)

            for element in to_del:
                del (data[element])

            user = request.user

            if not 'user' in new_extra:
                new_extra['user'] = u"%s (%s) - %s" % (user.username, user.get_full_name(), user.email)
            if not 'user-agent' in new_extra:
                new_extra['user-agent'] = request.META.get('HTTP_USER_AGENT', None)
            if not 'referer' in new_extra:
                new_extra['referer'] = request.META.get('HTTP_REFERER', None)
            if not 'ip' in new_extra:
                new_extra['ip'] = ip.get_ip(request)
            if not 'tenant' in new_extra:
                new_extra['tenant'] = request.META.get('HTTP_HOST', None)

            data['extra'] = new_extra
        elif isinstance(request.DATA, dict):
            data = request.DATA

            try:
                extra = data['extra']
            except KeyError:
                extra = {}

            new_extra = OrderedDict(extra)
            user = request.user

            if not 'user' in new_extra:
                new_extra['user'] = u"%s (%s) - %s" % (user.username, user.get_full_name(), user.email)
            if not 'user-agent' in new_extra:
                new_extra['user-agent'] = request.META.get('HTTP_USER_AGENT', None)
            if not 'referer' in new_extra:
                new_extra['referer'] = request.META.get('HTTP_REFERER', None)
            if not 'ip' in new_extra:
                new_extra['ip'] = ip.get_ip(request)
            if not 'tenant' in new_extra:
                new_extra['tenant'] = request.META.get('HTTP_HOST', None)

            data['extra'] = new_extra
        else:
            data = request.DATA

        log.debug(data)
        try:
            if len(settings.REDMINE_ADDRESS):
                serializer = serializer(data=data)

                if serializer.is_valid():
                    obj = serializer.save()
                    try:
                        ret = request_redmine('issues', data=obj.to_json(), method='POST')
                    except urllib2.HTTPError as ex:
                        log.debug("HTTPError")
                        return Response(data={'code': ex.code, 'message': ex.reason},
                                        status=status.HTTP_400_BAD_REQUEST)
                    except urllib2.URLError as ex:
                        log.debug("URLError")
                        return Response(data={'reason': ex.reason[1]},
                                        status=status.HTTP_400_BAD_REQUEST)
                    log.debug(ret)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    log.debug("Serializer is invalid")
            else:
                log.debug("No redmine address")
        except AttributeError:
            log.debug("Redmine address not set.")

        try:
            if len(settings.YOUTRACK_ADDRESS):
                log.debug("YouTrack address is set")

                conn = YTConnection(settings.YOUTRACK_ADDRESS, settings.YOUTRACK_USER, settings.YOUTRACK_PASSWORD)
                serializer = YouTrackIssueSerializer(data=data)

                if serializer.is_valid():
                    obj = serializer.save()

                    if obj.extra:
                        context = {
                            'description': obj.description,
                            'extra': obj.extra,
                        }

                        template = get_template(obj.template_name)
                        context = Context(context)
                        description = template.render(context)
                    else:
                        description = obj.description

                    ret = conn.createIssue(obj.project_id, assignee=None, summary=obj.subject,
                                           description=description,
                                           priority=obj.priority, type=obj.type, subsystem=obj.subsystem)

                    log.debug(ret)
                    ret_dict = obj.to_dict()
                    try:
                        del(ret_dict['project_id'])
                    except KeyError:
                        pass

                    return Response(ret_dict, status=status.HTTP_201_CREATED)

        except AttributeError:
            log.debug("YouTrack address not set.")


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)