import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

function Dashboard() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [apiResponse, setApiResponse] = useState('');

  // Estados para formulários
  const [newUser, setNewUser] = useState({ username: '', email: '', password: '' });
  const [updateUser, setUpdateUser] = useState({ id: '', username: '', email: '', password: '' });
  const [searchUserId, setSearchUserId] = useState('');
  const [deleteUserId, setDeleteUserId] = useState('');
  const [pagination, setPagination] = useState({ offset: 0, limit: 10 });

  const showMessage = (message, type = 'success') => {
    if (type === 'success') {
      setSuccess(message);
      setError('');
    } else {
      setError(message);
      setSuccess('');
    }
    setTimeout(() => {
      setSuccess('');
      setError('');
    }, 5000);
  };

  const formatResponse = (data) => {
    return JSON.stringify(data, null, 2);
  };

  // Buscar todos os usuários
  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await apiService.getUsers(pagination.offset, pagination.limit);
      setUsers(response.data.users);
      setApiResponse(formatResponse(response.data));
      showMessage('Usuários carregados com sucesso!');
    } catch (error) {
      showMessage(error.response?.data?.detail || 'Erro ao carregar usuários', 'error');
      setApiResponse(formatResponse(error.response?.data || { error: 'Erro desconhecido' }));
    } finally {
      setLoading(false);
    }
  };

  // Criar novo usuário
  const handleCreateUser = async (e) => {
    e.preventDefault();
    if (!newUser.username || !newUser.email || !newUser.password) {
      showMessage('Preencha todos os campos', 'error');
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.createUser(newUser.username, newUser.email, newUser.password);
      setApiResponse(formatResponse(response.data));
      showMessage('Usuário criado com sucesso!');
      setNewUser({ username: '', email: '', password: '' });
      fetchUsers(); // Recarregar lista
    } catch (error) {
      showMessage(error.response?.data?.detail || 'Erro ao criar usuário', 'error');
      setApiResponse(formatResponse(error.response?.data || { error: 'Erro desconhecido' }));
    } finally {
      setLoading(false);
    }
  };

  // Buscar usuário por ID
  const handleSearchUser = async (e) => {
    e.preventDefault();
    if (!searchUserId) {
      showMessage('Digite um ID de usuário', 'error');
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.getUserById(searchUserId);
      setApiResponse(formatResponse(response.data));
      showMessage('Usuário encontrado!');
    } catch (error) {
      showMessage(error.response?.data?.detail || 'Erro ao buscar usuário', 'error');
      setApiResponse(formatResponse(error.response?.data || { error: 'Erro desconhecido' }));
    } finally {
      setLoading(false);
    }
  };

  // Atualizar usuário
  const handleUpdateUser = async (e) => {
    e.preventDefault();
    if (!updateUser.id || !updateUser.username || !updateUser.email || !updateUser.password) {
      showMessage('Preencha todos os campos', 'error');
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.updateUser(
        updateUser.id, 
        updateUser.username, 
        updateUser.email, 
        updateUser.password
      );
      setApiResponse(formatResponse(response.data));
      showMessage('Usuário atualizado com sucesso!');
      setUpdateUser({ id: '', username: '', email: '', password: '' });
      fetchUsers(); // Recarregar lista
    } catch (error) {
      showMessage(error.response?.data?.detail || 'Erro ao atualizar usuário', 'error');
      setApiResponse(formatResponse(error.response?.data || { error: 'Erro desconhecido' }));
    } finally {
      setLoading(false);
    }
  };

  // Deletar usuário
  const handleDeleteUser = async (e) => {
    e.preventDefault();
    if (!deleteUserId) {
      showMessage('Digite um ID de usuário', 'error');
      return;
    }

    if (!window.confirm('Tem certeza que deseja deletar este usuário?')) {
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.deleteUser(deleteUserId);
      setApiResponse(formatResponse(response.data));
      showMessage('Usuário deletado com sucesso!');
      setDeleteUserId('');
      fetchUsers(); // Recarregar lista
    } catch (error) {
      showMessage(error.response?.data?.detail || 'Erro ao deletar usuário', 'error');
      setApiResponse(formatResponse(error.response?.data || { error: 'Erro desconhecido' }));
    } finally {
      setLoading(false);
    }
  };

  // Refresh token
  const handleRefreshToken = async () => {
    setLoading(true);
    try {
      const response = await apiService.refreshToken();
      setApiResponse(formatResponse(response.data));
      showMessage('Token renovado com sucesso!');
      localStorage.setItem('token', response.data.access_token);
    } catch (error) {
      showMessage(error.response?.data?.detail || 'Erro ao renovar token', 'error');
      setApiResponse(formatResponse(error.response?.data || { error: 'Erro desconhecido' }));
    } finally {
      setLoading(false);
    }
  };

  // Testar endpoint root
  const handleTestRoot = async () => {
    setLoading(true);
    try {
      const response = await apiService.getRoot();
      setApiResponse(formatResponse(response.data));
      showMessage('Endpoint root testado com sucesso!');
    } catch (error) {
      showMessage(error.response?.data?.detail || 'Erro ao testar endpoint root', 'error');
      setApiResponse(formatResponse(error.response?.data || { error: 'Erro desconhecido' }));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [pagination.offset, pagination.limit]);

  return (
    <div className="container">
      <h1>Dashboard - API FastAPI Zero</h1>
      
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      {/* Seção de Autenticação */}
      <div className="endpoint-section">
        <h2 className="endpoint-title">🔐 Autenticação</h2>
        <div className="card">
          <button onClick={handleRefreshToken} className="btn" disabled={loading}>
            Renovar Token
          </button>
          <button onClick={handleTestRoot} className="btn" disabled={loading}>
            Testar Endpoint Root (/)
          </button>
        </div>
      </div>

      {/* Seção de Usuários */}
      <div className="endpoint-section">
        <h2 className="endpoint-title">👥 Gerenciamento de Usuários</h2>
        
        {/* Listar Usuários */}
        <div className="card">
          <h3>Listar Usuários (GET /users/)</h3>
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginBottom: '15px' }}>
            <label>Offset:</label>
            <input
              type="number"
              value={pagination.offset}
              onChange={(e) => setPagination({...pagination, offset: parseInt(e.target.value) || 0})}
              style={{ width: '80px' }}
              min="0"
            />
            <label>Limit:</label>
            <input
              type="number"
              value={pagination.limit}
              onChange={(e) => setPagination({...pagination, limit: parseInt(e.target.value) || 10})}
              style={{ width: '80px' }}
              min="1"
              max="10"
            />
            <button onClick={fetchUsers} className="btn" disabled={loading}>
              Carregar Usuários
            </button>
          </div>
          
          {users.length > 0 && (
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Username</th>
                  <th>Email</th>
                </tr>
              </thead>
              <tbody>
                {users.map(user => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.username}</td>
                    <td>{user.email}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Criar Usuário */}
        <div className="card">
          <h3>Criar Usuário (POST /users/)</h3>
          <form onSubmit={handleCreateUser}>
            <div className="form-group">
              <label>Username:</label>
              <input
                type="text"
                value={newUser.username}
                onChange={(e) => setNewUser({...newUser, username: e.target.value})}
                placeholder="Digite o username"
              />
            </div>
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                value={newUser.email}
                onChange={(e) => setNewUser({...newUser, email: e.target.value})}
                placeholder="Digite o email"
              />
            </div>
            <div className="form-group">
              <label>Password:</label>
              <input
                type="password"
                value={newUser.password}
                onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                placeholder="Digite a senha"
              />
            </div>
            <button type="submit" className="btn btn-success" disabled={loading}>
              Criar Usuário
            </button>
          </form>
        </div>

        {/* Buscar Usuário por ID */}
        <div className="card">
          <h3>Buscar Usuário por ID (GET /users/{`{user_id}`}/)</h3>
          <form onSubmit={handleSearchUser}>
            <div className="form-group">
              <label>ID do Usuário:</label>
              <input
                type="number"
                value={searchUserId}
                onChange={(e) => setSearchUserId(e.target.value)}
                placeholder="Digite o ID do usuário"
              />
            </div>
            <button type="submit" className="btn" disabled={loading}>
              Buscar Usuário
            </button>
          </form>
        </div>

        {/* Atualizar Usuário */}
        <div className="card">
          <h3>Atualizar Usuário (PUT /users/{`{user_id}`}/)</h3>
          <form onSubmit={handleUpdateUser}>
            <div className="form-group">
              <label>ID do Usuário:</label>
              <input
                type="number"
                value={updateUser.id}
                onChange={(e) => setUpdateUser({...updateUser, id: e.target.value})}
                placeholder="Digite o ID do usuário"
              />
            </div>
            <div className="form-group">
              <label>Novo Username:</label>
              <input
                type="text"
                value={updateUser.username}
                onChange={(e) => setUpdateUser({...updateUser, username: e.target.value})}
                placeholder="Digite o novo username"
              />
            </div>
            <div className="form-group">
              <label>Novo Email:</label>
              <input
                type="email"
                value={updateUser.email}
                onChange={(e) => setUpdateUser({...updateUser, email: e.target.value})}
                placeholder="Digite o novo email"
              />
            </div>
            <div className="form-group">
              <label>Nova Password:</label>
              <input
                type="password"
                value={updateUser.password}
                onChange={(e) => setUpdateUser({...updateUser, password: e.target.value})}
                placeholder="Digite a nova senha"
              />
            </div>
            <button type="submit" className="btn" disabled={loading}>
              Atualizar Usuário
            </button>
          </form>
        </div>

        {/* Deletar Usuário */}
        <div className="card">
          <h3>Deletar Usuário (DELETE /users/{`{user_id}`}/)</h3>
          <form onSubmit={handleDeleteUser}>
            <div className="form-group">
              <label>ID do Usuário:</label>
              <input
                type="number"
                value={deleteUserId}
                onChange={(e) => setDeleteUserId(e.target.value)}
                placeholder="Digite o ID do usuário"
              />
            </div>
            <button type="submit" className="btn btn-danger" disabled={loading}>
              Deletar Usuário
            </button>
          </form>
        </div>
      </div>

      {/* Resposta da API */}
      <div className="endpoint-section">
        <h2 className="endpoint-title">📋 Resposta da API</h2>
        <div className="card">
          {loading && <div className="loading">Carregando...</div>}
          {apiResponse && (
            <div className="json-display">
              {apiResponse}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;