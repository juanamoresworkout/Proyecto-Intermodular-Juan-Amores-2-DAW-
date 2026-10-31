from django.shortcuts import render
from django.views.generic import TemplateView


# UD3.7.a: Muestra el panel principal de la aplicación.
class PanelView(TemplateView):
    template_name = 'common/panel.html'