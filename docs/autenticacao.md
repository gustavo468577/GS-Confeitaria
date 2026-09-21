# Autenticacao e permissoes

Todas as URLs exigem login, exceto login, cadastro e as excecoes internas do Django admin.
O cadastro publico cria somente clientes, com senha criptograficamente derivada pelo Django.

| Perfil | Acesso |
| --- | --- |
| Cliente | Catalogo ativo, proprio perfil e proprios pedidos/itens. Cria pedidos e altera/exclui os proprios enquanto PENDENTE. |
| Funcionarios | Consulta catalogo; consulta, cria e edita clientes comuns, pedidos e itens. Sem exclusao global. |
| Gerentes | Todas as permissoes dos cinco modelos comerciais. |
| Superusuario | Tambem administra usuarios, senhas, privilegios e grupos. |

As permissoes globais sao verificadas por acao. Sem elas, pedidos/itens ficam limitados ao dono; registros fora do escopo retornam 404. Operacoes administrativas proibidas retornam 403. Login e exigido antes dessas verificacoes.

## Aplicar e verificar

```powershell
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py test confeitaria
```

A migracao 0004 cria Funcionarios e Gerentes, mas nao inclui usuarios automaticamente. Um superusuario deve atribuir os grupos em /admin/auth/user/. Marque is_staff somente para quem realmente precisa entrar no Django admin; o acesso as views comuns depende das permissoes, nao dessa flag.

Contas antigas com senha vazia recebem uma senha inutilizavel. O superusuario pode definir uma nova senha pela tela de usuarios do admin ou por `manage.py changepassword USUARIO`. As senhas validas sao preservadas.

Clientes continuam usando a estrutura Cliente(User) existente; nenhuma tabela e remodelada. O admin de clientes aceita somente dados de perfil e exige senha na criacao. Contas privilegiadas sao ocultadas desse CRUD para quem nao e superusuario.

## Publicacao

Configure DJANGO_DEBUG=false, DJANGO_SECRET_KEY com uma chave privada nova e DJANGO_ALLOWED_HOSTS com os dominios separados por virgula. Fora do modo de desenvolvimento, HTTPS e cookies seguros ficam obrigatorios. A chave de desenvolvimento nao deve ser usada em producao. A mudanca da chave invalida sessoes existentes.

As alteracoes tratam autenticacao e autorizacao. Regras comerciais de preco historico e exclusoes em cascata permanecem como no modelo atual.
