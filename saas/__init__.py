# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from __future__ import absolute_import, unicode_literals
from saas.celery import app as celery_app  # noqa

__all__ = ("celery_app",)
