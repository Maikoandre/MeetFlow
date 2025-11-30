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
    path('evento/<int:evento_id>/inscrever/', views.inscrever_evento, name='inscrever_evento'),
    path('evento/<int:pk>/', views.detalhes_evento, name='detalhes_evento'),
    path('evento/', views.gerenciar_eventos, name='gerenciar_eventos'),
    path('evento/novo/', views.criar_evento, name='criar_evento'),
    path('evento/<int:pk>/editar/', views.editar_evento, name='editar_evento'),
    path('evento/<int:pk>/deletar/', views.deletar_evento, name='deletar_evento'),
    path('evento/<int:pk>/excluir/', views.excluir_evento, name='excluir_evento'),
    path('evento/<int:pk>/aprovar/', views.aprovar_evento, name='aprovar_evento'),
    path('evento/<int:pk>/publicar/', views.publicar_evento, name='publicar_evento'),
    path('evento9/<int:pk>/inscritos/', views.ver_inscritos, name='ver_inscritos'),
    # --- Perfil do Usuário ---
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/senha/', views.alterar_senha, name='alterar_senha'),
]