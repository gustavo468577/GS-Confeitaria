# GS Confeitaria

Aplicação web para gerenciamento de uma confeitaria, desenvolvida com Django. Reúne catálogo de produtos, cadastro de clientes e controle de pedidos, com acesso conforme as permissões de cada usuário.

## Funcionalidades

- Cadastro e autenticação de clientes.
- Catálogo de produtos com filtro por categoria.
- Imagens de produtos por upload ou endereço externo.
- Gerenciamento de categorias, produtos e clientes.
- Criação e acompanhamento de pedidos e seus itens.
- Cálculo de subtotais e do total dos pedidos.
- Controle de acesso para clientes, funcionários, gerentes e superusuários.
- Painel administrativo do Django.

## Tecnologias

- Python e Django (versão fixada em `requiremets.txt`).
- SQLite como banco de dados local.
- Pillow para processamento de imagens.
- HTML, CSS, JavaScript e Bootstrap, com interface baseada no tema Feane.

## Como executar localmente

Com Python 3, pip e suporte a ambientes virtuais instalados, abra um terminal na pasta do projeto.

### 1. Crie e ative um ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instale as dependências

```bash
python -m pip install -r requiremets.txt
```

O arquivo de dependências se chama `requiremets.txt` neste repositório; use esse nome no comando.

### 3. Prepare o banco e crie uma conta administrativa

```bash
python manage.py migrate
python manage.py createsuperuser
```

As migrações criam as tabelas e os grupos `Funcionarios` e `Gerentes`. O banco SQLite é armazenado em `db.sqlite3`.

### 4. Inicie o servidor

```bash
python manage.py runserver
```

Acesse [http://127.0.0.1:8000/](http://127.0.0.1:8000/). As páginas da aplicação exigem login; novos clientes podem se cadastrar em `/cadastro/`.

## Primeiros passos

1. Entre em `/admin/` com o superusuário criado.
2. Cadastre categorias e produtos. Mantenha ambos ativos para que apareçam no catálogo dos clientes.
3. Para experimentar o fluxo de compra, saia da conta administrativa e crie uma conta de cliente em `/cadastro/`.
4. Crie um pedido em `/pedidos/criar/` e adicione produtos em `/itens-pedido/criar/`.
5. Acompanhe os pedidos em `/pedidos/`.

Na interface da aplicação, o superusuário não pode criar pedidos ou itens. Use uma conta de cliente para esse fluxo.

### Perfis de acesso

| Perfil | Acesso |
| --- | --- |
| Cliente | Consulta o catálogo ativo e seus próprios pedidos; alterações nos pedidos e itens ficam restritas a pedidos pendentes. |
| Funcionarios | Consulta os registros e recebe permissões para criar e editar clientes, pedidos e itens. |
| Gerentes | Recebe permissões de consulta, criação, edição e exclusão dos cinco modelos da aplicação. |
| Superusuário | Administra usuários, grupos e permissões pelo painel administrativo. |

O superusuário pode atribuir grupos em `/admin/`. Para acessar o painel administrativo e as páginas de categorias, a conta também precisa estar marcada como membro da equipe (`is_staff`), além das permissões correspondentes.

## Rotas principais

| Caminho | Página |
| --- | --- |
| `/` | Início |
| `/cadastro/` | Cadastro de cliente |
| `/login/` | Login |
| `/produtos/` | Catálogo de produtos |
| `/categorias/` | Gerenciamento de categorias |
| `/clientes/` | Gerenciamento de clientes |
| `/pedidos/` | Pedidos |
| `/itens-pedido/` | Itens dos pedidos |
| `/admin/` | Administração do Django |

## Configuração

As configurações ficam em `config/settings.py`. As seguintes variáveis são lidas do ambiente:

| Variável | Padrão | Finalidade |
| --- | --- | --- |
| `DJANGO_DEBUG` | `true` | Ativa o modo de desenvolvimento; use `false` para desativá-lo. |
| `DJANGO_SECRET_KEY` | Chave local de desenvolvimento | Obrigatória quando `DJANGO_DEBUG=false`. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Hosts permitidos, separados por vírgula, sem espaços. |

O projeto não carrega arquivos `.env` automaticamente. Defina as variáveis no terminal ou no ambiente que executa a aplicação.

Uploads são gravados em `media/`. Arquivos estáticos estão em `confeitaria/static/`, e `collectstatic` os reúne em `staticfiles/`. Com o modo de desenvolvimento desativado, a configuração exige HTTPS; arquivos estáticos e uploads precisam ser servidos pela infraestrutura de hospedagem.

## Estrutura do projeto

```text
GS-Confeitaria/
├── config/                 # Configurações e rotas principais
├── confeitaria/
│   ├── migrations/         # Migrações do banco de dados
│   ├── static/             # CSS, JavaScript, fontes e imagens
│   ├── templates/          # Páginas HTML
│   ├── access.py           # Regras de acesso aos registros
│   ├── admin.py            # Painel administrativo
│   ├── forms.py            # Formulários
│   ├── models.py           # Modelos de dados
│   ├── urls.py             # Rotas da aplicação
│   └── views.py            # Lógica das páginas
├── docs/                   # Diagrama do projeto
├── manage.py               # Comandos do Django
└── requiremets.txt         # Dependências Python
```

## Verificação da configuração

Com as dependências instaladas e o ambiente virtual ativo:

```bash
python manage.py check
```

## Diagrama

![Diagrama do projeto](docs/Diagrama%20sem%20nome.drawio.png)
