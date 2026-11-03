from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DEEPSEEK_KEY: str

    REDIS_URL: str
    CACHE_SEARCH_TTL: int = 900
    CACHE_PRODUCT_TTL: int = 3600

    class Config:
        env_file = ".env"
        case_sensitive = True

    def check_settings(self):
        if self.CACHE_SEARCH_TTL <= 0 or self.CACHE_PRODUCT_TTL <= 0:
            raise ValueError("Cache TTL values must be positive integers")

settings = Settings()
settings.check_settings()