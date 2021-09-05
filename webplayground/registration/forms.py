from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'link']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file mt-3'}),
            'bio': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows': 3, 'placeholder': 'Biografia'}),
            'link': forms.URLInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Enlace'}),
        }

class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text='Requerido, 254 caracterese como maximo y debe ser valido')

    class Meta:
        model = User
        fields = ['email']


    # Añadiendo una validacion, se ejecutara al recibir los valores desde el form
    # clean_<<name_field>>
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verifica si se cambio este campo, entonces si debe validarse
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                # Enviando la expecion de encontrar coincidencias
                raise forms.ValidationError('El email ya esta registrado, prueba con otro.')
        return email
