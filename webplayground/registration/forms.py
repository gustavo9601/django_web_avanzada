from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido, 254 caracterese como maximo y debe ser valido')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # Añadiendo una validacion, se ejecutara al recibir los valores desde el form
    # clean_<<name_field>>
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            # Enviando la expecion de encontrar coincidencias
            raise forms.ValidationError('El email ya esta registrado, prueba con otro.')
        return email
