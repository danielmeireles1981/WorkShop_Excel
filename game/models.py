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

from django.conf import settings
from django.db import models

class Presentation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resumo = models.TextField()
    link = models.URLField(blank=True, null=True)
    anexo = models.FileField(upload_to="presentations/", blank=True, null=True)
    auto_score = models.DecimalField(max_digits=4, decimal_places=1)  # 0–10
    phase = models.PositiveSmallIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

class Score(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points_total = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    