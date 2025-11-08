from django.shortcuts import render, redirect, get_object_or_404
from .models import Fase, Progresso
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Presentation, Score

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

@login_required
def fase2_finish(request):
    if request.method == 'POST':
        # Exemplo: leitura de dados enviados
        phase = request.POST.get('phase', '2')
        points = int(request.POST.get('points', '80'))

        # TODO (opcional): salvar em um modelo Progress vinculado ao usuário
        # Progress.objects.update_or_create(
        #     user=request.user,
        #     phase=phase,
        #     defaults={'completed_at': timezone.now(), 'points': points}
        # )

        messages.success(request, f'Fase {phase} concluída! +{points} pontos adicionados ao seu perfil.')
        return redirect('game_home')

    messages.error(request, 'Ação inválida.')
    return redirect('fase2_final')

# ---------------- FASE 3 ---------------- #

@login_required
def fase3_etapa1(request):
    # Ranking (top 10)
    top_scores = Score.objects.order_by('-points_total', '-updated_at')[:10]
    return render(request, 'game/fase3_etapa1.html', {'top_scores': top_scores})

@login_required
def fase3_submit(request):
    if request.method != 'POST':
        messages.error(request, 'Método inválido.')
        return redirect('fase3_etapa1')

    resumo = request.POST.get('resumo', '').strip()
    link = request.POST.get('link', '').strip() or None
    auto_score = request.POST.get('auto_score')
    anexo = request.FILES.get('anexo')

    if not resumo or auto_score is None:
        messages.error(request, 'Preencha o resumo e a autoavaliação.')
        return redirect('fase3_etapa1')

    pres = Presentation.objects.create(
        user=request.user, resumo=resumo, link=link, anexo=anexo, auto_score=auto_score, phase=3
    )

    # Regra simples de pontuação (ajuste como quiser):
    # pontos = 60 base + (auto_score * 4), máximo 100
    try:
        pts = min(100, 60 + int(float(auto_score) * 4))
    except:
        pts = 60

    score, _ = Score.objects.get_or_create(user=request.user)
    score.points_total = max(score.points_total, pts)  # ou some: score.points_total += pts
    score.save()

    messages.success(request, f'Apresentação registrada! Você marcou {pts} pontos.')
    return redirect('fase3_etapa1')

@login_required
def fase3_etapa2(request):
    return render(request, 'game/fase3_etapa2.html')

@login_required
def fase3_final(request):
    return render(request, 'game/fase3_final.html')


# Em game/views.py
import logging
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Pega uma instância do logger
logger = logging.getLogger(__name__)

@login_required
@require_POST  # Garante que esta view só aceite requisições POST
def submit_etapa_view(request):
    # Onde o usuário será redirecionado em caso de sucesso ou erro
    redirect_url = request.META.get('HTTP_REFERER', 'game_home')

    logger.info(f"Iniciando 'submit_etapa_view' para o usuário: {request.user.username}")
    logger.debug(f"Dados do POST recebidos: {request.POST}")
    logger.debug(f"Arquivos recebidos (request.FILES): {request.FILES}")

    etapa_id = request.POST.get('etapa_id')
    planilha = request.FILES.get('planilha')

    if not etapa_id:
        logger.error("Erro no envio: 'etapa_id' não foi encontrado no POST.")
        messages.error(request, 'Erro no envio: ID da etapa não foi fornecido.')
        return redirect(redirect_url)

    if not planilha:
        logger.error(f"Erro no envio da etapa '{etapa_id}': Nenhum arquivo ('planilha') encontrado em request.FILES.")
        messages.error(request, 'Você esqueceu de selecionar um arquivo para enviar.')
        return redirect(redirect_url)

    logger.info(f"Arquivo '{planilha.name}' (tamanho: {planilha.size} bytes) recebido para a etapa '{etapa_id}'.")

    # Salvar o upload da etapa
    try:
        from .models import EtapaSubmission
        EtapaSubmission.objects.create(
            user=request.user,
            etapa_id=etapa_id,
            planilha=planilha,
        )
        logger.info("Upload persistido em EtapaSubmission.")
    except Exception as e:
        logger.exception(f"Falha ao salvar EtapaSubmission: {e}")

    # --- Lógica para salvar e validar o arquivo ---
    # Aqui você adicionaria o código para salvar o arquivo,
    # validar o conteúdo, calcular pontos, etc.
    # Exemplo:
    try:
        # Exemplo de como salvar o arquivo em um modelo (se você tiver um)
        # from .models import Submission
        # Submission.objects.create(
        #     user=request.user,
        #     etapa_id=etapa_id,
        #     file=planilha,
        # )
        logger.info(f"Processamento do arquivo para a etapa '{etapa_id}' iniciado...")
        # ... sua lógica de validação ...
        logger.info(f"Arquivo da etapa '{etapa_id}' processado com sucesso.")

    except Exception as e:
        logger.exception(f"Ocorreu uma exceção ao processar o arquivo da etapa '{etapa_id}': {e}")
        messages.error(request, f"Houve um erro inesperado ao processar seu arquivo: {e}")
        return redirect(redirect_url)
    # ---------------------------------------------

    messages.success(request, f'Planilha da etapa {etapa_id} enviada com sucesso!')
    logger.info(f"Redirecionando usuário '{request.user.username}' para '{redirect_url}' com mensagem de sucesso.")

    return redirect(redirect_url)

