# FastAPI Zero - Guia Completo

Um projeto completo de API REST usando FastAPI, servindo como guia de referência para desenvolvimento de APIs modernas em Python.

## Índice

- [Visão Geral](#visão-geral)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Conceitos Fundamentais](#conceitos-fundamentais)
- [Endpoints da API](#endpoints-da-api)
- [Modelos e Schemas](#modelos-e-schemas)
- [Testes](#testes)
- [Comandos Úteis](#comandos-úteis)
- [Exemplos Práticos](#exemplos-práticos)

## Visão Geral

Este projeto demonstra uma API REST completa usando FastAPI com as seguintes funcionalidades:

- CRUD completo de usuários
- Validação de dados com Pydantic
- Modelos SQLAlchemy para ORM
- Testes automatizados com pytest
- Documentação automática (Swagger/OpenAPI)
- Respostas em JSON e HTML
- Tratamento de erros HTTP
- Configuração de desenvolvimento com Poetry

## Configuração do Ambiente

### Pré-requisitos

- Python 3.13+
- Poetry (gerenciador de dependências)

### Instalação

```bash
# 1. Instalar pipx (se não tiver)
pip install --user pipx

# 2. Instalar Poetry
pipx install poetry 
pipx inject poetry poetry-plugin-shell

# 3. Configurar Python 3.13
poetry python install 3.13

# 4. Criar projeto (se for novo)
poetry new --flat fastapi_zero

# 5. Configurar ambiente
poetry env use 3.13
poetry install

# 6. Instalar dependências principais
poetry add 'fastapi[standard]' sqlalchemy

# 7. Instalar dependências de desenvolvimento
poetry add --group dev pytest pytest-cov taskipy ruff

# 8. Ativar ambiente virtual
poetry shell
```

### Executar o Projeto

```bash
# Desenvolvimento
poetry run task run
# ou
fastapi dev fastapi_zero/app.py

# Testes
poetry run task test

# Linting e formatação
poetry run task lint
poetry run task format
```

## Estrutura do Projeto

```
fastapi_zero/
├── fastapi_zero/
│   ├── __init__.py
│   ├── app.py          # Aplicação principal FastAPI
│   ├── models.py       # Modelos SQLAlchemy (ORM)
│   └── schemas.py      # Schemas Pydantic (validação)
├── tests/
│   ├── __init__.py
│   ├── conftest.py     # Configurações de teste
│   ├── test_app.py     # Testes da aplicação
│   └── test_db.py      # Testes do banco de dados
├── pyproject.toml      # Configurações do projeto
├── poetry.lock         # Lock das dependências
└── README.md           # Este arquivo
```

## Conceitos Fundamentais

### 1. FastAPI Application

```python
from fastapi import FastAPI

app = FastAPI(title='Minha Api Bala!')
```

**Conceitos:**
- `FastAPI()`: Cria a instância principal da aplicação
- `title`: Define o título que aparece na documentação automática
- Gera automaticamente documentação OpenAPI/Swagger

### 2. Decoradores de Rota

```python
@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
@app.put('/users/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
@app.delete('/users/{user_id}/', status_code=HTTPStatus.OK, response_model=Message)
```

**Conceitos:**
- `@app.get/post/put/delete`: Define o método HTTP e rota
- `status_code`: Código de status HTTP de retorno
- `response_model`: Modelo Pydantic para validar resposta
- `{user_id}`: Parâmetro de path dinâmico

### 3. Códigos de Status HTTP

```python
from http import HTTPStatus

# Principais códigos usados:
HTTPStatus.OK           # 200 - Sucesso
HTTPStatus.CREATED      # 201 - Recurso criado
HTTPStatus.NOT_FOUND    # 404 - Não encontrado
HTTPStatus.UNPROCESSABLE_CONTENT  # 422 - Dados inválidos
```

### 4. Tratamento de Erros

```python
from fastapi import HTTPException

raise HTTPException(
    status_code=HTTPStatus.NOT_FOUND, 
    detail='User not found!'
)
```

## Endpoints da API

### 1. Endpoint Raiz (GET /)

```python
@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}
```

**Funcionalidade:** Endpoint básico de teste
**Retorna:** JSON com mensagem de boas-vindas
**Exemplo de resposta:**
```json
{
  "message": "Olá mundo!"
}
```

### 2. Endpoint HTML (GET /html/)

```python
@app.get('/html/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_root_html():
    return """
    <html>
        <head>
            <title> Nosso olá mundo! </title>
        </head>
        <body>
            <h1>Olá Mundo</h1>
        </body>
    </html>"""
```

**Conceitos:**
- `response_class=HTMLResponse`: Retorna HTML em vez de JSON
- Útil para páginas web simples ou documentação

### 3. Criar Usuário (POST /users/)

```python
@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id
```

**Conceitos:**
- `user: UserSchema`: Validação automática do corpo da requisição
- `**user.model_dump()`: Desempacota dados do Pydantic model
- `len(database) + 1`: Gera ID sequencial simples

**Exemplo de requisição:**
```json
{
  "username": "ana",
  "email": "ana@example.com",
  "password": "senha-da-ana"
}
```

**Exemplo de resposta:**
```json
{
  "username": "ana",
  "email": "ana@example.com",
  "id": 1
}
```

### 4. Listar Usuários (GET /users/)

```python
@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}
```

**Conceitos:**
- Retorna lista de todos os usuários
- `UserList`: Schema que encapsula lista de usuários

### 5. Buscar Usuário por ID (GET /users/{user_id}/)

```python
@app.get('/users/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user_for_id(user_id: int):
    for data in database:
        if data.id == user_id:
            return data
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
    )
```

**Conceitos:**
- `user_id: int`: Parâmetro de path com validação de tipo
- Busca linear no banco em memória
- `HTTPException`: Tratamento de erro quando usuário não existe

### 6. Atualizar Usuário (PUT /users/{user_id}/)

```python
@app.put('/users/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    
    for i in range(len(database)):
        if database[i].id == user_id:
            database[i] = user_with_id
            return user_with_id
    
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
    )
```

**Conceitos:**
- Combina parâmetro de path (`user_id`) com corpo da requisição (`user`)
- Substitui completamente o usuário existente
- Mantém o ID original

### 7. Deletar Usuário (DELETE /users/{user_id}/)

```python
@app.delete('/users/{user_id}/', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(user_id: int):
    for data in database:
        if data.id == user_id:
            database.remove(data)
            return {'message': 'User Deleted!'}
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
    )
```

## Modelos e Schemas

### Schemas Pydantic (schemas.py)

#### 1. Message Schema
```python
class Message(BaseModel):
    message: str
```
**Uso:** Respostas simples com mensagens

#### 2. UserSchema (Input)
```python
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
```
**Conceitos:**
- `EmailStr`: Validação automática de email
- Usado para entrada de dados (criação/atualização)

#### 3. UserPublic (Output)
```python
class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int
```
**Conceitos:**
- Exclui campos sensíveis (como password)
- Usado para retornar dados ao cliente

#### 4. UserList
```python
class UserList(BaseModel):
    users: list[UserPublic]
```
**Uso:** Encapsula lista de usuários

#### 5. UserDB (Internal)
```python
class UserDB(UserSchema):
    id: int
```
**Conceitos:**
- Herda de `UserSchema`
- Adiciona campo `id`
- Usado internamente no banco em memória

### Modelos SQLAlchemy (models.py)

```python
@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
```

**Conceitos:**
- `@table_registry.mapped_as_dataclass`: Cria dataclass automaticamente
- `Mapped[tipo]`: Type hints para SQLAlchemy 2.0+
- `init=False`: Campo não incluído no construtor
- `primary_key=True`: Chave primária
- `unique=True`: Restrição de unicidade
- `server_default=func.now()`: Valor padrão no banco

## Testes

### Configuração de Testes (conftest.py)

#### Fixture de Cliente
```python
@pytest.fixture
def client():
    return TestClient(app)
```
**Uso:** Cria cliente de teste para fazer requisições HTTP

#### Fixture de Sessão de Banco
```python
@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        echo=False
    )
    table_registry.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session
    
    table_registry.metadata.drop_all(engine)
    engine.dispose()  # Fecha todas as conexoes do pool
```
**Conceitos:**
- `sqlite:///:memory:`: Banco em memória para testes
- `connect_args={'check_same_thread': False}`: Permite uso em threads diferentes
- `echo=False`: Desabilita logs SQL nos testes
- `create_all/drop_all`: Cria/remove tabelas para cada teste
- `engine.dispose()`: **IMPORTANTE** - Fecha todas as conexões para evitar ResourceWarning

#### Mock de Tempo
```python
@contextmanager
def _mock_db_time(model, time=datetime(2025, 5, 20)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
    
    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)
```
**Uso:** Controla timestamps em testes para resultados determinísticos

### Padrão AAA nos Testes

```python
def test_root_deve_retornar_ola_mundo(client):
    """
    Arrange (Arranjo): Preparar dados/estado
    Act (Ação): Executar a operação
    Assert (Verificação): Validar resultado
    """
    # Act
    response = client.get('/')
    
    # Assert
    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK
```

### Exemplos de Testes

#### Teste de Endpoint Básico
```python
def test_read_root_html_retornar_ola_mundo_html(client):
    response = client.get('/html')
    
    assert response.status_code == HTTPStatus.OK
    assert response.headers['content-type'].startswith('text/html')
    assert '<h1>Olá Mundo</h1>' in response.text
```

#### Teste de CRUD Completo
```python
def test_created_user_return_201(client):
    response = client.post(
        '/users',
        json={
            'username': 'ana',
            'email': 'ana@example.com',
            'password': 'senha-da-ana',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'ana',
        'email': 'ana@example.com',
        'id': 1,
    }
```

#### Teste de Validação
```python
def test_created_user_fail_not_username(client):
    response = client.post(
        '/users', 
        json={'email': 'user@example.com', 'password': 'string'}
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
```

#### Teste de Banco de Dados (test_db.py)
```python
def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='test', email='test@test.com', password='secret'
        )
        session.add(new_user)
        session.commit()
        user = session.scalar(select(User).where(User.username == 'test'))
        assert asdict(user) == {
            'id': 1,
            'username': 'test',
            'email': 'test@test.com',
            'password': 'secret',
            'created_at': time,
        }
```

**Conceitos:**
- `session.add()`: Adiciona objeto à sessão
- `session.commit()`: Confirma transação no banco
- `session.scalar()`: Retorna um único resultado
- `select(User).where()`: Query SQLAlchemy 2.0 style
- `asdict()`: Converte dataclass para dicionário
- `mock_db_time`: Controla timestamp para teste determinístico

### Troubleshooting de Testes

#### ResourceWarning: unclosed database
Se você encontrar este warning ao executar testes:
```
ResourceWarning: unclosed database in <sqlite3.Connection object>
```

**Solução:** Certifique-se de que o fixture `session` inclui `engine.dispose()`:
```python
@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    # ... código do teste ...
    engine.dispose()  # Esta linha é essencial!
```

**Por que acontece:**
- SQLAlchemy mantém um pool de conexões
- Em testes, essas conexões podem não ser fechadas automaticamente
- `engine.dispose()` força o fechamento de todas as conexões

#### Executar testes com mais detalhes
```bash
# Executar com warnings visíveis
poetry run pytest tests/ -v --tb=short

# Executar teste específico
poetry run pytest tests/test_db.py::test_create_user -v

# Executar com cobertura
poetry run pytest tests/ --cov=fastapi_zero --cov-report=html
```

## Comandos Úteis

### Taskipy (pyproject.toml)

```toml
[tool.taskipy.tasks]
lint = 'ruff check .'                    # Verificar código
pre_format = 'ruff check --fix'          # Corrigir automaticamente
format = 'ruff format .'                 # Formatar código
run = 'fastapi dev fastapi_zero/app.py'  # Executar em desenvolvimento
pre_test = 'task lint'                   # Executar antes dos testes
test = 'pytest -s --cov=fastapi_zero -vv'  # Executar testes
post_test = 'coverage html'              # Gerar relatório de cobertura
```

### Comandos Poetry

```bash
# Gerenciamento de dependências
poetry add <pacote>              # Adicionar dependência
poetry add --group dev <pacote>  # Adicionar dependência de desenvolvimento
poetry remove <pacote>           # Remover dependência
poetry update                    # Atualizar dependências

# Ambiente virtual
poetry shell                     # Ativar ambiente virtual
poetry env info                  # Informações do ambiente
poetry env list                  # Listar ambientes

# Execução
poetry run <comando>             # Executar comando no ambiente virtual
poetry run task <task>           # Executar task do taskipy
```

## Exemplos Práticos

### 1. Testando a API com curl

```bash
# Listar usuários (vazio inicialmente)
curl -X GET "http://localhost:8000/users/"

# Criar usuário
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao",
    "email": "joao@example.com",
    "password": "senha123"
  }'

# Buscar usuário por ID
curl -X GET "http://localhost:8000/users/1"

# Atualizar usuário
curl -X PUT "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao_updated",
    "email": "joao_new@example.com",
    "password": "nova_senha"
  }'

# Deletar usuário
curl -X DELETE "http://localhost:8000/users/1"
```

### 2. Usando Python requests

```python
import requests

base_url = "http://localhost:8000"

# Criar usuário
user_data = {
    "username": "maria",
    "email": "maria@example.com",
    "password": "senha_maria"
}

response = requests.post(f"{base_url}/users/", json=user_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Listar usuários
response = requests.get(f"{base_url}/users/")
users = response.json()
print(f"Usuários: {users}")
```

### 3. Documentação Automática

Após executar a aplicação, acesse:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## Conceitos Importantes

### ORM (Object-Relational Mapping)
- **Definição:** Mapeamento de Objetos Relacionais
- **Função:** Converte dados entre sistemas incompatíveis (Python ↔ SQL)
- **Vantagem:** Trabalhar com objetos Python em vez de SQL puro

### Pydantic Models vs SQLAlchemy Models
- **Pydantic:** Validação de dados, serialização/deserialização
- **SQLAlchemy:** Mapeamento para banco de dados, relacionamentos
- **Separação:** Permite diferentes representações para API e banco

### Dependency Injection (Futuro)
```python
# Exemplo para próximos projetos
from fastapi import Depends

def get_db():
    # Retorna sessão do banco
    pass

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    # Usa sessão injetada
    pass
```

### Middleware (Futuro)
```python
# Exemplo para próximos projetos
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Migrations com Alembic

### Configuração do Alembic

O projeto usa Alembic para gerenciar migrations do banco de dados:

```bash
# Inicializar Alembic (já feito)
poetry run alembic init migrations

# Gerar nova migration
poetry run alembic revision --autogenerate -m "descrição da mudança"

# Aplicar migrations
poetry run alembic upgrade head

# Verificar status
poetry run alembic check

# Ver histórico
poetry run alembic history

# Reverter migration
poetry run alembic downgrade -1
```

### Configuração de Settings

```python
# fastapi_zero/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    
    DATABASE_URL: str = 'sqlite:///./database.db'
```

**Conceitos importantes:**
- `DATABASE_URL: str`: Anotação de tipo obrigatória no Pydantic v2
- `model_config`: Configuração do modelo Pydantic
- `.env`: Arquivo para variáveis de ambiente

### Troubleshooting Alembic

#### Erro: "A non-annotated attribute was detected"
```
pydantic.errors.PydanticUserError: A non-annotated attribute was detected: `DATABASE_URL = <class 'str'>`
```

**Problema:** Pydantic v2 requer anotações de tipo adequadas.

**Solução:**
```python
# ❌ Incorreto
DATABASE_URL = str

# ✅ Correto  
DATABASE_URL: str = 'sqlite:///./database.db'
```

#### Arquivo .env
```bash
# .env
DATABASE_URL="sqlite:///database.db"
```

## Próximos Passos

Para expandir este projeto, considere:

1. **Banco de Dados Real:** Substituir lista em memória por PostgreSQL/MySQL
2. **Autenticação:** JWT tokens, OAuth2
3. **Relacionamentos:** Modelos relacionados (User → Posts → Comments)
4. **Paginação:** Limitar resultados de listagem
5. **Filtros:** Busca por campos específicos
6. **Validações Avançadas:** Regras de negócio customizadas
7. **Background Tasks:** Processamento assíncrono
8. **Cache:** Redis para performance
9. **Deploy:** Docker, Kubernetes, cloud providers
10. **Monitoramento:** Logs, métricas, health checks

---

**Autor:** jpbp  
**Email:** jppenna04@gmail.com  
**Versão:** 0.1.0