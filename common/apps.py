from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
    # UD3.4.d: Nombre visible de la aplicación en el administrador.
    verbose_name = 'Común'
