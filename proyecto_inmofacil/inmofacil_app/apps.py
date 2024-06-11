from django.apps import AppConfig


class InmofacilAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inmofacil_app'

    def ready(self):
        import inmofacil_app.signals
