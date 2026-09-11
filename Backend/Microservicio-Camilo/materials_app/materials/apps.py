from django.apps import AppConfig  # Configuración estándar de app Django.


class MaterialsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "materials"
    verbose_name = "Materiales del Mercado"