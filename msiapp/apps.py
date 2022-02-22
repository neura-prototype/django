from django.apps import AppConfig


class MsiappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'msiapp'

    def ready(self):
        import msiapp.signals
