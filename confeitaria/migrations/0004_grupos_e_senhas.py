from django.contrib.auth.hashers import make_password
from django.db import migrations


def configurar_acessos(apps, schema_editor):
    db = schema_editor.connection.alias
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    User = apps.get_model('auth', 'User')
    funcionarios, _ = Group.objects.using(db).get_or_create(name='Funcionarios')
    gerentes, _ = Group.objects.using(db).get_or_create(name='Gerentes')
    for model in ['categoria', 'produto', 'cliente', 'pedido', 'itempedido']:
        content_type, _ = ContentType.objects.using(db).get_or_create(app_label='confeitaria', model=model)
        for action in ['view', 'add', 'change', 'delete']:
            permission, _ = Permission.objects.using(db).get_or_create(
                content_type=content_type, codename=f'{action}_{model}',
                defaults={'name': f'Can {action} {model}'},
            )
            gerentes.permissions.add(permission)
            if action == 'view' or (model in ['cliente', 'pedido', 'itempedido'] and action in ['add', 'change']):
                funcionarios.permissions.add(permission)
    # Uma conta sem senha definida nao deve conter um hash vazio/invalido.
    User.objects.using(db).filter(password='').update(password=make_password(None))


class Migration(migrations.Migration):
    dependencies = [
        ('confeitaria', '0003_alter_cliente_options_alter_cliente_managers_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]
    operations = [migrations.RunPython(configurar_acessos, migrations.RunPython.noop)]
