from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    TIPOS = [
        ('admin', 'Administrador'),
        ('organizador', 'Organizador'),
        ('participante', 'Participante'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    idade = models.PositiveIntegerField()
    tipo = models.CharField(max_length=20, choices=TIPOS)

    def __str__(self):
        return f"{self.nome} ({self.tipo})"


class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data = models.DateField()
    local = models.CharField(max_length=100)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos')
    aprovado = models.BooleanField(default=False)
    publicado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo


class Inscricao(models.Model):
    STATUS = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes')
    participante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscricoes')
    status = models.CharField(max_length=20, choices=STATUS, default='pendente')

    def __str__(self):
        return f"{self.participante.username} - {self.evento.titulo}"


class Presenca(models.Model):
    inscricao = models.OneToOneField(Inscricao, on_delete=models.CASCADE)
    presente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.inscricao.participante.username} - {self.inscricao.evento.titulo}"


class Relatorio(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    total_inscritos = models.IntegerField(default=0)
    total_presentes = models.IntegerField(default=0)
    data_geracao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Relatório - {self.evento.titulo}"

    
