# coding=utf-8

import os

from applyx.conf import settings
settings.from_yaml(os.path.join(__file__, '../../conf/settings.yaml'))

from applyx.celery.base import setup_signals
setup_signals()

enable_utc = settings.get('celery.utc')
timezone = settings.get('celery.timezone')
broker_url = settings.get('celery.broker.url')
result_backend = settings.get('celery.result.backend')
result_expires = settings.get('celery.result.expires')
result_persistent = settings.get('celery.result.persistent')


imports = [
    "project.celery.tasks.demo",
]
