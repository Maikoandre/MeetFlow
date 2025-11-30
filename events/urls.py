from django.urls import path
from . import views

urlpatterns = [
    # --- Home e Públicas ---
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    # --- Eventos ---
    path('evento/<int:evento_id>/inscrever/', views.inscrever_evento, name='inscrever_evento'),
    path('evento/<int:pk>/', views.detalhes_evento, name='detalhes_evento'),
    # --- Perfil do Usuário ---
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/senha/', views.alterar_senha, name='alterar_senha'),
]