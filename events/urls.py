from django.urls import path
from . import views

urlpatterns = [
    # --- Home e Públicas ---
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    # --- Eventos ---
    path('evento/<int:evento_id>/inscrever/', views.inscrever_evento, name='inscrever_evento'),
    path('evento/<int:pk>/', views.detalhes_evento, name='detalhes_evento'),
    path('evento/', views.gerenciar_eventos, name='gerenciar_eventos'),
    path('evento/novo/', views.criar_evento, name='criar_evento'),
    path('evento/<int:pk>/editar/', views.editar_evento, name='editar_evento'),
    path('evento/<int:pk>/deletar/', views.deletar_evento, name='deletar_evento'),
    path('evento9/<int:pk>/inscritos/', views.ver_inscritos, name='ver_inscritos'),
    # --- Perfil do Usuário ---
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/senha/', views.alterar_senha, name='alterar_senha'),
    # --- Admin ---
    path('relatorios/', views.relatorio_admin, name='relatorio_admin'),
]