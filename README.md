Django-Support
==============

Backend for TEONITE Angular Support - an application to submit bug/features from your app/service to YouTrack/Redmine

Installation steps
==================

# Add required applications to your django apps

 In single schema application::

```
        INSTALLED_APPS = (
            'apps.support',
        )
```

 In django tenant schemas application::

```
        SHARED_APPS = (
            'apps.support',
        )
```

# Add necessary settings to your config file:

YouTrack:

```
    YOUTRACK_ADDRESS = ''         # URL to your YouTrack instance
    YOUTRACK_USER = ''
    YOUTRACK_PASSWORD = ''
    YOUTRACK_ISSUE_DEFAULTS = {   # Define to which project submit issues
        'project_id': 'tst',
        'subsystem': None,
        'status': None,
        'priority' : None,
        'type': None,
    }
```

Redmine:

```
    REDMINE_ADDRESS = ''          # URL to your Redmine instance
    REDMINE_API_KEY = ''          # API key to your redmine
    REDMINE_ISSUE_DEFAULTS = {    # Define to which project submit issues
        'project_id': 1,
        'tracker_id': None, # None for Redmine/YT defaults
        'status_id': None,  # None for Redmine/YT defaults
        'priority_id': None,  # None for Redmine/YT defaults
    }

	# If you are not using TEONITE Angular Support and would like to render templates using Django
	# please provide path to the tempalte
    ISSUE_TEMPLATE = 'default.html'
```

# Add to yours urls.py:

```
    urlpatterns += patterns('',
        url(r'^api/', include('apps.support.urls')),
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    )
```

# Configure logging:

```
    LOGGING = {
        'loggers': {
            'apps.support': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }
```

Usage
=====
Use api view located default at: ``api/issues/``

- types supported by default:

    "application/json",
    "application/x-www-form-urlencoded",
    "multipart/form-data"

- mandatory fields:
    * ``title``
    * ``description``

- optional fields:
    * ``tracker_id`` - trackers are e.g. ``Bug``, ``Feature``, default for console: ``Bug, id=1``
    * ``priority_id`` - default for console: ``Normal, id=4``
    * ``category_id``
    * ``extra``

Extra field
===========
This field is used to provide extra info, which should be appended to description field. It accepts dictionaries eg.::

    {
        "ip": "127.0.0.1",
        "browser": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
    }

Available values for Console:
=============================

```
    "issue_priorities": [
            {
                "id": 3,
                "name": "Low"
            },
            {
                "id": 4,
                "is_default": true,
                "name": "Normal"
            },
            {
                "id": 5,
                "name": "High"
            },
            {
                "id": 6,
                "name": "Urgent"
            },
            {
                "id": 7,
                "name": "Immediate"
            }
    ],

    "trackers": [
            {
                "id": 1,
                "name": "Bug"
            },
            {
                "id": 2,
                "name": "Feature"
            },
            {
                "id": 3,
                "name": "Support"
            },
            {
                "id": 5,
                "name": "Test"
            },
            {
                "id": 4,
                "name": "Refactoring"
            }
    ]
```

Default description template
============================
::

    {{ description }}

    Additional information: {% for key, value in extra.items %}
        - {{ key }} : {{ value }}{% endfor %}

