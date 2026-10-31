"""
URL configuration for reservas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from common.views import PanelView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PanelView.as_view(),name='panel'),
    # UD3.7.b: Incorpora al proyecto las rutas de facturación y cobros.
    path('billing/', include('billing.urls')),
    # UD3.7.b: Incorpora las rutas de la aplicación de reservas.
    path('reservas/', include('core.urls')),

]


# UD3.2.e: Publica los archivos multimedia durante el desarrollo.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
