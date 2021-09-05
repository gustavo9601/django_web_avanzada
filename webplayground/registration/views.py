from .models import Profile

from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, TemplateView
from django.views.generic.edit import UpdateView
from django import forms
from django.urls import reverse_lazy
from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class SignUpView(CreateView):
    # Usamos nuestra propia clase adicionando el campo de email
    form_class = UserCreationFormWithEmail
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        # Modificar el objeto de form heredado del padre propio django
        form.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Nombre usuario'})
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Direccion de correo electronico'})
        form.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Repite contraseña'})
        # Labels
        form.fields['username'].label = ''
        form.fields['email'].label = ''
        form.fields['password1'].label = ''
        form.fields['password2'].label = ''

        return form


# Requiere de login
@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        # Recupera el modelo que se va a editar y de no existir lo crea
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


# Requiere de login
@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        # Recupera el modelo que se va a editar y de no existir lo crea
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        # Modificar el objeto de form heredado del padre propio django
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Direccion de correo electronico'})
        return form
