from django.db import models
from django.contrib.auth.models import User

class Fase(models.Model):
    numero = models.IntegerField(unique=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    pontos = models.IntegerField(default=10)

    def __str__(self):
        return f"Fase {self.numero}: {self.titulo}"

class Progresso(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    concluida = models.BooleanField(default=False)
    data_conclusao = models.DateTimeField(null=True, blank=True)
