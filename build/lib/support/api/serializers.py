#
# TEONITE Support - an application to submit a bug/features from your app/service to YouTrack/Redmine
#
# Copyright (C) 2012-2014 TEONITE
#
from django.conf import settings

from rest_framework import serializers

from ..redmine import RedmineIssue
from ..youtrack import YouTrackIssue

__author__ = 'kkrzysztofik'


class YouTrackIssueSerializer(serializers.Serializer):
    tracker_id = serializers.IntegerField(required=False)
    priority_id = serializers.IntegerField(required=False)
    subject = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        return YouTrackIssue(**validated_data)


class RedmineIssueSerializer(serializers.Serializer):
    tracker_id = serializers.IntegerField(required=False)
    priority_id = serializers.IntegerField(required=False)
    subject = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)
    category_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return RedmineIssue(**validated_data)
