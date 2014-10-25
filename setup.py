#
# TEONITE Support - an application to submit a bug/features from your app/service to YouTrack/Redmine 
#
# Copyright (C) 2012-2014 TEONITE
#
from setuptools import setup

__version__ = "1.0.9"

readme = []
with open('README.rst', 'r') as fh:
    readme = fh.readlines()

setup(
    name='django-support',
    version=__version__,
    author='TEONITE',
    author_email='kkrzysztofik@teonite.com',
    packages=['support', 'support.api'],
    url='http://teonite.com/',
    description='django-support is an app that provide api method to add new issue to Redmine/YouTrack issue tracker',
    long_description='\n'.join(readme),
    license='Proprietary',
    include_package_data=True,
    install_requires=[
        "Django >= 1.5.0",
        "djangorestframework >= 2.3.0",
        "YouTrack-Python >= 1.0.6",
        "django-ipware >= 0.0.8"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Other/Proprietary License",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: Python :: 2.7"
    ]
)
