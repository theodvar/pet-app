import os

class Config:
    DEBUG = os.getenv("DEBUG", True)
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_NAME = os.getenv("DB_NAME", "pets_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
