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
    path('inscricao/<int:inscricao_id>/presenca/', views.marcar_presenca, name='marcar_presenca'),
    # --- Perfil do Usuário ---
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/senha/', views.alterar_senha, name='alterar_senha'),
    # --- Admin ---
    path('relatorios/', views.relatorio_admin, name='relatorio_admin'),
]