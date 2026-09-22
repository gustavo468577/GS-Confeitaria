"""Permissoes globais para a equipe; propriedade dos registros para clientes."""
from functools import wraps

from django.core.exceptions import PermissionDenied

from .models import Cliente, Pedido


def clientes_permitidos(user, acao='view'):
    clientes = Cliente.objects.all()
    if user.has_perm(f'confeitaria.{acao}_cliente'):
        # Dados de contas privilegiadas ficam reservados ao superusuario.
        return clientes if user.is_superuser else clientes.filter(is_staff=False, is_superuser=False)
    return clientes.filter(pk=user.pk)


def pedidos_permitidos(user, permissao='view_pedido'):
    pedidos = Pedido.objects.all()
    if user.has_perm(f'confeitaria.{permissao}'):
        return pedidos
    pedidos = pedidos.filter(cliente_id=user.pk)
    if not permissao.startswith('view_'):
        pedidos = pedidos.filter(status=Pedido.Status.PENDENTE)
    return pedidos


def administrador_required(view):
    """Restrict administrative pages without replacing action permissions."""
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        user = request.user
        if not user.is_active or not (user.is_staff or user.is_superuser):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapped
