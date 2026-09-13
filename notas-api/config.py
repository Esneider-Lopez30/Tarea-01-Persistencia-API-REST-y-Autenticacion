import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "cambia-esta-clave")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "cambia-esta-clave-jwt")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///notas.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False