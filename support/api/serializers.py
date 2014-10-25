#
# TEONITE Support - an application to submit a bug/features from your app/service to YouTrack/Redmine 
#
# Copyright (C) 2012-2014 TEONITE
#
import logging

from django.conf import settings

from rest_framework import serializers

from ..redmine import RedmineIssue
from ..youtrack import YouTrackIssue
from .fields import DictField

__author__ = 'kkrzysztofik'

log = logging.getLogger('apps.support')


class YouTrackIssueSerializer(serializers.Serializer):
    tracker_id = serializers.IntegerField(required=False)
    priority_id = serializers.IntegerField(required=False)
    subject = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)
    extra = DictField(required=False)

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            raise NotImplementedError
        try:
            if attrs['tracker_id'] == 2:
                attrs['type'] = 'Feature'
            else:
                attrs['type'] = 'Bug'
        except KeyError:
            attrs['type'] = 'Bug'


        #TODO: implement priority serializing

        return YouTrackIssue(**attrs)


class RedmineIssueSerializer(serializers.Serializer):
    tracker_id = serializers.IntegerField(required=False)
    priority_id = serializers.IntegerField(required=False)
    subject = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)
    category_id = serializers.IntegerField(required=False)
    extra = DictField(required=False)

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            raise NotImplementedError

        return RedmineIssue(**attrs)