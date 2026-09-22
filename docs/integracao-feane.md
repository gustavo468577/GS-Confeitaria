# Interface da confeitaria

O Feane fornece a base visual dos templates Django. As rotas e os cinco CRUDs permanecem independentes.
Templates compartilhados em confeitaria/templates/confeitaria: base, formulários, exclusões e includes.
Arquivos estáticos em confeitaria/static/feane e confeitaria/static/confeitaria.

## Categorias

Todas as páginas de categorias exigem conta ativa com is_staff ou is_superuser,
além da permissão Django da ação (view/add/change/delete). O acesso direto sem autorização
retorna 403. Visitantes continuam sendo enviados ao login pelo middleware.
Os links de categorias ficam ocultos para clientes. Os filtros do catálogo continuam disponíveis.

## Comprar

Cards e detalhes mostram Comprar para contas Cliente em produtos e categorias ativos.
O link abre item_pedido_criar?produto=<id> e seleciona o produto no formulário.
O ID é validado contra os produtos permitidos para o usuário; IDs inválidos ou inacessíveis
retornam 404. Em POST, os dados enviados e as validações originais do formulário prevalecem.
O cliente ainda escolhe um pedido existente e pendente. Nenhum pedido é criado automaticamente.

## Imagens

Produto.imagem_url usa upload, URL externa HTTP/HTTPS ou imagem padrão, nessa ordem.
A migration 0005 acrescenta campos opcionais e mantém os registros existentes.
A foto do bolo fornecida em assets foi transferida para
confeitaria/static/confeitaria/images/bolo-inicio.png e aparece na página inicial.

## Static e media

STATIC_URL=/static/, STATIC_ROOT=staticfiles/, MEDIA_URL=/media/, MEDIA_ROOT=media/.
Em desenvolvimento, runserver serve static e o URLconf serve media em DEBUG.
Na publicação, configure o servidor/storage e execute collectstatic.
Google Fonts continua sendo usado pelo CSS Feane; as demais dependências visuais são locais.

## Limpeza

A pasta assets continha referências e cópias dos arquivos já integrados em static.
Ela foi removida depois de preservar a nova imagem. Também foram removidos, a pedido do usuário,
os arquivos tests.py e tests_frontend.py, o script de teste visual e suas capturas.
As migrations, bibliotecas utilizadas, arquivos enviados e regras funcionais foram mantidos.
