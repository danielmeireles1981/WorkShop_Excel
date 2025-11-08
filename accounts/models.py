from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personagem = models.CharField(max_length=100, choices=[
        ('universitario', 'Estudante Universitário'),
        ('empreendedor', 'Empreendedor Júnior'),
        ('aprendiz', 'Aprendiz Financeiro'),
    ])
    avatar = models.CharField(max_length=10, default='🙂')
    email = models.EmailField()
    data_nascimento = models.DateField()
    idade = models.IntegerField(default=0)
    pontuacao_total = models.IntegerField(default=0)
    fase_atual = models.IntegerField(default=1)

    def calcular_idade(self):
        if isinstance(self.data_nascimento, str):
            # Converte a string do formulário para um objeto date
            data = datetime.strptime(self.data_nascimento, "%Y-%m-%d").date()
        else:
            data = self.data_nascimento

        hoje = date.today()
        return hoje.year - data.year - ((hoje.month, hoje.day) < (data.month, data.day))

    def save(self, *args, **kwargs):
        self.idade = self.calcular_idade()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.avatar})"
