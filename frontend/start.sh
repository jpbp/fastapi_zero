#!/bin/bash

echo "🚀 Iniciando Frontend FastAPI Zero..."
echo ""

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale o Node.js primeiro."
    echo "   Visite: https://nodejs.org/"
    exit 1
fi

# Verificar se npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ npm não encontrado. Por favor, instale o npm primeiro."
    exit 1
fi

echo "✅ Node.js $(node --version) encontrado"
echo "✅ npm $(npm --version) encontrado"
echo ""

# Verificar se as dependências estão instaladas
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências..."
    npm install
    echo ""
fi

echo "🌐 Iniciando servidor de desenvolvimento..."
echo "   Frontend: http://localhost:3000"
echo "   API Backend: http://localhost:8000 (certifique-se de que está rodando)"
echo ""
echo "💡 Dica: Para parar o servidor, pressione Ctrl+C"
echo ""

# Iniciar o servidor
npm start