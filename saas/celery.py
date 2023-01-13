# Stdlib Imports
from __future__ import absolute_import, unicode_literals
import os

# Celery Imports
from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas.settings")

app = Celery("saas")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Beat schedules
app.conf.beat_schedule = {
    "monitor_websites": {
        "task": "apps.monitor.tasks.monitor_websites_up_x_downtimes",
        "schedule": crontab(minute="*/2"),
    },
}
