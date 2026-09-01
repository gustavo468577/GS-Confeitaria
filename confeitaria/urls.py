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

    # URLs do CRUD de pedidos.
    path('pedidos/', views.pedido_listar, name='pedido_listar'),
    path('pedidos/<int:pk>/', views.pedido_detalhar, name='pedido_detalhar'),
    path('pedidos/criar/', views.pedido_criar, name='pedido_criar'),
    path('pedidos/<int:pk>/editar/', views.pedido_editar, name='pedido_editar'),
    path('pedidos/<int:pk>/excluir/', views.pedido_excluir, name='pedido_excluir'),

    # URLs do CRUD de itens de pedido.
    path('itens-pedido/', views.item_pedido_listar, name='item_pedido_listar'),
    path('itens-pedido/<int:pk>/', views.item_pedido_detalhar, name='item_pedido_detalhar'),
    path('itens-pedido/criar/', views.item_pedido_criar, name='item_pedido_criar'),
    path('itens-pedido/<int:pk>/editar/', views.item_pedido_editar, name='item_pedido_editar'),
    path('itens-pedido/<int:pk>/excluir/', views.item_pedido_excluir, name='item_pedido_excluir'),
]