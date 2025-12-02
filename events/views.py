from django.shortcuts import render,  redirect, get_object_or_404
from .models import Evento, Usuario, Inscricao
from .forms import InscricaoEventoForm, EventoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EventoForm, InscricaoEventoForm, UsuarioForm
from .models import Evento, Inscricao, Usuario, Presenca

def index(request):
    if request.user.is_authenticated:
        try:
            return dashboard(request)
        except Exception:
            return render(request, 'index.html')
            
    return render(request, 'index.html')


@login_required
def dashboard(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    context = {
        'perfil': usuario,    # ← você usa isso no HTML
        'tipo': usuario.tipo, # ← ESSENCIAL
    }

    if usuario.tipo == 'admin':
        context.update({
            'total_eventos': Evento.objects.count(),
            'total_usuarios': Usuario.objects.count(),
            'eventos_pendentes': Evento.objects.filter(aprovado=False).count(),
            # Prepara lista de pendentes com nome seguro do organizador para evitar
            # RelatedObjectDoesNotExist ao acessar `organizador.usuario` no template.
            'lista_pendentes': Evento.objects.filter(aprovado=False).select_related('organizador'),
            'lista_a_publicar': Evento.objects.filter(aprovado=True, publicado=False).select_related('organizador'),
            'lista_publicados': Evento.objects.filter(publicado=True).select_related('organizador'),
        })
        # Adiciona atributo organizador_nome para cada evento (fallback para username)
        for ev in context['lista_pendentes']:
            try:
                ev.organizador_nome = ev.organizador.usuario.nome
            except Exception:
                ev.organizador_nome = getattr(ev.organizador, 'username', 'Organizador')

    elif usuario.tipo == 'organizador':
        meus_eventos = Evento.objects.filter(organizador=request.user)
        context.update({
            'meus_eventos': meus_eventos,
            'meus_eventos_count': meus_eventos.count(),
            'total_inscritos': Inscricao.objects.filter(evento__organizador=request.user).count(),
        })

    else:
        inscricoes = Inscricao.objects.filter(participante=request.user).select_related('evento')
        context.update({
            'minhas_inscricoes': inscricoes,
            'total_inscricoes': inscricoes.count(),
            'eventos_confirmados': inscricoes.filter(status='confirmado').count(),
        })

    return render(request, 'dashboard_users.html', context)




def eventos_lista(request):
    eventos = Evento.objects.filter(publicado=True, aprovado=True)

    is_participante = False
    if request.user.is_authenticated:
        is_participante = request.user.groups.filter(name="participantes").exists()

    return render(
        request,
        'events.html',
        {
            'eventos': eventos,
            'is_participante': is_participante
        }
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    return render(request, 'pages/samples/login.html', {'form': form})

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

def detalhes_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    ja_inscrito = False
    if request.user.is_authenticated:
        ja_inscrito = Inscricao.objects.filter(evento=evento, participante=request.user).exists()

    return render(request, 'detalhes_evento.html', {
        'evento': evento,
        'ja_inscrito': ja_inscrito
    })

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
    eventos = Evento.objects.filter(organizador=request.user).order_by('-data')
    return render(request, 'gestao/gerenciar_eventos.html', {'eventos': eventos})

@login_required
def criar_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user
            evento.aprovado = False
            evento.save()
            messages.success(request, 'Evento criado e enviado para aprovação!')
            return redirect('gerenciar_eventos')
    else:
        form = EventoForm()
    
    return render(request, 'gestao/evento_form.html', {
        'form': form, 
        'titulo': 'Novo Evento'
    })

@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            evento_salvo = form.save(commit=False)
            evento_salvo.save()
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('gerenciar_eventos')
    else:
        form = EventoForm(instance=evento)
        
    return render(request, 'gestao/evento_form.html', {
        'form': form, 
        'titulo': f'Editar: {evento.titulo}'
    })

@login_required
def deletar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento cancelado/excluído com sucesso.')
        return redirect('gerenciar_eventos')
    return render(request, 'gestao/evento_confirmar_delete.html', {'evento': evento})


@login_required
def aprovar_evento(request, pk):
    # Permite superuser, staff ou usuários com perfil Usuario.tipo == 'admin'
    if not (
        request.user.is_superuser or
        request.user.is_staff or
        (hasattr(request.user, 'usuario') and getattr(request.user.usuario, 'tipo', None) == 'admin')
    ):
        messages.error(request, 'Permissão negada.')
        return redirect('dashboard_user')

    evento = get_object_or_404(Evento, pk=pk)
    evento.aprovado = True
    evento.save()
    messages.success(request, 'Evento aprovado com sucesso.')
    return redirect('dashboard_user')


@login_required
def publicar_evento(request, pk):
    # Somente usuários staff/superuser podem publicar
    if not (
        request.user.is_superuser or
        request.user.is_staff or
        (hasattr(request.user, 'usuario') and getattr(request.user.usuario, 'tipo', None) == 'admin')
    ):
        messages.error(request, 'Permissão negada.')
        return redirect('dashboard_user')

    evento = get_object_or_404(Evento, pk=pk)
    evento.publicado = True
    evento.save()
    messages.success(request, 'Evento publicado com sucesso.')
    return redirect('dashboard_user')

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

@login_required
def ver_inscritos(request, pk):
    evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
    inscricoes_query = evento.inscricoes.all()
    lista_inscritos = []
    for inscricao in inscricoes_query:
        try:
            presente = inscricao.presenca.presente
        except Presenca.DoesNotExist:
            presente = False
            
        lista_inscritos.append({
            'inscricao': inscricao,
            'presente': presente
        })
    return render(request, 'gestao/ver_inscritos.html', {
        'evento': evento, 
        'lista_inscritos': lista_inscritos
    })

@login_required
def marcar_presenca(request, inscricao_id):
    inscricao = get_object_or_404(Inscricao, pk=inscricao_id)
    if inscricao.evento.organizador != request.user:
        messages.error(request, "Apenas o organizador pode marcar presença.")
        return redirect('index')
    presenca, created = Presenca.objects.get_or_create(inscricao=inscricao)
    presenca.presente = not presenca.presente
    presenca.save()
    status = "confirmada" if presenca.presente else "removida"
    messages.success(request, f"Presença de {inscricao.participante.username} {status}.")
    return redirect('ver_inscritos', pk=inscricao.evento.id)