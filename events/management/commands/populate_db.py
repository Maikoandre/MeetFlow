import random
from datetime import timedelta, date
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from events.models import Usuario, Evento, Inscricao, Presenca, Relatorio
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populates the database with mock data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating mock data...')

        # Names for generation
        first_names = ['Ana', 'Bruno', 'Carlos', 'Daniela', 'Eduardo', 'Fernanda', 'Gabriel', 'Helena', 'Igor', 'Julia', 'Lucas', 'Mariana', 'Nicolas', 'Olivia', 'Pedro', 'Rafaela', 'Samuel', 'Tatiana', 'Vitor', 'Yasmin']
        last_names = ['Silva', 'Santos', 'Oliveira', 'Souza', 'Rodrigues', 'Ferreira', 'Alves', 'Pereira', 'Lima', 'Gomes', 'Costa', 'Ribeiro', 'Martins', 'Carvalho', 'Almeida', 'Lopes', 'Soares', 'Fernandes', 'Vieira', 'Barbosa']

        def get_random_name():
            return f"{random.choice(first_names)} {random.choice(last_names)}"

        # 0. Create Admin
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser('admin', 'admin@example.com', 'password123')
            Usuario.objects.create(user=user, nome='Administrador', idade=30, tipo='admin')
            self.stdout.write('Created admin: admin')

        # 1. Create Organizers
        organizers = []
        for i in range(5):
            username = f'org{i+1}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=f'{username}@example.com', password='password123')
                Usuario.objects.create(user=user, nome=get_random_name(), idade=random.randint(25, 50), tipo='organizador')
                organizers.append(user)
                self.stdout.write(f'Created organizer: {username}')
            else:
                organizers.append(User.objects.get(username=username))

        # 2. Create Participants
        participants = []
        for i in range(20):
            username = f'user{i+1}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=f'{username}@example.com', password='password123')
                Usuario.objects.create(user=user, nome=get_random_name(), idade=random.randint(18, 40), tipo='participante')
                participants.append(user)
                self.stdout.write(f'Created participant: {username}')
            else:
                participants.append(User.objects.get(username=username))

        # 3. Create Events
        event_titles = ['Workshop Python', 'Palestra IA', 'Meetup Django', 'Hackathon Web', 'Curso React', 'Seminário DevOps', 'Conferência Tech', 'Bootcamp Java', 'Workshop UX/UI', 'Encontro Agile']
        events = []
        for i, title in enumerate(event_titles):
            organizer = random.choice(organizers)
            event_date = timezone.now().date() + timedelta(days=random.randint(-30, 60))
            
            evento = Evento.objects.create(
                titulo=title,
                descricao=f'Descrição detalhada para o evento {title}. Este evento será incrível e contará com muitos aprendizados.',
                data=event_date,
                local=f'Sala {random.randint(100, 999)}',
                organizador=organizer,
                aprovado=random.choice([True, True, False]), # More likely to be approved
                publicado=random.choice([True, True, False])
            )
            events.append(evento)
            self.stdout.write(f'Created event: {title}')

        # 4. Create Inscriptions
        for _ in range(50):
            participant = random.choice(participants)
            evento = random.choice(events)
            
            if not Inscricao.objects.filter(participante=participant, evento=evento).exists():
                status = random.choice(['pendente', 'confirmado', 'cancelado'])
                inscricao = Inscricao.objects.create(
                    evento=evento,
                    participante=participant,
                    status=status
                )
                
                # 5. Create Presence (only if confirmed and event passed)
                if status == 'confirmado' and evento.data < timezone.now().date():
                    presente = random.choice([True, False])
                    Presenca.objects.create(inscricao=inscricao, presente=presente)

        # 6. Create Reports (for past events)
        for evento in events:
            if evento.data < timezone.now().date():
                total_inscritos = evento.inscricoes.count()
                total_presentes = Presenca.objects.filter(inscricao__evento=evento, presente=True).count()
                Relatorio.objects.create(
                    evento=evento,
                    total_inscritos=total_inscritos,
                    total_presentes=total_presentes
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated database with mock data'))
