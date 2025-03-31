from django.apps import AppConfig


class MainConfig(AppConfig):
    """Configuration class for the 'main' Django application.

    This class sets the default auto field and the application name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"
