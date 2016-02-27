# -*- coding:utf-8 -*-
from __future__ import absolute_import

import os

from django.conf import settings
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sohu.settings')

app = Celery('sohu')

app.config_from_object('django.conf:settings')
# load task modules from all import registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
