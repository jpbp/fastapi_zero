# Configuração CORS para FastAPI Zero

Para que o frontend React funcione corretamente com sua API FastAPI, você precisa configurar o CORS (Cross-Origin Resource Sharing).

## ⚠️ IMPORTANTE: Adicione CORS à sua API

Adicione as seguintes linhas ao seu arquivo `fastapi_zero/app.py`:

```python
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware  # ← ADICIONE ESTA LINHA

from fastapi_zero.routers import auth, users
from fastapi_zero.schemas import (
    Message,
)

app = FastAPI(title='Minha Api Bala!')

# ← ADICIONE ESTAS LINHAS PARA CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL do frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)

# ... resto do código permanece igual
```

## 🔧 Configuração Alternativa (Mais Permissiva para Desenvolvimento)

Se você quiser permitir qualquer origem durante o desenvolvimento:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🚀 Como Testar

1. **Inicie sua API FastAPI:**
   ```bash
   cd /caminho/para/seu/projeto
   poetry run task run
   # ou
   fastapi dev fastapi_zero/app.py
   ```

2. **Em outro terminal, inicie o frontend:**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Acesse:**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000

## 🐛 Solução de Problemas

### Erro: "Access to fetch at 'http://localhost:8000/...' from origin 'http://localhost:3000' has been blocked by CORS policy"

**Solução:** Certifique-se de que adicionou o middleware CORS conforme mostrado acima.

### Erro: "Network Error" ou "Connection refused"

**Possíveis causas:**
1. API não está rodando em http://localhost:8000
2. Firewall bloqueando a conexão
3. API rodando em porta diferente

**Solução:** 
1. Verifique se a API está rodando: `curl http://localhost:8000/`
2. Se a API estiver em outra porta, edite `frontend/src/services/api.js`

### Frontend não carrega

**Verificações:**
1. Node.js instalado (versão 16+)
2. Dependências instaladas: `npm install`
3. Porta 3000 disponível

## 📝 Notas Importantes

- **Produção:** Em produção, substitua `allow_origins=["*"]` pela URL real do seu frontend
- **Segurança:** Nunca use `allow_origins=["*"]` em produção com `allow_credentials=True`
- **HTTPS:** Em produção, use HTTPS tanto para frontend quanto backend