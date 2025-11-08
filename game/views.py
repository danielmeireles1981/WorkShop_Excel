from django.shortcuts import render, redirect, get_object_or_404
from .models import Fase, Progresso
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def home_game(request):
    fases = Fase.objects.all().order_by('numero')
    progresso = Progresso.objects.filter(user=request.user)
    concluidas = [p.fase.numero for p in progresso if p.concluida]

    return render(request, 'game/home.html', {
        'fases': fases,
        'concluidas': concluidas,
    })

@login_required
def fase_view(request, numero):
    fase = get_object_or_404(Fase, numero=numero)
    return render(request, 'game/fase.html', {'fase': fase})

@login_required
def concluir_fase(request, numero):
    fase = get_object_or_404(Fase, numero=numero)
    progresso, _ = Progresso.objects.get_or_create(user=request.user, fase=fase)
    progresso.concluida = True
    progresso.data_conclusao = timezone.now()
    progresso.save()
    return redirect('/game/')

# --- Etapas da Fase 1 ---

@login_required
def etapa1_view(request):
    return render(request, 'game/fase1_etapa1.html')

@login_required
def etapa2_view(request):
    return render(request, 'game/fase1_etapa2.html')

@login_required
def etapa3_view(request):
    return render(request, 'game/fase1_etapa3.html')

@login_required
def etapa4_view(request):
    return render(request, 'game/fase1_etapa4.html')

# ---------------- FASE 2 ---------------- #

@login_required
def fase2_etapa1(request):
    return render(request, 'game/fase2_etapa1.html')

@login_required
def fase2_etapa2(request):
    return render(request, 'game/fase2_etapa2.html')

@login_required
def fase2_etapa3(request):
    return render(request, 'game/fase2_etapa3.html')

@login_required
def fase2_final(request):
    return render(request, 'game/fase2_final.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# ---------------- FASE 3 ---------------- #

@login_required
def fase3_etapa1(request):
    return render(request, 'game/fase3_etapa1.html')

@login_required
def fase3_etapa2(request):
    return render(request, 'game/fase3_etapa2.html')

@login_required
def fase3_final(request):
    return render(request, 'game/fase3_final.html')
