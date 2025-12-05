from django.urls import path
from . import views

urlpatterns = [
    # --- Home e Públicas ---
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard_user'),
    # --- Eventos ---
    path('eventos/', views.eventos_lista, name='eventos'),
    path('eventos/novo/', views.criar_evento, name='criar_evento'),
    path('eventos/gerenciar/', views.gerenciar_eventos, name='gerenciar_eventos'),
    path('eventos/<int:pk>/', views.detalhes_evento, name='detalhes_evento'),
    path('eventos/<int:pk>/editar/', views.editar_evento, name='editar_evento'),
    path('eventos/<int:pk>/deletar/', views.deletar_evento, name='deletar_evento'),
    path('eventos/<int:evento_id>/inscrever/', views.inscrever_evento, name='inscrever_evento'),
    path('eventos/<int:pk>/aprovar/', views.aprovar_evento, name='aprovar_evento'),
    path('eventos/<int:pk>/publicar/', views.publicar_evento, name='publicar_evento'),
    path('eventos/<int:pk>/inscritos/', views.ver_inscritos, name='ver_inscritos'),
    # --- Inscrição ---
    path('inscricao/<int:inscricao_id>/presenca/', views.marcar_presenca, name='marcar_presenca'),
    path('inscricao/<int:pk>/confirmar/', views.confirmar_inscricao, name='confirmar_inscricao'),
    path('inscricao/<int:pk>/editar/', views.editar_inscricao, name='editar_inscricao'),
    path('inscricao/<int:pk>/deletar/', views.deletar_inscricao, name='deletar_inscricao'),
    path('inscricao/<int:pk>/', views.detalhes_inscricao, name='detalhes_inscricao'),
    # --- Presença ---
    path('presenca/<int:pk>/editar/', views.editar_presenca, name='editar_presenca'),
    path('presenca/<int:pk>/deletar/', views.deletar_presenca, name='deletar_presenca'),
    path('presenca/<int:pk>/', views.detalhes_presenca, name='detalhes_presenca'),
    # --- Relatório ---
    path('eventos/<int:pk>/relatorio/gerar/', views.gerar_relatorio, name='gerar_relatorio'),
    # --- Gestão de Relatórios do Evento ---
    path('eventos/<int:evento_id>/relatorios/', views.lista_relatorios, name='lista_relatorios'),
    path('eventos/<int:pk>/relatorio/gerar/', views.gerar_relatorio, name='gerar_relatorio'),
    path('relatorios/<int:pk>/', views.detalhes_relatorio, name='detalhes_relatorio'),
    path('relatorios/<int:pk>/editar/', views.editar_relatorio, name='editar_relatorio'),
    path('relatorios/<int:pk>/deletar/', views.deletar_relatorio, name='deletar_relatorio'),
    # --- Perfil do Usuário ---
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/senha/', views.alterar_senha, name='alterar_senha'),
    path('perfil/deletar/', views.deletar_minha_conta, name='deletar_minha_conta'),
    # --- Admin ---
    path('relatorios/', views.relatorio_admin, name='relatorio_admin'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario_admin, name='editar_usuario_admin'),
    path('usuarios/<int:pk>/deletar/', views.deletar_usuario, name='deletar_usuario'),
    path('usuarios/<int:pk>/', views.detalhes_usuario, name='detalhes_usuario'),
]