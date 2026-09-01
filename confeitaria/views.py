from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CategoriaForm,
    ClienteForm,
    ProdutoForm,
    PedidoForm,
    ItemPedidoForm,
)
from .models import Categoria, Cliente, Produto, Pedido, ItemPedido


# Mostra a tela inicial do sistema.
def inicio(request):
    return render(request, 'confeitaria/inicio.html')


# FUNCOES DE CATEGORIA
# Lista todas as categorias cadastradas.
def categoria_listar(request):
    categorias = Categoria.objects.all()
    contexto = {'categorias': categorias}
    return render(request, 'confeitaria/categoria/listar.html', contexto)


# Mostra os detalhes de uma categoria.
def categoria_detalhar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    contexto = {'categoria': categoria}
    return render(request, 'confeitaria/categoria/detalhar.html', contexto)


# Cria uma nova categoria.
def categoria_criar(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_listar')
    else:
        form = CategoriaForm()

    contexto = {'form': form}
    return render(request, 'confeitaria/categoria/form.html', contexto)


# Edita uma categoria existente.
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categoria_listar')
    else:
        form = CategoriaForm(instance=categoria)

    contexto = {'form': form, 'categoria': categoria}
    return render(request, 'confeitaria/categoria/form.html', contexto)


# Exclui uma categoria existente.
def categoria_excluir(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria_listar')

    contexto = {'categoria': categoria}
    return render(request, 'confeitaria/categoria/confirmar_exclusao.html', contexto)


# FUNCOES DE PRODUTO
# Lista todos os produtos cadastrados.
def produto_listar(request):
    produtos = Produto.objects.all()
    contexto = {'produtos': produtos}
    return render(request, 'confeitaria/produto/listar.html', contexto)


# Mostra os detalhes de um produto.
def produto_detalhar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    contexto = {'produto': produto}
    return render(request, 'confeitaria/produto/detalhar.html', contexto)


# Cria um novo produto.
def produto_criar(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produto_listar')
    else:
        form = ProdutoForm()

    contexto = {'form': form}
    return render(request, 'confeitaria/produto/form.html', contexto)


# Edita um produto existente.
def produto_editar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produto_listar')
    else:
        form = ProdutoForm(instance=produto)

    contexto = {'form': form, 'produto': produto}
    return render(request, 'confeitaria/produto/form.html', contexto)


# Exclui um produto existente.
def produto_excluir(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == 'POST':
        produto.delete()
        return redirect('produto_listar')

    contexto = {'produto': produto}
    return render(request, 'confeitaria/produto/confirmar_exclusao.html', contexto)


# FUNCOES DE CLIENTE
# Lista todos os clientes cadastrados.
def cliente_listar(request):
    clientes = Cliente.objects.all()
    contexto = {'clientes': clientes}
    return render(request, 'confeitaria/cliente/listar.html', contexto)


# Mostra os detalhes de um cliente.
def cliente_detalhar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    contexto = {'cliente': cliente}
    return render(request, 'confeitaria/cliente/detalhar.html', contexto)


# Cria um novo cliente.
def cliente_criar(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_listar')
    else:
        form = ClienteForm()

    contexto = {'form': form}
    return render(request, 'confeitaria/cliente/form.html', contexto)


# Edita um cliente existente.
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_listar')
    else:
        form = ClienteForm(instance=cliente)

    contexto = {'form': form, 'cliente': cliente}
    return render(request, 'confeitaria/cliente/form.html', contexto)


# Exclui um cliente existente.
def cliente_excluir(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_listar')

    contexto = {'cliente': cliente}
    return render(request, 'confeitaria/cliente/confirmar_exclusao.html', contexto)


# FUNCOES DE PEDIDO
# Lista todos os pedidos cadastrados.
def pedido_listar(request):
    pedidos = Pedido.objects.all()
    contexto = {'pedidos': pedidos}
    return render(request, 'confeitaria/pedido/listar.html', contexto)


# Mostra os detalhes de um pedido.
def pedido_detalhar(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    contexto = {'pedido': pedido}
    return render(request, 'confeitaria/pedido/detalhar.html', contexto)


# Cria um novo pedido.
def pedido_criar(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedido_listar')
    else:
        form = PedidoForm()

    contexto = {'form': form}
    return render(request, 'confeitaria/pedido/form.html', contexto)


# Edita um pedido existente.
def pedido_editar(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('pedido_listar')
    else:
        form = PedidoForm(instance=pedido)

    contexto = {'form': form, 'pedido': pedido}
    return render(request, 'confeitaria/pedido/form.html', contexto)


# Exclui um pedido existente.
def pedido_excluir(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == 'POST':
        pedido.delete()
        return redirect('pedido_listar')

    contexto = {'pedido': pedido}
    return render(request, 'confeitaria/pedido/confirmar_exclusao.html', contexto)


# FUNCOES DE ITEM PEDIDO
# Lista todos os itens de pedido cadastrados.
def item_pedido_listar(request):
    itens_pedido = ItemPedido.objects.all()
    contexto = {'itens_pedido': itens_pedido}
    return render(request, 'confeitaria/item_pedido/listar.html', contexto)


# Mostra os detalhes de um item de pedido.
def item_pedido_detalhar(request, pk):
    item_pedido = get_object_or_404(ItemPedido, pk=pk)
    contexto = {'item_pedido': item_pedido}
    return render(request, 'confeitaria/item_pedido/detalhar.html', contexto)


# Cria um novo item de pedido.
def item_pedido_criar(request):
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_pedido_listar')
    else:
        form = ItemPedidoForm()

    contexto = {'form': form}
    return render(request, 'confeitaria/item_pedido/form.html', contexto)


# Edita um item de pedido existente.
def item_pedido_editar(request, pk):
    item_pedido = get_object_or_404(ItemPedido, pk=pk)

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            form.save()
            return redirect('item_pedido_listar')
    else:
        form = ItemPedidoForm(instance=item_pedido)

    contexto = {'form': form, 'item_pedido': item_pedido}
    return render(request, 'confeitaria/item_pedido/form.html', contexto)


# Exclui um item de pedido existente.
def item_pedido_excluir(request, pk):
    item_pedido = get_object_or_404(ItemPedido, pk=pk)

    if request.method == 'POST':
        item_pedido.delete()
        return redirect('item_pedido_listar')

    contexto = {'item_pedido': item_pedido}
    return render(request, 'confeitaria/item_pedido/confirmar_exclusao.html', contexto)
