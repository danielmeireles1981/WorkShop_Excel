from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_game, name='game_home'),
    path('fase/<int:numero>/', views.fase_view, name='fase'),
    path('concluir/<int:numero>/', views.concluir_fase, name='concluir_fase'),

    # Fase 1 - Funções básicas do Excel
    path('etapa1/', views.etapa1_view, name='etapa1'),
    path('etapa2/', views.etapa2_view, name='etapa2'),
    path('etapa3/', views.etapa3_view, name='etapa3'),
    path('etapa4/', views.etapa4_view, name='etapa4'),
    
    # Fase 2
    path('fase2/etapa1/', views.fase2_etapa1, name='fase2_etapa1'),
    path('fase2/etapa2/', views.fase2_etapa2, name='fase2_etapa2'),
    path('fase2/etapa3/', views.fase2_etapa3, name='fase2_etapa3'),
    path('fase2/final/', views.fase2_final, name='fase2_final'),
    path('fase2/finish/', views.fase2_finish, name='fase2_finish'),  # POST
    
    # Fase 3
    path('fase3/etapa1/', views.fase3_etapa1, name='fase3_etapa1'),
    path('fase3/submit/', views.fase3_submit, name='fase3_submit'),
]
