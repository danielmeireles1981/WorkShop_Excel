from django.urls import path
from . import views

urlpatterns = [
    path('', views.ranking_view, name='ranking'),
]
