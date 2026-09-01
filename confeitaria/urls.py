from django.urls import path
from . import views

urlpatterns = [
    # URL da tela inicial.
    path('', views.inicio, name='inicio'),

    # URLs do CRUD de categorias.
    path('categorias/', views.categoria_listar, name='categoria_listar'),
    path('categorias/<int:pk>/', views.categoria_detalhar, name='categoria_detalhar'),
    path('categorias/criar/', views.categoria_criar, name='categoria_criar'),
    path('categorias/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('categorias/<int:pk>/excluir/', views.categoria_excluir, name='categoria_excluir'),

    # URLs do CRUD de produtos.
    path('produtos/', views.produto_listar, name='produto_listar'),
    path('produtos/<int:pk>/', views.produto_detalhar, name='produto_detalhar'),
    path('produtos/criar/', views.produto_criar, name='produto_criar'),
    path('produtos/<int:pk>/editar/', views.produto_editar, name='produto_editar'),
    path('produtos/<int:pk>/excluir/', views.produto_excluir, name='produto_excluir'),

    # URLs do CRUD de clientes.
    path('clientes/', views.cliente_listar, name='cliente_listar'),
    path('clientes/<int:pk>/', views.cliente_detalhar, name='cliente_detalhar'),
    path('clientes/criar/', views.cliente_criar, name='cliente_criar'),
    path('clientes/<int:pk>/editar/', views.cliente_editar, name='cliente_editar'),
    path('clientes/<int:pk>/excluir/', views.cliente_excluir, name='cliente_excluir'),
]