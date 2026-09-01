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
    list_display = ("nome", "telefone", "email", "endereco")
    search_fields = ("nome", "telefone", "email", "endereco")


# Permite cadastrar itens diretamente dentro do pedido no Admin.
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    autocomplete_fields = ("produto",)


# Configura a exibicao de pedidos no Django Admin.
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "usuario", "criado_em",
                    "data_entrega", "status", "total")
    list_filter = ("status", "criado_em", "data_entrega")
    search_fields = (
        "id",
        "cliente__nome",
        "cliente__telefone",
        "cliente__email",
        "usuario__username",
    )
    autocomplete_fields = ("cliente", "usuario")
    date_hierarchy = "criado_em"
    inlines = (ItemPedidoInline,)

    # Mostra o total calculado do pedido na listagem do Admin.
    def total(self, obj):
        return obj.calcular_total()


# Configura a exibicao de itens de pedido no Django Admin.
@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "produto", "quantidade",
                    "preco_unitario", "subtotal")
    list_filter = ("produto",)
    search_fields = ("pedido__id", "produto__nome")
    autocomplete_fields = ("pedido", "produto")

    # Mostra o subtotal calculado do item na listagem do Admin.
    def subtotal(self, obj):
        return obj.calcular_subtotal()
