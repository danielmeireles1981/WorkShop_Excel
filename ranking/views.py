from django.shortcuts import render
from accounts.models import Profile

def ranking_view(request):
    ranking = Profile.objects.order_by('-pontuacao_total')
    return render(request, 'ranking/ranking.html', {'ranking': ranking})
