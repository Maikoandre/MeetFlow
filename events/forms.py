from django import forms
from django.contrib.auth.models import User
from .models import Inscricao, Usuario

class InscricaoEventoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = []
    
    def clean(self):
        # Validação extra: verificar se já existe inscrição pode ser feito aqui ou na View
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