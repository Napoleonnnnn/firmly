from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name:str = "Firmly API"
    version: str = "1.0.0"
    debug: bool = True
    gemini_api_key: str = ""
    
    class Config:
        env_file = ".env"
    
settings = Settings()