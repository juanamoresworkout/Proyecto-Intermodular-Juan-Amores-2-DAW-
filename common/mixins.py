# messages permite crear avisos que se muestran en la siguiente plantilla.
from django.contrib import messages
# SuccessMessageMixin conserva el aviso hasta cargar la página de destino.
from django.contrib.messages.views import SuccessMessageMixin
# ProtectedError identifica exclusivamente un borrado bloqueado por PROTECT.
from django.db.models.deletion import ProtectedError
# HttpResponseRedirect envía al navegador a la URL indicada tras el intento.
from django.http import HttpResponseRedirect
# reverse_lazy transforma el nombre de una ruta en su dirección final.
from django.urls import reverse_lazy


# UD4.2.d: Comparte con la plantilla los textos y la URL de borrado.
class CreateUpdateContextMixin:
    # Cada vista concreta sustituye estos valores según su modelo y acción.
    titulo_creacion = None
    titulo_actualizacion = None
    url_borrado = None

    def get_context_data(self, **kwargs):
        # Conserva primero todo el contexto preparado por CreateView/UpdateView.
        context = super().get_context_data(**kwargs)
        # Añade los tres valores que consume base_create_update.html.
        context['titulo_creacion'] = self.titulo_creacion
        context['titulo_actualizacion'] = self.titulo_actualizacion
        context['url_borrado'] = self.url_borrado
        # Devuelve el contexto ampliado para que Django renderice la plantilla.
        return context


# UD4.4.a: Muestra un mensaje dinámico y vuelve al objeto guardado.
class CreateUpdateSuccessMixin(SuccessMessageMixin):
    # Cada vista concreta indica su ruta de actualización y el texto adecuado.
    success_url_name = None
    success_message = None

    def get_success_url(self):
        # self.object es el objeto que CreateView o UpdateView acaba de guardar.
        return reverse_lazy(
            self.success_url_name,
            kwargs={'pk': self.object.pk},
        )

    def get_success_message(self, cleaned_data):
        # Inserta la representación textual real dentro del mensaje de la vista.
        return self.success_message.format(
            object=self.object,
        )


# UD4.2.e: Comparte con la plantilla los textos de confirmación de borrado.
class DeleteContextMixin:
    # La vista concreta define los textos apropiados para su modelo.
    titulo = None
    mensaje_confirmacion = None

    def get_context_data(self, **kwargs):
        # Recupera el contexto y el objeto que DeleteView ya ha localizado.
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.titulo
        # Sustituye {object} por la representación textual del objeto real.
        context['mensaje_confirmacion'] = (
            self.mensaje_confirmacion.format(object=self.object)
        )
        return context


# UD4.2.f: Impide eliminar objetos con dependencias e informa del motivo.
class ProtectedDeleteMixin:
    def form_valid(self, form):
        # Deja que DeleteView intente realizar el borrado normal.
        try:
            return super().form_valid(form)
        # Si una relación PROTECT lo impide, conserva todos los registros.
        except ProtectedError:
            # Incluye el objeto concreto en el aviso que se mostrará en rojo.
            messages.error(
                self.request,
                'Existen dependencias para el objeto {}. '
                'Elimine antes dichas dependencias.'.format(self.object),
            )
            # Vuelve al listado configurado como success_url en la vista.
            return HttpResponseRedirect(self.get_success_url())


# UD4.2.i: Ordena los listados por identificador según la URL.
class OrderingMixin:
    def get_queryset(self):
        # Parte del queryset normal para conservar filtros y comportamiento base.
        queryset = super().get_queryset()
        # Lee ordering de la consulta, por ejemplo ?ordering=asc.
        ordering = self.request.GET.get('ordering')

        # id ordena de menor a mayor cuando el valor permitido es asc.
        if ordering == 'asc':
            return queryset.order_by('id')

        # El prefijo - invierte la ordenación cuando se solicita desc.
        if ordering == 'desc':
            return queryset.order_by('-id')

        # Sin un valor válido mantiene la ordenación definida en el modelo.
        return queryset
