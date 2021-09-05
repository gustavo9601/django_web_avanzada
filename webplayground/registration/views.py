from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django import forms
from django.urls import reverse_lazy
from .forms import UserCreationFormWithEmail

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
