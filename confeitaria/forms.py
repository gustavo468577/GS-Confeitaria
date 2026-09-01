from django import forms
from .models import Categoria, Cliente, ItemPedido, Pedido, Produto


# Formulario usado para criar e editar categorias.
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'ativo']


# Formulario usado para criar e editar produtos.
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['categoria', 'nome', 'descricao', 'preco', 'ativo']


# Formulario usado para criar e editar clientes.
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['username', 'first_name', 'last_name', 'email', 'telefone', 'endereco']


# Formulario usado para criar e editar pedidos.
class PedidoForm(forms.ModelForm):
    data_entrega = forms.DateTimeField(
        required=False,
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        ),
    )

    class Meta:
        model = Pedido
        fields = ['cliente', 'data_entrega', 'status', 'observacao']


# Formulario usado para criar e editar itens de pedido.
class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['pedido', 'produto', 'quantidade']
