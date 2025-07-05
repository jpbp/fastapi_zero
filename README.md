# FastAPI Zero - API REST Completa

Uma API REST robusta e moderna desenvolvida com FastAPI, demonstrando as melhores práticas para desenvolvimento de APIs em Python.

## 🚀 Funcionalidades

- ✅ **CRUD completo de usuários** com validações de integridade
- ✅ **Validação de dados** com Pydantic e EmailStr
- ✅ **ORM SQLAlchemy** com modelos dataclass
- ✅ **Migrações de banco** com Alembic
- ✅ **Testes automatizados** com 100% de cobertura
- ✅ **Documentação automática** (Swagger/OpenAPI)
- ✅ **Configuração flexível** com Pydantic Settings
- ✅ **Linting e formatação** com Ruff
- ✅ **Gerenciamento de dependências** com Poetry
- ✅ **Timestamps automáticos** (created_at, updated_at)

## 📊 Status do Projeto

- **Versão:** 0.1.0
- **Cobertura de Testes:** 100%
- **Testes:** 19 testes passando
- **Python:** 3.13+

## 🛠️ Configuração do Ambiente

### Pré-requisitos

- Python 3.13+
- Poetry (gerenciador de dependências)

### Instalação Rápida

```bash
# 1. Clonar o repositório
git clone <seu-repositorio>
cd fastapi_zero

# 2. Instalar dependências
poetry install

# 3. Ativar ambiente virtual
poetry shell

# 4. Configurar variáveis de ambiente
echo "DATABASE_URL=sqlite:///./database.db" > .env

# 5. Executar migrações (se necessário)
poetry run alembic upgrade head
```

### Comandos Disponíveis

```bash
# Desenvolvimento (com hot reload)
poetry run task run

# Testes com cobertura
poetry run task test

# Linting e formatação
poetry run task lint
poetry run task format

# Executar diretamente
poetry run fastapi dev fastapi_zero/app.py
```

## 📁 Estrutura do Projeto

```
fastapi_zero/
├── fastapi_zero/
│   ├── __init__.py
│   ├── app.py          # Aplicação FastAPI com endpoints
│   ├── database.py     # Configuração SQLAlchemy e sessões
│   ├── models.py       # Modelos de dados (User com timestamps)
│   ├── schemas.py      # Schemas Pydantic para validação
│   └── settings.py     # Configurações com Pydantic Settings
├── migrations/         # Migrações Alembic
│   ├── versions/       # 6 arquivos de migração
│   ├── env.py         # Configuração do Alembic
│   └── script.py.mako # Template para migrações
├── tests/
│   ├── __init__.py
│   ├── conftest.py     # Fixtures e configurações de teste
│   ├── test_app.py     # 17 testes dos endpoints
│   └── test_db.py      # 2 testes do banco de dados
├── pyproject.toml      # Dependências e configurações
├── alembic.ini        # Configuração do Alembic
├── poetry.lock        # Lock das dependências
├── .gitignore         # Arquivos ignorados pelo Git
└── .env               # Variáveis de ambiente (criar)
```

## 🔗 Endpoints da API

### Endpoints Básicos
- **GET /** - Health check: `{"message": "Olá mundo!"}`
- **GET /html/** - Página HTML simples

### CRUD de Usuários

| Método | Endpoint | Descrição | Body |
|--------|----------|-----------|------|
| POST | `/users/` | Criar usuário | `{"username": "string", "email": "user@example.com", "password": "string"}` |
| GET | `/users/` | Listar usuários | Query: `limit=10`, `offset=0` |
| GET | `/users/{user_id}/` | Buscar usuário por ID | - |
| PUT | `/users/{user_id}/` | Atualizar usuário | `{"username": "string", "email": "user@example.com", "password": "string"}` |
| DELETE | `/users/{user_id}/` | Deletar usuário | - |

### Validações Implementadas
- ✅ Username único
- ✅ Email único e válido
- ✅ Verificação de existência do usuário
- ✅ Tratamento de conflitos (409)
- ✅ Tratamento de não encontrado (404)

## 📊 Modelos e Schemas

### Modelo User (models.py)

```python
@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, default=func.now(), onupdate=func.now())
```

### Schemas Pydantic (schemas.py)

```python
# Input - Criação/Atualização
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

# Output - Resposta (sem senha)
class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int
    model_config = ConfigDict(from_attributes=True)

# Lista de usuários
class UserList(BaseModel):
    users: list[UserPublic]

# Mensagens simples
class Message(BaseModel):
    message: str
```

## 🧪 Testes

O projeto possui **100% de cobertura** com 19 testes:

### Testes dos Endpoints (test_app.py)
- ✅ Endpoint raiz (JSON e HTML)
- ✅ Criação de usuários (sucesso e falhas)
- ✅ Listagem de usuários (com e sem dados)
- ✅ Busca por ID (válido e inválido)
- ✅ Atualização de usuários (sucesso e conflitos)
- ✅ Deleção de usuários

### Testes do Banco (test_db.py)
- ✅ Criação de usuário no banco
- ✅ Funcionamento das sessões

```bash
# Executar testes
poetry run task test

# Ver relatório de cobertura
open htmlcov/index.html
```

## 🔧 Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **FastAPI** | 0.115+ | Framework web principal |
| **SQLAlchemy** | 2.0+ | ORM para banco de dados |
| **Alembic** | 1.16+ | Migrações de banco |
| **Pydantic** | 2.0+ | Validação de dados |
| **Pytest** | 8.4+ | Framework de testes |
| **Ruff** | 0.12+ | Linting e formatação |
| **Poetry** | - | Gerenciamento de dependências |

## 📚 Conceitos Demonstrados

- **Dependency Injection** com `Depends()`
- **Validação automática** com Pydantic
- **ORM moderno** com SQLAlchemy 2.0
- **Testes com fixtures** e mocks
- **Migrações de banco** com Alembic
- **Configuração por ambiente** com Settings
- **Documentação automática** OpenAPI/Swagger
- **Type hints** em todo o código
- **Tratamento de erros** HTTP

## 🚀 Próximos Passos

- [ ] Autenticação JWT
- [ ] Paginação avançada
- [ ] Filtros de busca
- [ ] Rate limiting
- [ ] Logs estruturados
- [ ] Docker containerization
- [ ] CI/CD pipeline

## 📖 Documentação da API

Após executar o servidor, acesse:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

**Desenvolvido com ❤️ usando FastAPI**