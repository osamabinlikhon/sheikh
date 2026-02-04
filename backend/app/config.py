from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Environment
    debug: bool = Field(default=False, env="PYTHON_ENV")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        env="CORS_ORIGINS"
    )
    
    # LLM Configuration
    api_key: str = Field(default="u2nkaN5BxVlI0ZfxP1ELKTKZ8Oz9eomf", env="API_KEY")
    api_base: str = Field(default="https://codestral.mistral.ai/v1", env="API_BASE")
    model_name: str = Field(default="codestral-latest", env="MODEL_NAME")
    temperature: float = Field(default=0.7, env="TEMPERATURE")
    max_tokens: int = Field(default=2000, env="MAX_TOKENS")
    
    # Database Configuration
    mongodb_uri: str = Field(..., env="MONGODB_URI")
    mongodb_database: str = Field(default="agent_sheikh", env="MONGODB_DATABASE")
    mongodb_username: str = Field(default=None, env="MONGODB_USERNAME")
    mongodb_password: str = Field(default=None, env="MONGODB_PASSWORD")
    
    # Cache Configuration
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    redis_password: str = Field(default=None, env="REDIS_PASSWORD")
    
    # Sandbox Configuration
    sandbox_image: str = Field(
        default="agent-sheikh-sandbox:latest", 
        env="SANDBOX_IMAGE"
    )
    sandbox_name_prefix: str = Field(
        default="sheikh-sandbox", 
        env="SANDBOX_NAME_PREFIX"
    )
    sandbox_ttl_minutes: int = Field(default=30, env="SANDBOX_TTL_MINUTES")
    sandbox_network: str = Field(
        default="agent-sheikh-network", 
        env="SANDBOX_NETWORK"
    )
    sandbox_https_proxy: str = Field(default=None, env="SANDBOX_HTTPS_PROXY")
    sandbox_http_proxy: str = Field(default=None, env="SANDBOX_HTTP_PROXY")
    sandbox_no_proxy: str = Field(default=None, env="SANDBOX_NO_PROXY")
    
    # Search Configuration
    search_provider: str = Field(default="bing", env="SEARCH_PROVIDER")
    google_search_api_key: str = Field(default=None, env="GOOGLE_SEARCH_API_KEY")
    google_search_engine_id: str = Field(default=None, env="GOOGLE_SEARCH_ENGINE_ID")
    
    # Authentication Configuration
    auth_provider: str = Field(default="password", env="AUTH_PROVIDER")
    password_salt: str = Field(default="agent-sheikh-salt", env="PASSWORD_SALT")
    password_hash_rounds: int = Field(default=10, env="PASSWORD_HASH_ROUNDS")
    local_auth_email: str = Field(default="admin@example.com", env="LOCAL_AUTH_EMAIL")
    local_auth_password: str = Field(default="admin", env="LOCAL_AUTH_PASSWORD")
    
    # JWT Configuration
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expire_days: int = Field(default=7, env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    
    # Email Configuration
    email_host: str = Field(default="smtp.gmail.com", env="EMAIL_HOST")
    email_port: int = Field(default=587, env="EMAIL_PORT")
    email_username: str = Field(default=None, env="EMAIL_USERNAME")
    email_password: str = Field(default=None, env="EMAIL_PASSWORD")
    email_from: str = Field(default=None, env="EMAIL_FROM")
    
    # MCP Configuration
    mcp_config_path: str = Field(default="/etc/mcp.json", env="MCP_CONFIG_PATH")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Agent Configuration
    max_agent_iterations: int = Field(default=10, env="MAX_AGENT_ITERATIONS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()