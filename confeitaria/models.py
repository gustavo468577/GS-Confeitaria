from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="produtos"
    )
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    endereco = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Pedido(models.Model):

    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        PRODUCAO = "PRODUCAO", "Em produção"
        PRONTO = "PRONTO", "Pronto"
        ENTREGUE = "ENTREGUE", "Entregue"
        CANCELADO = "CANCELADO", "Cancelado"

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="pedidos"
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="pedidos_registrados"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    data_entrega = models.DateTimeField(null=True, blank=True)
    observacao = models.TextField(blank=True)

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.itens.all())

    def confirmar(self):
        self.status = self.Status.PRODUCAO
        self.save()

    def finalizar(self):
        self.status = self.Status.ENTREGUE
        self.save()

    def cancelar(self):
        self.status = self.Status.CANCELADO
        self.save()

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nome}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="itens"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="itens_pedido"
    )

    quantidade = models.PositiveIntegerField(default=1)

    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def calcular_subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}x"