# flashcards
Backend para um aplicativo de flashcards desenvolvido para a cadeira DLSC817 - Desenvolvimento de Software Educacional

![banco de dados](db.png)

## Pacotes
1. django
2. djangorestframework
3. django-cors-headers
4. djangorestframework-simplejwt
5. pillow
6. google-genai
7. python-dotenv

#### para rodar o  programa, siga as seguintes instruções:

1. Baixe o código fonte ou faça o pull 
2. inicialize um ambiente virtual de python, ative-o e baixe os pacotes:
    #### `pip install django djangorestframework django-cors-headers pillow python-dotenv`
    #### `pip install -q -U google-genai`
3. faça cd para o diretório do projeto (deve ver flashcards, software_educacional, db.sqlite3 e manage.py)
4. execute o seguinte comando: 
    #### `python manage.py runserver`
5. Faça as requisiçoes para o endereço "127.0.0.1:8000/"

obs: se visitar 127.0.0.1:8000/admin, e logar com nome: "guidjy" e senha: "craft22@" da pra ver todas as mudanças feitas no banco de dados com as requisições

## APIs

### Usuários

#### `GET /`
Retorna todos os usuários cadastrados.  
**Resposta:** JSON com lista de usuários.

#### `POST /registrar/`
Registra um novo usuário.  
**Campos:**
- `nome`: string (obrigatório)
- `senha`: string (obrigatório)
- `confirmacaoSenha`: string (obrigatório)
- `email`: string (opcional)
- `imagemDePerfil`: url (opcional)  
**Resposta:** Mensagem de sucesso ou erro.

#### `POST /api/token/`
Realiza login de um usuário.  
**Campos:**
- `nome`: string
- `senha`: string  
**Resposta:** Mensagem de sucesso ou erro.

#### `GET /logout/`
Realiza logout do usuário autenticado.  
**Resposta:** Mensagem de sucesso.

#### `POST /editar_usuario/`
Permite editar os dados do usuário atual
- `novoNome`: string
- `novaSenha`: string
- `novoEmail`: string
- `novaImagem`: url
- **Resposta:** Mensagem de sucesso e dados do usuário editado

#### `GET /perfil/`
Retorna dados sobre o usuário atual

---

### Decks

#### `POST /criar_deck/`
Cria um novo deck para o usuário autenticado.  
**Campos:**
- `nome`: string  
**Resposta:** JSON com o deck criado.

#### `PATCH /editar_deck/`
Edita o nome de um deck existente.  
**Campos:**
- `id`: int (ID do deck)
- `novoNome`: string  
**Resposta:** Mensagem de sucesso ou erro.

#### `DELETE /deletar_deck/<id>`
Deleta um deck pelo ID.  
**Resposta:** Mensagem de sucesso ou erro.

#### `GET /get_deck/<id>`
Retorna um deck e seus cards pelo ID.  
**Resposta:** JSON com o deck e seus cards.

#### `GET /decks_usuario/`
retorna todos os decks criados pelo usuário atual.
**Resoista:** JSON com o id, nome, numero de cards, ordem dos cards e criador

#### `GET /todos_decks/`
retorna todos os decks criados.
**Resoista:** JSON com o id, nome, numero de cards, ordem dos cards e criador

---

### Cards

#### `POST /criar_card/`
Cria um novo card em um deck.  
**Campos:**
- `frente`: string
- `tras`: string
- `imagem`: file (opcional)
- `deck`: string (nome do deck)
- `tag`: string (opcional)  
**Resposta:** Mensagem de sucesso e dados do card.

#### `PATCH /editar_card/`
Edita um card existente.  
**Campos:**
- `id`: int (ID do card)
- `novaFrente`: string (opcional)
- `novaTras`: string (opcional)
- `novaImagem`: file (opcional)
- `novaTag`: string (opcional)  
**Resposta:** Mensagem de sucesso e dados atualizados.

#### `DELETE /deletar_card/<id>`
Deleta um card pelo ID.  
**Resposta:** Mensagem de sucesso ou erro.

#### `GET /get_card/<id>`
Retorna um card pelo ID.  
**Resposta:** JSON com os dados do card.

---

### Estudo

#### `GET /comecar_estudo/<id>`
Retorna todos os cards do deck de "id"
**Resposta:** JSON com todos os dados do deck a ser estudado.

#### `PATCH /TERMINAR_ESTUDO`
Atualiza a ordem dos cards do deck após uma sessão de estudo
- `id`: int (id do deck sendo estudado)
- `novaOrdem`: int[] (lista com os ids dos cards)  

