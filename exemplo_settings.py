"""
Exemplo de como usar as configurações do projeto
"""

from fastapi_zero.settings import Settings

def demonstrar_settings():
    print("=== DEMONSTRAÇÃO DAS CONFIGURAÇÕES ===")
    
    # Criar instância das configurações
    settings = Settings()
    
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    print(f"Tipo: {type(settings.DATABASE_URL)}")
    
    # Mostrar como o Pydantic valida automaticamente
    print(f"\nConfigurações carregadas:")
    print(f"- Arquivo .env: {settings.model_config.get('env_file')}")
    print(f"- Encoding: {settings.model_config.get('env_file_encoding')}")
    
    # Demonstrar que funciona com variáveis de ambiente
    import os
    print(f"\nVariável de ambiente DATABASE_URL: {os.getenv('DATABASE_URL', 'Não definida')}")

if __name__ == "__main__":
    demonstrar_settings()