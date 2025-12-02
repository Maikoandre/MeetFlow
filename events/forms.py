from django import forms
from django.contrib.auth.models import User
from .models import Inscricao, Usuario, Evento

class InscricaoEventoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = []
    
    def clean(self):
        pass

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'idade', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'data', 'local', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do evento'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço ou Link'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detalhes do evento...'}),
        }
        labels = {
            'titulo': 'Título do Evento',
            'local': 'Localização',
            'descricao': 'Descrição Completa',
            'data': 'Data do Evento'
        }

