from django.apps import AppConfig


class ChatV1Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chat_v1"

    def ready(self):
        from .scheduler import scheduler
        scheduler.start()
