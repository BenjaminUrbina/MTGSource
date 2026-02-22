from django.apps import AppConfig


class AppmtgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appMTG'

    def ready(self):
        import appMTG.signals
