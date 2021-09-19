import redis
from django.apps import AppConfig

from .drive import refresh_token


class PortalConfig(AppConfig):
    name = "portal"

    def ready(self):
        # refresh_token.delay()
        pass
