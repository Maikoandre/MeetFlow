from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EventoForm, InscricaoEventoForm, UsuarioForm
from .models import Evento, Inscricao, Usuario


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

@login_required
def editar_perfil(request):
    perfil, created = Usuario.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('index')
    else:
        form = UsuarioForm(instance=perfil)
    
    return render(request, 'forms/usuario_editar.html', {'form': form})

@login_required
def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
        
    return render(request, 'forms/usuario_senha.html', {'form': form})

def detalhes_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    ja_inscrito = False
    if request.user.is_authenticated:
        ja_inscrito = Inscricao.objects.filter(evento=evento, participante=request.user).exists()

    return render(request, 'detalhes_evento.html', {
        'evento': evento,
        'ja_inscrito': ja_inscrito
    })

@login_required
def gerenciar_eventos(request):
    eventos = Evento.objects.filter(organizador=request.user)
    return render(request, 'gestao/gerenciar_eventos.html', {'eventos': eventos})

@login_required
def criar_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user
            evento.save()
            messages.success(request, 'Evento criado com sucesso!')
            return redirect('gerenciar_eventos')
    else:
        form = EventoForm()
    return render(request, 'gestao/evento_form.html', {'form': form, 'titulo': 'Criar Evento'})

@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento atualizado!')
            return redirect('gerenciar_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'gestao/evento_form.html', {'form': form, 'titulo': 'Editar Evento'})

@login_required
def deletar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento cancelado/excluído com sucesso.')
        return redirect('gerenciar_eventos')
    return render(request, 'gestao/evento_confirmar_delete.html', {'evento': evento})

@login_required
def ver_inscritos(request, pk):
    evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
    inscricoes = evento.inscricoes.all()
    return render(request, 'gestao/ver_inscritos.html', {'evento': evento, 'inscricoes': inscricoes})

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'usuario') and user.usuario.tipo == 'admin')

@login_required
@user_passes_test(is_admin)
def relatorio_admin(request):
    total_eventos = Evento.objects.count()
    total_usuarios = Usuario.objects.count()
    total_inscricoes = Inscricao.objects.count()
    status_counts = Inscricao.objects.values('status').annotate(total=Count('status'))
    
    top_eventos = Evento.objects.annotate(
        num_inscritos=Count('inscricoes')
    ).order_by('-num_inscritos')[:5]

    context = {
        'total_eventos': total_eventos,
        'total_usuarios': total_usuarios,
        'total_inscricoes': total_inscricoes,
        'status_counts': status_counts,
        'top_eventos': top_eventos,
    }
    return render(request, 'gestao/relatorio_admin.html', context)