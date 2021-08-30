from django.shortcuts import render

from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = "core/home.html"

    # Metodo que permite retornar el contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi super Web GM'
        return context


class SamplePageView(TemplateView):
    template_name = "core/sample.html"

    # Sobreescribiendo la respuesta del la vista basada en clase
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name, context={'title': 'Samplee'})
