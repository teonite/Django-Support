#
# TEONITE Support - an application to submit a bug/features from your app/service to YouTrack/Redmine 
#
# Copyright (C) 2012-2014 TEONITE
#
import logging

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from rest_framework.compat import six
from rest_framework.fields import WritableField
from rest_framework.serializers import NestedValidationError

#from: https://github.com/estebistec/drf-compound-fields/blob/master/drf_compound_fields/fields.py
#Copyright (c) 2014, Steven Cummings
#All rights reserved.

log = logging.getLogger('apps.support')


class DictField(WritableField):
    """
    A field whose values are dicts of values described by the given value field. The value field
    can be another field type (e.g., CharField) or a serializer.
    """

    default_error_messages = {
        'invalid_type': _('%(value)s is not a dict'),
    }
    default_unicode_options = {}
    empty = {}

    def __init__(self, value_field=None, unicode_options=None, *args, **kwargs):
        super(DictField, self).__init__(*args, **kwargs)
        self.value_field = value_field
        self.unicode_options = unicode_options or self.default_unicode_options

    def to_native(self, obj):
        if self.value_field and obj:
            return dict(
                (six.text_type(key, **self.unicode_options), self.value_field.to_native(value))
                for key, value in obj.items()
            )
        return obj

    def from_native(self, data):
        self.validate_is_dict(data)
        if self.value_field and data:
            return dict(
                (six.text_type(key, **self.unicode_options), self.value_field.from_native(value))
                for key, value in data.items()
            )
        return data

    def validate(self, value):
        super(DictField, self).validate(value)

        self.validate_is_dict(value)

        if self.value_field:
            errors = {}
            for k, v in six.iteritems(value):
                try:
                    self.value_field.run_validators(v)
                    self.value_field.validate(v)
                except ValidationError as e:
                    errors[k] = e.messages

            if errors:
                raise NestedValidationError(errors)

    def validate_is_dict(self, value):
        log.error(type(value))
        if not isinstance(value, dict):
            raise ValidationError(
                self.error_messages['invalid_type'],
                code='invalid_type',
                params={'value': value}
            )