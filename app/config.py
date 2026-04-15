"""
Configurações centralizadas da aplicação
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação via variáveis de ambiente"""
    
    # Banco de dados
    DATABASE_URL: str = "sqlite:///./gmuds.db"
    
    # GLPI
    GLPI_URL: str = ""
    GLPI_APP_TOKEN: str = ""
    GLPI_USER_TOKEN: str = ""
    
    # Aplicação
    APP_NAME: str = "GMUD - Gestão de Manutenção"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Servidor
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # Permite variáveis extras no .env
    )


@lru_cache()
def get_settings():
    """Retorna instância singleton das configurações"""
    return Settings()
