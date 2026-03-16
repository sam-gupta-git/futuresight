from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/trading"
    redis_url: str = "redis://localhost:6379/0"
    supabase_url: str = ""
    supabase_anon_key: str = ""
    polygon_api_key: str = ""
    ibkr_api_key: str = ""
    ibkr_base_url: str = "http://localhost:5000/v1/api"
    slack_webhook: str = ""
    smtp_host: str = ""
    smtp_user: str = ""
    smtp_pass: str = ""
    smtp_port: int = 587
    alert_email_to: str = ""
    api_base_url: str = "http://localhost:8000"
    scanner_equity_symbols: str = "AAPL,MSFT,NVDA"
    scanner_options_symbols: str = "SPY,QQQ"
    scanner_futures_contracts: str = "ESM6,NQM6"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
