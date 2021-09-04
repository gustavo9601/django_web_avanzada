from django import forms
from .models import Page


# Personalizando los fomularios generados automaticamente por django views class
class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        # Especificando que datos columnas del modelo se permitiran crear
        fields = ['title', 'content', 'order']
        # Configurando las clases que llevara cada input del form
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo'}),
            'content': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Orden'}),
        }
        # Configura las etiquetas que acompañaran los input
        labels = {
            'title': '',
            'content': 'Contenido HTML',
            'order': 'Orden'
        }
