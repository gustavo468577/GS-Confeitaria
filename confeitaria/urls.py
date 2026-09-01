from django.urls import path
from . import views

urlpatterns = [
    # URL da tela inicial.
    path('', views.inicio, name='inicio'),
]
