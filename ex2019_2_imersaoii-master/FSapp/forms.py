from .models import Imersionista, Evento
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.forms import ModelForm
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

class ImersionistaForm(forms.ModelForm):
    class Meta:
        model = Imersionista
        fields = ['matricula', 'first_name','last_name','cpf','email', 'curso','periodo', 'anexo_1', 'anexo_2', 'anexo_3']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['matricula'].widget.attrs.update({'placeholder': 'Matrícula'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Primeiro Nome'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Sobrenome'})
        self.fields['cpf'].widget.attrs.update({'placeholder': 'CPF'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})






class LoginVeterano(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Imersionista
        fields = ('matricula', 'password')

    def clean(self):
        if self.is_valid():
            matricula = self.cleaned_data['matricula']
            password = self.cleaned_data['password']
            if not authenticate(matricula=matricula, password=password):
                raise forms.ValidationError('Dados Inválidos')


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['workshop']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['workshop'].widget.attrs.update({'placeholder': 'Data de Inicio do Workshop'})


class EscolherAreaForm(forms.ModelForm):
    class Meta:
        model = Imersionista
        fields = ['areadeinteresse']


