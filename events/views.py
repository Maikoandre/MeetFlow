from django.shortcuts import render,  redirect, get_object_or_404
from .models import Evento, Usuario, Inscricao
from .forms import InscricaoEventoForm, EventoForm, InscricaoStatusForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EventoForm, InscricaoEventoForm, UsuarioForm, PresencaForm, RelatorioForm
from .models import Evento, Inscricao, Usuario, Presenca, Relatorio


def index(request):
    total_eventos = Evento.objects.filter(publicado=True, aprovado=True).count()
    total_participantes = Usuario.objects.count()

    if request.user.is_authenticated:
        try:
            return dashboard(request)
        except Exception:
            pass 

    return render(request, 'index.html', {
        'total_eventos': total_eventos,
        'total_participantes': total_participantes,
    })



@login_required
def dashboard(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    context = {
        'perfil': usuario,
        'tipo': usuario.tipo,
    }

    if usuario.tipo == 'admin':
        context.update({
            'total_eventos': Evento.objects.count(),
            'total_usuarios': Usuario.objects.count(),
            'eventos_pendentes': Evento.objects.filter(aprovado=False).count(),
            'lista_pendentes': Evento.objects.filter(aprovado=False).select_related('organizador'),
            'lista_a_publicar': Evento.objects.filter(aprovado=True, publicado=False).select_related('organizador'),
            'lista_publicados': Evento.objects.filter(publicado=True).select_related('organizador'),
        })
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


@login_required
def criar_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user
            evento.aprovado = False
            evento.publicado = False
            evento.save()
            messages.success(request, 'Evento criado com sucesso! Aguarde a aprovação.')
            return redirect('gerenciar_eventos')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = EventoForm()
    
    return render(request, 'gestao/evento_form.html', {
        'form': form, 
        'titulo': 'Novo Evento',
        'btn_texto': 'Criar Evento'
    })


@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.save()
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('gerenciar_eventos')
    else:
        form = EventoForm(instance=evento)
        
    return render(request, 'gestao/evento_form.html', {
        'form': form, 
        'titulo': f'Editar: {evento.titulo}',
        'btn_texto': 'Atualizar Evento'
    })


@login_required
def deletar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
    
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento eliminado com sucesso.')
        return redirect('gerenciar_eventos')
    
    return render(request, 'gestao/evento_confirmar_delete.html', {
        'objeto': evento,
        'titulo_confirmacao': f"eliminar o evento {evento.titulo}",
        'cancel_url': reverse('gerenciar_eventos')
    })


@login_required
def aprovar_evento(request, pk):
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
    return render(request, 'gestao/relatorio_admin.html', context)


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

@login_required
def inscrever_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    if Inscricao.objects.filter(evento=evento, participante=request.user).exists():
        messages.warning(request, "Você já está inscrito neste evento.")
        return redirect('detalhes_evento', pk=evento.id)
    
    if request.method == 'POST':
        form = InscricaoEventoForm(request.POST)
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.participante = request.user
            inscricao.evento = evento
            inscricao.save()
            messages.success(request, "Inscrição confirmada com sucesso!")
            
            return redirect('detalhes_evento', pk=evento.id)
    else:
        form = InscricaoEventoForm()

    return render(request, 'forms/evento_inscricao.html', {'form': form, 'evento': evento})

@login_required
def gerenciar_eventos(request):
    """ R (Read - List): Lista os eventos do organizador para gestão """
    eventos = Evento.objects.filter(organizador=request.user).order_by('-data')
    return render(request, 'gestao/gerenciar_eventos.html', {'eventos': eventos})

def detalhes_evento(request, pk):
    """ R (Read - Detail): Mostra os detalhes de um evento único """
    evento = get_object_or_404(Evento, pk=pk)
    ja_inscrito = False
    
    if request.user.is_authenticated:
        ja_inscrito = Inscricao.objects.filter(evento=evento, participante=request.user).exists()

    return render(request, 'detalhes_evento.html', {
        'evento': evento,
        'ja_inscrito': ja_inscrito
    })

@login_required
def editar_inscricao(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)
    if not (request.user == inscricao.evento.organizador or request.user.is_superuser):
        messages.error(request, "Permissão negada.")
        return redirect('dashboard_user')

    if request.method == 'POST':
        form = InscricaoStatusForm(request.POST, instance=inscricao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estado da inscrição atualizado!')
            return redirect('ver_inscritos', pk=inscricao.evento.pk)
    else:
        form = InscricaoStatusForm(instance=inscricao)

    return render(request, 'gestao/evento_form.html', {
        'form': form,
        'titulo': f'Gerir Inscrição: {inscricao.participante.username}',
        'btn_texto': 'Atualizar Status'
    })

@login_required
def deletar_inscricao(request, pk):

    inscricao = get_object_or_404(Inscricao, pk=pk)
    evento_id = inscricao.evento.id
    
    is_dono = request.user == inscricao.evento.organizador
    is_proprio = request.user == inscricao.participante
    
    if not (is_dono or is_proprio or request.user.is_superuser):
        messages.error(request, "Permissão negada.")
        return redirect('index')

    if request.method == 'POST':
        inscricao.delete()
        messages.success(request, 'Inscrição cancelada/removida.')
        if is_dono:
            return redirect('ver_inscritos', pk=evento_id)
        return redirect('dashboard_user')

    return render(request, 'gestao/evento_confirmar_delete.html', {
        'objeto': inscricao,
        'titulo_confirmacao': f"cancelar a inscrição de {inscricao.participante.username}",
        'cancel_url': reverse('ver_inscritos', args=[evento_id]) if is_dono else reverse('dashboard_user')
    })


@login_required
def editar_presenca(request, pk):
    presenca = get_object_or_404(Presenca, pk=pk)
    if presenca.inscricao.evento.organizador != request.user:
        messages.error(request, "Apenas o organizador pode editar esta presença.")
        return redirect('dashboard_user')

    if request.method == 'POST':
        form = PresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estado da presença atualizado com sucesso!')
            return redirect('ver_inscritos', pk=presenca.inscricao.evento.pk)
    else:
        form = PresencaForm(instance=presenca)

    return render(request, 'gestao/evento_form.html', {
        'form': form,
        'titulo': f'Editar Presença: {presenca.inscricao.participante.username}',
        'btn_texto': 'Guardar Alterações'
    })

@login_required
def deletar_presenca(request, pk):
    presenca = get_object_or_404(Presenca, pk=pk)
    evento_id = presenca.inscricao.evento.id
    
    if presenca.inscricao.evento.organizador != request.user:
        messages.error(request, "Permissão negada.")
        return redirect('dashboard_user')

    if request.method == 'POST':
        presenca.delete()
        messages.success(request, 'Presença removida com sucesso.')
        return redirect('ver_inscritos', pk=evento_id)
    
    return render(request, 'gestao/evento_confirmar_delete.html', {
        'objeto': presenca,
        'titulo_confirmacao': f"remover a presença de {presenca.inscricao.participante.username}",
        'cancel_url': reverse('ver_inscritos', args=[evento_id])
    })

@login_required
def gerar_relatorio(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if evento.organizador != request.user and not request.user.is_superuser:
        messages.error(request, "Não tem permissão para gerar relatórios deste evento.")
        return redirect('dashboard_user')

    total_inscritos = evento.inscricoes.count()
    total_presentes = Presenca.objects.filter(inscricao__evento=evento, presente=True).count()
    Relatorio.objects.create(
        evento=evento,
        total_inscritos=total_inscritos,
        total_presentes=total_presentes
    )

    messages.success(request, "Relatório de estatísticas gerado com sucesso!")
    return redirect('detalhes_evento', pk=evento.pk)

@login_required
def lista_relatorios(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    if evento.organizador != request.user and not request.user.is_superuser:
        messages.error(request, "Permissão negada.")
        return redirect('dashboard_user')

    relatorios = Relatorio.objects.filter(evento=evento).order_by('-data_geracao')
    return render(request, 'gestao/relatorio_lista.html', {
        'evento': evento,
        'relatorios': relatorios
    })

@login_required
def detalhes_relatorio(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)
    if relatorio.evento.organizador != request.user and not request.user.is_superuser:
        messages.error(request, "Permissão negada.")
        return redirect('dashboard_user')

    return render(request, 'gestao/relatorio_detalhe.html', {'relatorio': relatorio})


@login_required
def editar_relatorio(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)
    if relatorio.evento.organizador != request.user and not request.user.is_superuser:
        messages.error(request, "Permissão negada.")
        return redirect('dashboard_user')

    if request.method == 'POST':
        form = RelatorioForm(request.POST, instance=relatorio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do relatório atualizados manualmente.')
            return redirect('detalhes_relatorio', pk=relatorio.pk)
    else:
        form = RelatorioForm(instance=relatorio)

    return render(request, 'gestao/evento_form.html', {
        'form': form,
        'titulo': f'Editar Relatório: {relatorio.evento.titulo}',
        'btn_texto': 'Salvar Correções'
    })

@login_required
def deletar_relatorio(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)
    evento_id = relatorio.evento.id
    if relatorio.evento.organizador != request.user and not request.user.is_superuser:
        messages.error(request, "Permissão negada.")
        return redirect('dashboard_user')

    if request.method == 'POST':
        relatorio.delete()
        messages.success(request, 'Relatório removido do histórico.')
        return redirect('lista_relatorios', evento_id=evento_id)
    
    return render(request, 'gestao/evento_confirmar_delete.html', {
        'objeto': relatorio, 
        'titulo_confirmacao': f"apagar o relatório gerado em {relatorio.data_geracao}",
        'cancel_url': reverse('lista_relatorios', args=[evento_id])
    })

@login_required
def confirmar_inscricao(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)
    if inscricao.participante != request.user:
        messages.error(request, "Você não tem permissão para confirmar esta inscrição.")
        return redirect('dashboard_user')
    
    inscricao.save()
    messages.success(request, "Inscrição confirmada com sucesso!")
    return redirect('dashboard_user')

@login_required
def deletar_minha_conta(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Sua conta foi deletada com sucesso.")
        return redirect('index')
    return render(request, 'forms/confirmar_delete_conta.html')

@login_required
@user_passes_test(is_admin)
def lista_usuarios(request):
    usuarios = Usuario.objects.select_related('user').all()
    return render(request, 'gestao/lista_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(is_admin)
def deletar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        user = usuario.user
        user.delete()
        messages.success(request, f"Usuário {usuario.nome} deletado com sucesso.")
        return redirect('lista_usuarios')
    return render(request, 'gestao/evento_confirmar_delete.html', {
        'objeto': usuario, 
        'titulo_confirmacao': f"deletar o usuário {usuario.nome}",
        'cancel_url': reverse('lista_usuarios')
    })