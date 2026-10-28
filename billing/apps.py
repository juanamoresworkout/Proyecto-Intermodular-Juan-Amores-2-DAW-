from django.apps import AppConfig


class BillingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'billing'
    # UD3.4.d: Nombre visible de la aplicación en el administrador.
    verbose_name = 'Facturación y cobros'
