from django.apps import AppConfig


class QueueAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'queue_app'

class QueueAppConfig(AppConfig):
    def ready(self):
        import queue_app.signals
