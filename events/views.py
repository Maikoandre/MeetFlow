from django.shortcuts import render,  redirect, get_object_or_404
from .models import Evento
from .forms import InscricaoEventoForm

def index(request):
    return render(request, 'index.html')

def inscrever_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    
    if request.method == 'POST':
        form = InscricaoEventoForm(request.POST)
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.participante = request.user
            inscricao.evento = evento
            inscricao.save()
            return redirect('detalhes_evento', pk=evento.id)
    else:
        form = InscricaoEventoForm()

    return render(request, 'forms/evento_inscricao.html', {'form': form, 'evento': evento})

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import UsuarioForm

def cadastro_usuario(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        perfil_form = UsuarioForm(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save()
            
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()

            login(request, user)
            return redirect('index')
    else:
        user_form = UserCreationForm()
        perfil_form = UsuarioForm()

    return render(request, 'forms/usuario_cadastro.html', {
        'user_form': user_form,
        'form': perfil_form
    })