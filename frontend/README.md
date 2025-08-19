# Frontend FastAPI Zero

Este é o frontend em React para a API FastAPI Zero. Ele fornece uma interface web completa para interagir com todos os endpoints da API.

## 🚀 Funcionalidades

### 🔐 Autenticação
- **Login**: Interface para fazer login com email e senha
- **Registro**: Formulário para criar novos usuários
- **Logout**: Botão para sair da aplicação
- **Refresh Token**: Renovação automática do token de acesso

### 👥 Gerenciamento de Usuários
- **Listar Usuários**: Visualizar todos os usuários com paginação
- **Criar Usuário**: Formulário para criar novos usuários
- **Buscar por ID**: Encontrar usuário específico pelo ID
- **Atualizar Usuário**: Editar informações de usuários existentes
- **Deletar Usuário**: Remover usuários do sistema

### 📋 Interface Interativa
- **Resposta da API**: Visualização em tempo real das respostas JSON
- **Tratamento de Erros**: Mensagens de erro e sucesso claras
- **Loading States**: Indicadores de carregamento durante requisições

## 🛠️ Tecnologias Utilizadas

- **React 18**: Framework principal
- **React Router DOM**: Roteamento
- **Axios**: Cliente HTTP para requisições
- **Context API**: Gerenciamento de estado de autenticação
- **CSS Vanilla**: Estilização responsiva

## 📦 Instalação e Execução

### Pré-requisitos
- Node.js (versão 16 ou superior)
- npm ou yarn
- API FastAPI Zero rodando em `http://localhost:8000`

### Passos para executar:

1. **Navegue até a pasta do frontend:**
   ```bash
   cd frontend
   ```

2. **Instale as dependências:**
   ```bash
   npm install
   ```

3. **Inicie o servidor de desenvolvimento:**
   ```bash
   npm start
   ```

4. **Acesse a aplicação:**
   - Abra seu navegador em `http://localhost:3000`

## 🔧 Configuração

### Configuração da API
O frontend está configurado para se conectar com a API em `http://localhost:8000`. Se sua API estiver rodando em outro endereço, edite o arquivo `src/services/api.js`:

```javascript
this.api = axios.create({
  baseURL: 'http://localhost:8000', // Altere aqui
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### Proxy (Desenvolvimento)
O `package.json` inclui uma configuração de proxy para desenvolvimento:
```json
"proxy": "http://localhost:8000"
```

## 📱 Como Usar

### 1. Primeiro Acesso
1. Acesse `http://localhost:3000`
2. Clique em "Registrar" para criar uma conta
3. Preencha o formulário com seus dados
4. Após o registro, faça login com suas credenciais

### 2. Dashboard
Após o login, você terá acesso ao dashboard com todas as funcionalidades:

#### 🔐 Seção de Autenticação
- **Renovar Token**: Atualiza seu token de acesso
- **Testar Endpoint Root**: Testa a conectividade com a API

#### 👥 Seção de Usuários
- **Listar Usuários**: Use os controles de paginação (offset/limit)
- **Criar Usuário**: Preencha o formulário para adicionar novos usuários
- **Buscar por ID**: Digite um ID para encontrar um usuário específico
- **Atualizar**: Modifique dados de usuários existentes
- **Deletar**: Remove usuários (com confirmação)

#### 📋 Resposta da API
- Todas as respostas da API são exibidas em formato JSON
- Mensagens de sucesso e erro são mostradas no topo da página

## 🔒 Segurança

- **JWT Token**: Armazenado no localStorage
- **Interceptors**: Adiciona automaticamente o token nas requisições
- **Redirecionamento**: Logout automático em caso de token expirado
- **Rotas Protegidas**: Acesso restrito baseado na autenticação

## 📁 Estrutura do Projeto

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   └── Navbar.js
│   ├── contexts/
│   │   └── AuthContext.js
│   ├── pages/
│   │   ├── Dashboard.js
│   │   ├── Login.js
│   │   └── Register.js
│   ├── services/
│   │   └── api.js
│   ├── App.js
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## 🚀 Scripts Disponíveis

- `npm start`: Inicia o servidor de desenvolvimento
- `npm build`: Cria build de produção
- `npm test`: Executa os testes
- `npm eject`: Ejeta a configuração do Create React App

## 🤝 Integração com a API

O frontend está totalmente integrado com os seguintes endpoints da API FastAPI Zero:

### Autenticação
- `POST /auth/token` - Login
- `POST /auth/refresh_token` - Refresh token

### Usuários
- `POST /users/` - Criar usuário
- `GET /users/` - Listar usuários
- `GET /users/{user_id}/` - Buscar usuário por ID
- `PUT /users/{user_id}/` - Atualizar usuário
- `DELETE /users/{user_id}/` - Deletar usuário

### Outros
- `GET /` - Endpoint root

## 🎨 Personalização

O arquivo `src/index.css` contém todos os estilos da aplicação. Você pode personalizar:
- Cores do tema
- Layout dos componentes
- Responsividade
- Animações

## 🐛 Solução de Problemas

### Erro de CORS
Se encontrar erros de CORS, certifique-se de que sua API FastAPI tenha o middleware CORS configurado:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API não encontrada
Verifique se:
1. A API FastAPI está rodando em `http://localhost:8000`
2. Todos os endpoints estão funcionando corretamente
3. A configuração de baseURL no `api.js` está correta

## 📄 Licença

Este projeto faz parte do FastAPI Zero e segue a mesma licença do projeto principal.