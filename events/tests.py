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
        
        self.client.login(username='testuser', password='password123')
        
        url = reverse('editar_evento', args=[self.evento.pk]) 
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)

    def test_bloqueio_de_outros_usuarios(self):
        invasor = User.objects.create_user(username='invasor', password='password123')
        self.client.login(username='invasor', password='password123')
        
        url = reverse('editar_evento', args=[self.evento.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_criar_novo_evento_post(self):
        
        self.client.login(username='testuser', password='password123')
        
        dados_formulario = {
            'titulo': 'Workshop Django',
            'descricao': 'Aprendendo testes automatizados',
            'data': '2025-12-20',
            'local': 'Online'
        }

        url = reverse('criar_evento') 
        response = self.client.post(url, dados_formulario)

        self.assertEqual(response.status_code, 302) 

        self.assertEqual(Evento.objects.count(), 2)

        novo_evento = Evento.objects.last()
        self.assertEqual(novo_evento.titulo, 'Workshop Django')
        self.assertEqual(novo_evento.organizador.username, 'testuser')

        if response.status_code == 200:
            print(response.context['form'].errors)