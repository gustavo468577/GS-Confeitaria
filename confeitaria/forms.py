from django import forms
from django.shortcuts import get_object_or_404
from .access import pedidos_permitidos
from .models import Categoria, Cliente, ItemPedido, Pedido, Produto
from django.contrib.auth.forms import UserCreationForm




# Formulario usado para criar e editar categorias.
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'ativo']


# Formulario usado para criar e editar produtos.
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['categoria', 'nome', 'descricao', 'preco', 'ativo', 'imagem', 'imagem_externa']


# Formulario usado para criar e editar clientes.
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['username', 'first_name', 'last_name', 'email', 'telefone', 'endereco']


# Formulario usado para criar e editar pedidos.
class PedidoForm(forms.ModelForm):
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        acao = 'add' if self.instance._state.adding else 'change'
        if not user.has_perm(f'confeitaria.{acao}_pedido'):
            self.fields.pop('cliente')
            self.fields.pop('status')
            self.instance.cliente = get_object_or_404(Cliente, pk=user.pk)
            if self.instance._state.adding:
                self.instance.status = Pedido.Status.PENDENTE

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
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        acao = 'add' if self.instance._state.adding else 'change'
        permissao = f'{acao}_itempedido'
        self.fields['pedido'].queryset = pedidos_permitidos(user, permissao)
        if not user.has_perm(f'confeitaria.{permissao}'):
            self.fields['produto'].queryset = Produto.objects.filter(ativo=True, categoria__ativo=True)
        self.fields['quantidade'].min_value = 1

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']
        if quantidade < 1:
            raise forms.ValidationError('Informe ao menos uma unidade.')
        return quantidade

    class Meta:
        model = ItemPedido
        fields = ['pedido', 'produto', 'quantidade']

#formulario de cadastro de usuario
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'telefone',
            'endereco',
        ]
