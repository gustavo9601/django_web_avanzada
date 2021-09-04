from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from .forms import PageForm
from .models import Page


class StaffRequiredMixin(object):
    """
    Este mixin requerira que el usuario este autenticado y sea miembro del staff
    """

    # Metodo que se ejecuta en cada peticion
    # Se puede implementar un middlware o alguna logica pre
    # Las clases que la heredn se usara este metodo
    def dispatch(self, request, *args, **kwargs):
        # Si no esta autenticado se redireccionara
        if not request.user.is_staff:
            return redirect(reverse_lazy('admin:login'))
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


# Create your views here.
class PageListView(ListView):
    model = Page


class PageDetailView(DetailView):
    model = Page


class PageCreate(StaffRequiredMixin, CreateView):
    model = Page

    # Especificando la redireccion cuando se guarde en la bd
    # Forma 1
    """def get_success_url(self):
        return reverse('pages:pages')"""
    # Forma 2
    success_url = reverse_lazy('pages:pages')

    # Especificando la clase que configura el formulario a generar
    form_class = PageForm


class PageUpdate(StaffRequiredMixin, UpdateView):
    model = Page
    # Especifica el sufijo al final del nombre del archivo del html "page_update_form.html"
    template_name_suffix = '_update_form'
    # Especificando la clase que configura el formulario a generar
    form_class = PageForm

    def get_success_url(self):
        # Redireccionara a la URL pasando el parametro de ID
        # ?ok=True // concatena al final de la cadena, la url enviada
        return reverse_lazy('pages:update', args=[self.object.id]) + '?ok=True'


class PageDelete(StaffRequiredMixin, DeleteView):
    model = Page
    success_url = reverse_lazy('pages:pages')
