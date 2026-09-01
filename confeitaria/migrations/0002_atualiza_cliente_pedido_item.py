# Generated manually to preserve data while aligning the database with the models.

import re

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def _unique_username(User, base_username):
    base_username = re.sub(r"[^A-Za-z0-9_@.+-]", "_", base_username).strip("_")
    base_username = base_username[:120] or "cliente"

    username = base_username
    suffix = 1
    while User.objects.filter(username=username).exists():
        suffix += 1
        username = f"{base_username}_{suffix}"[:150]
    return username


def atualizar_tabelas(apps, schema_editor):
    User = apps.get_model("auth", "User")
    connection = schema_editor.connection

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, telefone, email, endereco FROM confeitaria_cliente")
        clientes = cursor.fetchall()
        cursor.execute(
            "SELECT id, status, criado_em, data_entrega, observacao, cliente_id "
            "FROM confeitaria_pedido"
        )
        pedidos = cursor.fetchall()
        cursor.execute("SELECT id, quantidade, pedido_id, produto_id FROM confeitaria_itempedido")
        itens = cursor.fetchall()

    cliente_id_para_usuario_id = {}
    for cliente_id, nome, telefone, email, endereco in clientes:
        username_base = email.split("@")[0] if email else f"cliente_{cliente_id}"
        user = User.objects.create(
            username=_unique_username(User, username_base),
            first_name=nome or "",
            email=email or "",
            is_active=True,
        )
        cliente_id_para_usuario_id[cliente_id] = user.pk

    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = OFF")

        cursor.execute(
            """
            CREATE TABLE confeitaria_cliente_new (
                user_ptr_id integer NOT NULL PRIMARY KEY
                    REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED,
                telefone varchar(20) NOT NULL,
                endereco varchar(200) NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE confeitaria_pedido_new (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                status varchar(20) NOT NULL,
                criado_em datetime NOT NULL,
                data_entrega datetime NULL,
                observacao text NOT NULL,
                cliente_id bigint NOT NULL
                    REFERENCES confeitaria_cliente(user_ptr_id) DEFERRABLE INITIALLY DEFERRED
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE confeitaria_itempedido_new (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                quantidade integer unsigned NOT NULL CHECK (quantidade >= 0),
                pedido_id bigint NOT NULL
                    REFERENCES confeitaria_pedido(id) DEFERRABLE INITIALLY DEFERRED,
                produto_id bigint NOT NULL
                    REFERENCES confeitaria_produto(id) DEFERRABLE INITIALLY DEFERRED
            )
            """
        )

        cursor.executemany(
            "INSERT INTO confeitaria_cliente_new (user_ptr_id, telefone, endereco) VALUES (%s, %s, %s)",
            [
                (cliente_id_para_usuario_id[cliente_id], telefone, endereco)
                for cliente_id, nome, telefone, email, endereco in clientes
            ],
        )
        cursor.executemany(
            """
            INSERT INTO confeitaria_pedido_new
                (id, status, criado_em, data_entrega, observacao, cliente_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            [
                (
                    pedido_id,
                    status,
                    criado_em,
                    data_entrega,
                    observacao,
                    cliente_id_para_usuario_id[cliente_id],
                )
                for pedido_id, status, criado_em, data_entrega, observacao, cliente_id in pedidos
            ],
        )
        cursor.executemany(
            """
            INSERT INTO confeitaria_itempedido_new
                (id, quantidade, pedido_id, produto_id)
            VALUES (%s, %s, %s, %s)
            """,
            itens,
        )

        cursor.execute("DROP TABLE confeitaria_itempedido")
        cursor.execute("DROP TABLE confeitaria_pedido")
        cursor.execute("DROP TABLE confeitaria_cliente")
        cursor.execute("ALTER TABLE confeitaria_cliente_new RENAME TO confeitaria_cliente")
        cursor.execute("ALTER TABLE confeitaria_pedido_new RENAME TO confeitaria_pedido")
        cursor.execute("ALTER TABLE confeitaria_itempedido_new RENAME TO confeitaria_itempedido")
        cursor.execute("CREATE INDEX confeitaria_pedido_cliente_id_idx ON confeitaria_pedido (cliente_id)")
        cursor.execute("CREATE INDEX confeitaria_itempedido_pedido_id_idx ON confeitaria_itempedido (pedido_id)")
        cursor.execute("CREATE INDEX confeitaria_itempedido_produto_id_idx ON confeitaria_itempedido (produto_id)")
        cursor.execute("PRAGMA foreign_keys = ON")


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ("confeitaria", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(atualizar_tabelas, migrations.RunPython.noop),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="cliente",
                    name="user_ptr",
                    field=models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="+",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                migrations.RemoveField(
                    model_name="pedido",
                    name="usuario",
                ),
                migrations.RemoveField(
                    model_name="itempedido",
                    name="preco_unitario",
                ),
                migrations.RemoveField(
                    model_name="cliente",
                    name="email",
                ),
                migrations.RemoveField(
                    model_name="cliente",
                    name="nome",
                ),
                migrations.RemoveField(
                    model_name="cliente",
                    name="id",
                ),
            ],
        ),
    ]
