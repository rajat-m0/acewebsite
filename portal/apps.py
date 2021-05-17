from django.apps import AppConfig
from .drive import refresh_token
import redis
class PortalConfig(AppConfig):
    name = 'portal'

    def ready(self):
        # refresh_token.delay()
        pass