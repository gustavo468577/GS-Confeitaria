from django.contrib import admin
from django.contrib.auth.models import Group, Permission, User
from django.test import Client as HttpClient, RequestFactory, TestCase
from django.urls import reverse

from .models import Categoria, Cliente, ItemPedido, Pedido, Produto


class AcessoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ana = Cliente.objects.create_user(username='ana', password='Senha-segura-928!', telefone='1', endereco='A')
        cls.bia = Cliente.objects.create_user(username='bia', password='Senha-segura-928!', telefone='2', endereco='B')
        cls.equipe = User.objects.create_user(username='equipe', password='Senha-segura-928!', is_staff=True)
        cls.categoria = Categoria.objects.create(nome='Bolos')
        cls.produto = Produto.objects.create(nome='Chocolate', categoria=cls.categoria, preco=10)
        cls.pedido = Pedido.objects.create(cliente=cls.ana)
        cls.outro = Pedido.objects.create(cliente=cls.bia)
        cls.item = ItemPedido.objects.create(pedido=cls.pedido, produto=cls.produto)
        cls.outro_item = ItemPedido.objects.create(pedido=cls.outro, produto=cls.produto)

    def permitir(self, *codenames):
        self.equipe.user_permissions.add(*Permission.objects.filter(
            content_type__app_label='confeitaria', codename__in=codenames,
        ))
        self.client.force_login(self.equipe)

    def test_visitante_nao_acessa_cruds_por_get_ou_post(self):
        objetos = {'categoria': self.categoria, 'produto': self.produto, 'cliente': self.ana,
                   'pedido': self.pedido, 'item_pedido': self.item}
        for nome, objeto in objetos.items():
            for acao in ['listar', 'criar', 'detalhar', 'editar', 'excluir']:
                url = reverse(f'{nome}_{acao}', args=[] if acao in ['listar', 'criar'] else [objeto.pk])
                for metodo in [self.client.get, self.client.post]:
                    with self.subTest(url=url, metodo=metodo.__name__):
                        response = metodo(url)
                        self.assertEqual(response.status_code, 302)
                        self.assertTrue(response.url.startswith('/login/?next='))
        self.assertEqual(Pedido.objects.count(), 2)

    def test_login_cadastro_publicos_inicio_privado(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)
        self.assertEqual(self.client.get(reverse('cadastro')).status_code, 200)
        self.assertEqual(self.client.get(reverse('inicio')).status_code, 302)

    def test_login_respeita_next_local_e_rejeita_externo(self):
        for destino, esperado in [('/pedidos/', '/pedidos/'), ('https://example.org/', '/')]:
            self.client.logout()
            response = self.client.post(reverse('login'), {'username': 'ana', 'password': 'Senha-segura-928!', 'next': destino})
            self.assertRedirects(response, esperado, fetch_redirect_response=False)

    def test_cadastro_nao_aceita_privilegios(self):
        response = self.client.post(reverse('cadastro'), {
            'username': 'novo', 'password1': 'Senha-nova-segura-298!', 'password2': 'Senha-nova-segura-298!',
            'telefone': '3', 'endereco': 'C', 'is_staff': 'on', 'is_superuser': 'on',
            'groups': Group.objects.get(name='Gerentes').pk,
        })
        self.assertEqual(response.status_code, 302)
        novo = Cliente.objects.get(username='novo')
        self.assertTrue(novo.check_password('Senha-nova-segura-298!'))
        self.assertFalse(novo.is_staff or novo.is_superuser or novo.groups.exists())
        self.assertEqual(self.client.get(reverse('produto_criar')).status_code, 403)

    def test_cliente_nao_gerencia_catalogo_ou_clientes(self):
        self.client.force_login(self.ana)
        for nome, objeto in [('categoria', self.categoria), ('produto', self.produto)]:
            for acao in ['criar', 'editar', 'excluir']:
                url = reverse(f'{nome}_{acao}', args=[] if acao == 'criar' else [objeto.pk])
                self.assertEqual(self.client.get(url).status_code, 403)
                self.assertEqual(self.client.post(url).status_code, 403)
        self.assertEqual(self.client.get(reverse('cliente_listar')).status_code, 403)
        self.assertEqual(self.client.post(reverse('cliente_criar')).status_code, 403)
        self.assertEqual(self.client.post(reverse('cliente_excluir', args=[self.ana.pk])).status_code, 403)

    def test_cliente_so_acessa_seus_registros(self):
        self.client.force_login(self.ana)
        response = self.client.get(reverse('pedido_listar'))
        self.assertEqual(list(response.context['pedidos']), [self.pedido])
        response = self.client.get(reverse('item_pedido_listar'))
        self.assertEqual(list(response.context['itens_pedido']), [self.item])
        for nome, objeto in [('pedido', self.outro), ('item_pedido', self.outro_item), ('cliente', self.bia)]:
            for acao in ['detalhar', 'editar']:
                url = reverse(f'{nome}_{acao}', args=[objeto.pk])
                self.assertEqual(self.client.get(url).status_code, 404)
                self.assertEqual(self.client.post(url, {'observacao': 'invadido'}).status_code, 404)
        for nome, objeto in [('pedido', self.outro), ('item_pedido', self.outro_item)]:
            self.assertEqual(self.client.post(reverse(f'{nome}_excluir', args=[objeto.pk])).status_code, 404)
        self.outro.refresh_from_db()
        self.assertEqual(self.outro.observacao, '')

    def test_pedido_ignora_cliente_e_status_forjados(self):
        self.client.force_login(self.ana)
        response = self.client.post(reverse('pedido_criar'), {
            'cliente': self.bia.pk, 'status': 'ENTREGUE', 'observacao': 'meu pedido',
        })
        self.assertEqual(response.status_code, 302)
        pedido = Pedido.objects.latest('pk')
        self.assertEqual(pedido.cliente_id, self.ana.pk)
        self.assertEqual(pedido.status, Pedido.Status.PENDENTE)
        response = self.client.post(reverse('pedido_editar', args=[pedido.pk]), {
            'cliente': self.bia.pk, 'status': 'ENTREGUE', 'observacao': 'editado',
        })
        self.assertEqual(response.status_code, 302)
        pedido.refresh_from_db()
        self.assertEqual(pedido.cliente_id, self.ana.pk)
        self.assertEqual(pedido.status, Pedido.Status.PENDENTE)

    def test_item_rejeita_pedido_alheio_e_quantidade_zero(self):
        self.client.force_login(self.ana)
        for pedido, quantidade in [(self.outro, 1), (self.pedido, 0)]:
            response = self.client.post(reverse('item_pedido_criar'), {
                'pedido': pedido.pk, 'produto': self.produto.pk, 'quantidade': quantidade,
            })
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].errors)
        response = self.client.post(reverse('item_pedido_editar', args=[self.item.pk]), {
            'pedido': self.outro.pk, 'produto': self.produto.pk, 'quantidade': 2,
        })
        self.assertTrue(response.context['form'].errors)
        self.item.refresh_from_db()
        self.assertEqual(self.item.pedido_id, self.pedido.pk)
        self.assertEqual(ItemPedido.objects.count(), 2)

    def test_cliente_pode_incluir_e_excluir_item_proprio_pendente(self):
        self.client.force_login(self.ana)
        response = self.client.post(reverse('item_pedido_criar'), {
            'pedido': self.pedido.pk, 'produto': self.produto.pk, 'quantidade': 2,
        })
        self.assertEqual(response.status_code, 302)
        item = ItemPedido.objects.latest('pk')
        self.assertEqual(self.client.post(reverse('item_pedido_excluir', args=[item.pk])).status_code, 302)
        self.assertFalse(ItemPedido.objects.filter(pk=item.pk).exists())

    def test_pedidos_nao_pendentes_bloqueiam_alteracoes_do_cliente(self):
        self.client.force_login(self.ana)
        for status in ['PRODUCAO', 'PRONTO', 'ENTREGUE', 'CANCELADO']:
            Pedido.objects.filter(pk=self.pedido.pk).update(status=status)
            for nome, objeto in [('pedido', self.pedido), ('item_pedido', self.item)]:
                for acao in ['editar', 'excluir']:
                    self.assertEqual(self.client.post(reverse(f'{nome}_{acao}', args=[objeto.pk])).status_code, 404)
            response = self.client.post(reverse('item_pedido_criar'), {
                'pedido': self.pedido.pk, 'produto': self.produto.pk, 'quantidade': 1,
            })
            self.assertTrue(response.context['form'].errors)

    def test_funcionario_precisa_da_permissao_da_acao(self):
        self.permitir('view_pedido', 'change_pedido')
        self.assertEqual(len(self.client.get(reverse('pedido_listar')).context['pedidos']), 2)
        response = self.client.post(reverse('pedido_editar', args=[self.outro.pk]), {
            'cliente': self.bia.pk, 'status': 'PRODUCAO', 'observacao': 'autorizado',
        })
        self.assertEqual(response.status_code, 302)
        self.outro.refresh_from_db()
        self.assertEqual(self.outro.status, 'PRODUCAO')
        self.assertEqual(self.client.post(reverse('pedido_excluir', args=[self.outro.pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse('produto_criar')).status_code, 403)

    def test_admin_cliente_nao_expoe_privilegios_ou_hash(self):
        self.permitir('view_cliente', 'change_cliente', 'add_cliente')
        request = RequestFactory().get('/admin/')
        request.user = User.objects.get(pk=self.equipe.pk)
        model_admin = admin.site._registry[Cliente]
        for objeto in [None, self.ana]:
            fields = model_admin.get_form(request, objeto).base_fields
            self.assertFalse({'password', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_active'} & fields.keys())
        self.assertIn('password1', model_admin.get_form(request).base_fields)
        self.assertFalse(admin.site._registry[User].has_change_permission(request))
        self.assertFalse(admin.site._registry[Group].has_change_permission(request))
        response = self.client.post(reverse('admin:confeitaria_cliente_change', args=[self.ana.pk]), {
            'username': 'ana', 'telefone': '1', 'endereco': 'A', 'is_superuser': 'on', 'is_staff': 'on',
        })
        self.assertEqual(response.status_code, 302)
        self.ana.refresh_from_db()
        self.assertFalse(self.ana.is_staff or self.ana.is_superuser)
        self.assertTrue(self.ana.check_password('Senha-segura-928!'))

    def test_admin_cria_cliente_com_senha_valida(self):
        self.permitir('add_cliente')
        response = self.client.post(reverse('admin:confeitaria_cliente_add'), {
            'username': 'viaadmin', 'telefone': '3', 'endereco': 'C',
            'password1': 'Senha-admin-segura-928!', 'password2': 'Senha-admin-segura-928!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Cliente.objects.get(username='viaadmin').check_password('Senha-admin-segura-928!'))

    def test_grupos_tem_permissoes_distintas(self):
        funcionarios = Group.objects.get(name='Funcionarios')
        gerentes = Group.objects.get(name='Gerentes')
        self.assertFalse(funcionarios.permissions.filter(codename__startswith='delete_').exists())
        self.assertEqual(gerentes.permissions.filter(content_type__app_label='confeitaria').count(), 20)
        self.equipe.groups.add(funcionarios)
        self.client.force_login(self.equipe)
        self.assertEqual(self.client.get(reverse('pedido_editar', args=[self.outro.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse('produto_criar')).status_code, 403)
        self.equipe.groups.add(gerentes)
        self.assertEqual(self.client.get(reverse('produto_criar')).status_code, 200)

    def test_logout_exige_post_e_csrf(self):
        client = HttpClient(enforce_csrf_checks=True)
        client.force_login(self.ana)
        self.assertEqual(client.get(reverse('logout')).status_code, 405)
        self.assertEqual(client.post(reverse('logout')).status_code, 403)
        client.get(reverse('inicio'))
        response = client.post(reverse('logout'), {'csrfmiddlewaretoken': client.cookies['csrftoken'].value})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(client.get(reverse('pedido_listar')).status_code, 302)

    def test_menus_nao_oferecem_gestao_ao_cliente(self):
        self.client.force_login(self.ana)
        self.assertNotContains(self.client.get(reverse('produto_listar')), reverse('produto_criar'))
        self.assertNotContains(self.client.get(reverse('inicio')), 'href="/clientes/"')


    def test_edicao_do_proprio_perfil_preserva_senha_e_privilegios(self):
        self.client.force_login(self.ana)
        response = self.client.post(reverse('cliente_editar', args=[self.ana.pk]), {
            'username': 'ana', 'telefone': '99', 'endereco': 'Novo endereco',
            'password': 'injetada', 'is_superuser': 'on', 'is_staff': 'on',
            'groups': Group.objects.get(name='Gerentes').pk,
        })
        self.assertEqual(response.status_code, 302)
        self.ana.refresh_from_db()
        self.assertEqual(self.ana.telefone, '99')
        self.assertTrue(self.ana.check_password('Senha-segura-928!'))
        self.assertFalse(self.ana.is_staff or self.ana.is_superuser or self.ana.groups.exists())

    def test_equipe_nao_acessa_cliente_privilegiado_nem_admin_de_usuarios(self):
        Cliente.objects.filter(pk=self.bia.pk).update(is_staff=True)
        self.permitir('view_cliente', 'change_cliente', 'delete_cliente')
        for acao in ['detalhar', 'editar', 'excluir']:
            self.assertEqual(self.client.get(reverse(f'cliente_{acao}', args=[self.bia.pk])).status_code, 404)
            self.assertEqual(self.client.post(reverse(f'cliente_{acao}', args=[self.bia.pk])).status_code, 404)
        # Nem permissao auth atribuida por engano permite gerir privilegios.
        self.equipe.user_permissions.add(*Permission.objects.filter(content_type__app_label='auth'))
        for model in ['user', 'group']:
            self.assertEqual(self.client.get(reverse(f'admin:auth_{model}_changelist')).status_code, 403)
        response = self.client.get(reverse('admin:confeitaria_cliente_change', args=[self.bia.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('original', response.context or {})
        self.assertTrue(Cliente.objects.filter(pk=self.bia.pk).exists())

    def test_senha_incorreta_e_conta_inativa_nao_autenticam(self):
        for senha, ativo in [('incorreta', True), ('Senha-segura-928!', False)]:
            User.objects.filter(pk=self.ana.pk).update(is_active=ativo)
            response = self.client.post(reverse('login'), {'username': 'ana', 'password': senha})
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('_auth_user_id', self.client.session)

    def test_catalogo_inativo_nao_e_oferecido_ao_cliente(self):
        self.client.force_login(self.ana)
        Produto.objects.filter(pk=self.produto.pk).update(ativo=False)
        self.assertEqual(self.client.get(reverse('produto_detalhar', args=[self.produto.pk])).status_code, 404)
        self.assertEqual(list(self.client.get(reverse('produto_listar')).context['produtos']), [])
        response = self.client.post(reverse('item_pedido_criar'), {
            'pedido': self.pedido.pk, 'produto': self.produto.pk, 'quantidade': 1,
        })
        self.assertTrue(response.context['form'].errors)
        # O historico do proprio pedido continua acessivel.
        self.assertEqual(self.client.get(reverse('pedido_detalhar', args=[self.pedido.pk])).status_code, 200)

    def test_migracao_repara_apenas_senhas_vazias_sem_promover_usuarios(self):
        from importlib import import_module
        from django.apps import apps
        from django.db import connection
        from types import SimpleNamespace
        usuario = User.objects.create(username='sem_senha', password='')
        configurar = import_module('confeitaria.migrations.0004_grupos_e_senhas').configurar_acessos
        configurar(apps, SimpleNamespace(connection=connection))
        configurar(apps, SimpleNamespace(connection=connection))
        usuario.refresh_from_db()
        self.assertFalse(usuario.has_usable_password())
        self.assertFalse(usuario.is_staff or usuario.is_superuser or usuario.groups.exists())
        self.ana.refresh_from_db()
        self.assertTrue(self.ana.check_password('Senha-segura-928!'))
        self.assertEqual(Group.objects.filter(name__in=['Funcionarios', 'Gerentes']).count(), 2)
