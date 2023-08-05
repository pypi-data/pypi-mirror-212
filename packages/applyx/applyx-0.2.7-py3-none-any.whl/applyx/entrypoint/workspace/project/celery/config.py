# coding=utf-8

import os

from applyx.conf import settings
settings.from_yaml(os.path.join(__file__, '../../conf/settings.yaml'))


enable_utc = settings.get('celery.utc')
timezone = settings.get('celery.timezone')
broker_url = settings.get('celery.broker.url')
