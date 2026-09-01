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
        fields = ['nome', 'telefone', 'email', 'endereco']


