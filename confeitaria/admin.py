from django.contrib import admin

from .models import Categoria, Cliente, ItemPedido, Pedido, Produto

# REGISTROS DAS TABELAS NO DJANGO ADMIN


# Configura a exibicao de categorias no Django Admin.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao", "ativo")
    list_filter = ("ativo",)
    search_fields = ("nome", "descricao")


# Configura a exibicao de produtos no Django Admin.
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "preco", "ativo")
    list_filter = ("categoria", "ativo")
    search_fields = ("nome", "descricao", "categoria__nome")
    list_editable = ("preco", "ativo")

 
# Configura a exibicao de clientes no Django Admin.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "telefone", "endereco")
    search_fields = ("username", "first_name", "last_name", "email", "telefone", "endereco")


# Permite cadastrar itens diretamente dentro do pedido no Admin.
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    autocomplete_fields = ("produto",)


# Configura a exibicao de pedidos no Django Admin.
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "criado_em", "data_entrega", "status", "total")
    list_filter = ("status", "criado_em", "data_entrega")
    search_fields = (
        "id",
        "cliente__username",
        "cliente__first_name",
        "cliente__last_name",
        "cliente__telefone",
        "cliente__email",
    )
    autocomplete_fields = ("cliente",)
    date_hierarchy = "criado_em"
    inlines = (ItemPedidoInline,)

    # Mostra o total calculado do pedido na listagem do Admin.
    def total(self, obj):
        return obj.calcular_total()


# Configura a exibicao de itens de pedido no Django Admin.
@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "produto", "quantidade", "valor_unitario", "subtotal")
    list_filter = ("produto",)
    search_fields = ("pedido__id", "produto__nome")
    autocomplete_fields = ("pedido", "produto")

    # Mostra o subtotal calculado do item na listagem do Admin.
    def subtotal(self, obj):
        return obj.calcular_subtotal()

    # Mostra o valor unitario vindo do produto.
    def valor_unitario(self, obj):
        return obj.produto.preco
