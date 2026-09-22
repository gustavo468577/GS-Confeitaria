from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_not_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from .forms import CustomUserCreationForm
from .access import administrador_required, clientes_permitidos, pedidos_permitidos

from .forms import (
    CategoriaForm,
    ClienteForm,
    ProdutoForm,
    PedidoForm,
    ItemPedidoForm,
)
from .models import Categoria, Cliente, Produto, Pedido, ItemPedido

@login_not_required
def cadastrar(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Conta criada com sucesso.')
            login(request, cliente)
            return redirect('inicio')
    else:
        form = CustomUserCreationForm()

    return render(request, 'confeitaria/cadastro.html', {'form': form})
# Mostra a tela inicial do sistema.
def inicio(request):
    return render(request, 'confeitaria/inicio.html')


# FUNCOES DE CATEGORIA
# Lista todas as categorias cadastradas.
@administrador_required
@permission_required('confeitaria.view_categoria', raise_exception=True)
def categoria_listar(request):
    categorias = Categoria.objects.all()
    contexto = {'categorias': categorias}
    return render(request, 'confeitaria/categoria/listar.html', contexto)


# Mostra os detalhes de uma categoria.
@administrador_required
@permission_required('confeitaria.view_categoria', raise_exception=True)
def categoria_detalhar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    contexto = {'categoria': categoria}
    return render(request, 'confeitaria/categoria/detalhar.html', contexto)


# Cria uma nova categoria.
@administrador_required
@permission_required('confeitaria.add_categoria', raise_exception=True)
def categoria_criar(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados salvos com sucesso.')
            return redirect('categoria_listar')
    else:
        form = CategoriaForm()

    contexto = {'form': form}
    return render(request, 'confeitaria/categoria/form.html', contexto)


# Edita uma categoria existente.
@administrador_required
@permission_required('confeitaria.change_categoria', raise_exception=True)
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados salvos com sucesso.')
            return redirect('categoria_listar')
    else:
        form = CategoriaForm(instance=categoria)

    contexto = {'form': form, 'categoria': categoria}
    return render(request, 'confeitaria/categoria/form.html', contexto)


# Exclui uma categoria existente.
@administrador_required
@permission_required('confeitaria.delete_categoria', raise_exception=True)
def categoria_excluir(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Registro excluído com sucesso.')
        return redirect('categoria_listar')

    contexto = {'categoria': categoria}
    return render(request, 'confeitaria/categoria/confirmar_exclusao.html', contexto)


# FUNCOES DE PRODUTO
# Lista todos os produtos cadastrados.
def produto_listar(request):
    produtos = Produto.objects.select_related('categoria')
    if not request.user.has_perm('confeitaria.view_produto'):
        produtos = produtos.filter(ativo=True, categoria__ativo=True)
    categorias = Categoria.objects.filter(
        pk__in=produtos.values('categoria_id'),
    ).order_by('nome')
    categoria_selecionada = request.GET.get('categoria', '')
    if categoria_selecionada:
        if categoria_selecionada.isascii() and categoria_selecionada.isdigit() and len(categoria_selecionada) <= 18:
            produtos = produtos.filter(categoria_id=int(categoria_selecionada))
        else:
            produtos = produtos.none()
    contexto = {
        'produtos': produtos.order_by('nome'),
        'categorias': categorias,
        'categoria_selecionada': categoria_selecionada,
    }
    return render(request, 'confeitaria/produto/listar.html', contexto)


# Mostra os detalhes de um produto.
def produto_detalhar(request, pk):
    produtos = Produto.objects.select_related('categoria')
    if not request.user.has_perm('confeitaria.view_produto'):
        produtos = produtos.filter(ativo=True, categoria__ativo=True)
    produto = get_object_or_404(produtos, pk=pk)
    contexto = {'produto': produto}
    return render(request, 'confeitaria/produto/detalhar.html', contexto)


# Cria um novo produto.
@permission_required('confeitaria.add_produto', raise_exception=True)
def produto_criar(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados salvos com sucesso.')
            return redirect('produto_listar')
    else:
        form = ProdutoForm()

    contexto = {'form': form}
    return render(request, 'confeitaria/produto/form.html', contexto)


# Edita um produto existente.
@permission_required('confeitaria.change_produto', raise_exception=True)
def produto_editar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados salvos com sucesso.')
            return redirect('produto_listar')
    else:
        form = ProdutoForm(instance=produto)

    contexto = {'form': form, 'produto': produto}
    return render(request, 'confeitaria/produto/form.html', contexto)


# Exclui um produto existente.
@permission_required('confeitaria.delete_produto', raise_exception=True)
def produto_excluir(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Registro excluído com sucesso.')
        return redirect('produto_listar')

    contexto = {'produto': produto}
    return render(request, 'confeitaria/produto/confirmar_exclusao.html', contexto)


# FUNCOES DE CLIENTE
# Lista todos os clientes cadastrados.
@permission_required('confeitaria.view_cliente', raise_exception=True)
def cliente_listar(request):
    clientes = clientes_permitidos(request.user)
    contexto = {'clientes': clientes}
    return render(request, 'confeitaria/cliente/listar.html', contexto)


# Mostra os detalhes de um cliente.
def cliente_detalhar(request, pk):
    cliente = get_object_or_404(clientes_permitidos(request.user, 'view'), pk=pk)
    contexto = {'cliente': cliente}
    return render(request, 'confeitaria/cliente/detalhar.html', contexto)


# Cria um novo cliente.
@permission_required('confeitaria.add_cliente', raise_exception=True)
def cliente_criar(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados salvos com sucesso.')
            return redirect('cliente_listar')
    else:
        form = CustomUserCreationForm()

    contexto = {'form': form}
    return render(request, 'confeitaria/cliente/form.html', contexto)


# Edita um cliente existente.
def cliente_editar(request, pk):
    cliente = get_object_or_404(clientes_permitidos(request.user, 'change'), pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados salvos com sucesso.')
            return redirect('cliente_detalhar', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)

    contexto = {'form': form, 'cliente': cliente}
    return render(request, 'confeitaria/cliente/form.html', contexto)


# Exclui um cliente existente.
@permission_required('confeitaria.delete_cliente', raise_exception=True)
def cliente_excluir(request, pk):
    cliente = get_object_or_404(clientes_permitidos(request.user, 'delete'), pk=pk)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Registro excluído com sucesso.')
        return redirect('cliente_listar')

    contexto = {'cliente': cliente}
    return render(request, 'confeitaria/cliente/confirmar_exclusao.html', contexto)


# FUNCOES DE PEDIDO
# Lista todos os pedidos cadastrados.
def pedido_listar(request):
    pedidos = pedidos_permitidos(request.user)
    contexto = {'pedidos': pedidos}
    return render(request, 'confeitaria/pedido/listar.html', contexto)


# Mostra os detalhes de um pedido.
def pedido_detalhar(request, pk):
    pedido = get_object_or_404(pedidos_permitidos(request.user, 'view_pedido'), pk=pk)
    contexto = {'pedido': pedido}
    return render(request, 'confeitaria/pedido/detalhar.html', contexto)


# Cria um novo pedido.
def pedido_criar(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados salvos com sucesso.')
            return redirect('pedido_listar')
    else:
        form = PedidoForm(user=request.user)

    contexto = {'form': form}
    return render(request, 'confeitaria/pedido/form.html', contexto)


# Edita um pedido existente.
def pedido_editar(request, pk):
    pedido = get_object_or_404(pedidos_permitidos(request.user, 'change_pedido'), pk=pk)

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados salvos com sucesso.')
            return redirect('pedido_listar')
    else:
        form = PedidoForm(instance=pedido, user=request.user)

    contexto = {'form': form, 'pedido': pedido}
    return render(request, 'confeitaria/pedido/form.html', contexto)


# Exclui um pedido existente.
def pedido_excluir(request, pk):
    pedido = get_object_or_404(pedidos_permitidos(request.user, 'delete_pedido'), pk=pk)

    if request.method == 'POST':
        pedido.delete()
        messages.success(request, 'Registro excluído com sucesso.')
        return redirect('pedido_listar')

    contexto = {'pedido': pedido}
    return render(request, 'confeitaria/pedido/confirmar_exclusao.html', contexto)


# FUNCOES DE ITEM PEDIDO
# Lista todos os itens de pedido cadastrados.
def item_pedido_listar(request):
    itens_pedido = ItemPedido.objects.filter(pedido__in=pedidos_permitidos(request.user, 'view_itempedido'))
    contexto = {'itens_pedido': itens_pedido}
    return render(request, 'confeitaria/item_pedido/listar.html', contexto)


# Mostra os detalhes de um item de pedido.
def item_pedido_detalhar(request, pk):
    item_pedido = get_object_or_404(
        ItemPedido, pk=pk,
        pedido__in=pedidos_permitidos(request.user, 'view_itempedido'),
    )
    contexto = {'item_pedido': item_pedido}
    return render(request, 'confeitaria/item_pedido/detalhar.html', contexto)


# Cria um novo item de pedido.
def item_pedido_criar(request):
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados salvos com sucesso.')
            return redirect('item_pedido_listar')
    else:
        form = ItemPedidoForm(user=request.user)
        produto_id = request.GET.get('produto')
        if produto_id is not None:
            if not produto_id.isascii() or not produto_id.isdigit() or len(produto_id) > 18:
                raise Http404('Produto não encontrado.')
            produto = get_object_or_404(form.fields['produto'].queryset, pk=int(produto_id))
            form.initial['produto'] = produto.pk

    contexto = {'form': form}
    return render(request, 'confeitaria/item_pedido/form.html', contexto)


# Edita um item de pedido existente.
def item_pedido_editar(request, pk):
    item_pedido = get_object_or_404(
        ItemPedido, pk=pk,
        pedido__in=pedidos_permitidos(request.user, 'change_itempedido'),
    )

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados salvos com sucesso.')
            return redirect('item_pedido_listar')
    else:
        form = ItemPedidoForm(instance=item_pedido, user=request.user)

    contexto = {'form': form, 'item_pedido': item_pedido}
    return render(request, 'confeitaria/item_pedido/form.html', contexto)


# Exclui um item de pedido existente.
def item_pedido_excluir(request, pk):
    item_pedido = get_object_or_404(
        ItemPedido, pk=pk,
        pedido__in=pedidos_permitidos(request.user, 'delete_itempedido'),
    )

    if request.method == 'POST':
        item_pedido.delete()
        messages.success(request, 'Registro excluído com sucesso.')
        return redirect('item_pedido_listar')

    contexto = {'item_pedido': item_pedido}
    return render(request, 'confeitaria/item_pedido/confirmar_exclusao.html', contexto)
