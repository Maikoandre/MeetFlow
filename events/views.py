from django.shortcuts import render,  redirect, get_object_or_404
from .models import Evento, Usuario, Inscricao
from .forms import InscricaoEventoForm, EventoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.contrib import messages

def index(request):
    # Se o usuário estiver autenticado, mostrar o dashboard personalizado
    if request.user.is_authenticated:
        try:
            return dashboard(request)
        except Exception:
            # Se ocorrer algum erro ao montar o dashboard (ex: perfil ausente),
            # cair para a renderização pública da página inicial.
            pass

    return render(request, 'index.html')

def eventos_lista(request):
    """Lista todos os eventos publicados e aprovados"""
    eventos = Evento.objects.filter(publicado=True, aprovado=True)
    return render(request, 'events.html', {'eventos': eventos})

@login_required
def logout_view(request):
    """Faz logout do usuário"""
    logout(request)
    return redirect('index')

def login_view(request):
    """Login do usuário"""
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

@login_required
def aprovar_evento(request, pk):
    """Admin aprova evento para publicação"""
    evento = get_object_or_404(Evento, pk=pk)
    if request.user.is_staff or request.user.is_superuser:
        evento.aprovado = True
        evento.save()
        messages.success(request, f'Evento "{evento.titulo}" aprovado com sucesso!')
    return redirect('eventos')

@login_required
def publicar_evento(request, pk):
    """Admin ou organizador publica o evento"""
    evento = get_object_or_404(Evento, pk=pk)
    if request.user.is_staff or request.user.is_superuser or request.user == evento.organizador:
        evento.publicado = True
        evento.save()
        messages.success(request, f'Evento "{evento.titulo}" publicado com sucesso!')
    return redirect('eventos')

@login_required
def excluir_evento(request, pk):
    """Alias para deletar_evento para compatibilidade com template"""
    return deletar_evento(request, pk)


def dashboard(request):
    # Tenta pegar o perfil do usuário (modelo Usuario)
    try:
        perfil = request.user.usuario
    except Usuario.DoesNotExist:
        # Se não tiver perfil, talvez redirecionar para uma página de completar cadastro
        return render(request, 'erro_perfil.html', {'message': 'Perfil não encontrado'})

    context = {'perfil': perfil}

    # === LÓGICA DO ADMINISTRADOR ===
    if perfil.tipo == 'admin':
        # Admin vê estatísticas globais e eventos pendentes de aprovação
        context['total_usuarios'] = Usuario.objects.count()
        context['total_eventos'] = Evento.objects.count()
        context['eventos_pendentes'] = Evento.objects.filter(aprovado=False).count()
        
        # Lista dos últimos eventos que precisam de aprovação
        context['lista_pendentes'] = Evento.objects.filter(aprovado=False).order_by('data')

    # === LÓGICA DO ORGANIZADOR ===
    elif perfil.tipo == 'organizador':
        # Organizador vê APENAS seus eventos
        meus_eventos = Evento.objects.filter(organizador=request.user)
        context['meus_eventos_count'] = meus_eventos.count()
        context['meus_eventos'] = meus_eventos.order_by('-data')
        
        # Cálculo simples de total de inscritos nos eventos deste organizador
        total_inscritos = 0
        for evento in meus_eventos:
            total_inscritos += evento.inscricoes.count()
        context['total_inscritos'] = total_inscritos

    # === LÓGICA DO PARTICIPANTE ===
    elif perfil.tipo == 'participante':
        # Participante vê suas inscrições
        minhas_inscricoes = Inscricao.objects.filter(participante=request.user)
        context['minhas_inscricoes'] = minhas_inscricoes
        context['total_inscricoes'] = minhas_inscricoes.count()
        
        # Eventos confirmados (onde a inscrição status='confirmado')
        context['eventos_confirmados'] = minhas_inscricoes.filter(status='confirmado').count()

    # Renderiza o template de dashboard de usuário (arquivo em templates/)
    return render(request, 'dashboard_users.html', context)