from django.test import TestCase
from django.contrib.auth.models import User
from .models import Evento
from datetime import date
from django.urls import reverse

class EventoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

        self.evento = Evento.objects.create(
            titulo="Meetup Python",
            descricao="Teste de evento",
            data=date.today(),
            local="Sala 1",
            organizador=self.user
        )

    def test_evento_foi_criado(self):
        self.assertEqual(self.evento.titulo, "Meetup Python")
        self.assertEqual(str(self.evento), "Meetup Python")
        self.assertEqual(self.evento.organizador.username, 'testuser')
        self.assertFalse(self.evento.aprovado)

    def test_view_detalhe(self):
        url = reverse('detalhes_evento', args=[self.evento.pk]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edicao_apenas_pelo_organizador(self):
        """Teste: O dono deve conseguir acessar a página de edição"""
        
        # 1. Faz login como o dono (criado no setUp)
        self.client.login(username='testuser', password='password123')
        
        # 2. Tenta acessar a página (ajuste 'editar_evento' para o nome da sua url)
        url = reverse('editar_evento', args=[self.evento.pk]) 
        response = self.client.get(url)
        
        # 3. Espera sucesso (200)
        self.assertEqual(response.status_code, 200)

    def test_bloqueio_de_outros_usuarios(self):
        invasor = User.objects.create_user(username='invasor', password='password123')
        self.client.login(username='invasor', password='password123')
        
        url = reverse('editar_evento', args=[self.evento.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)