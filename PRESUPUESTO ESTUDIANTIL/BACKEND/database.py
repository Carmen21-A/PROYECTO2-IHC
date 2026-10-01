import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/presupuesto_estudiantil"
)

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql+psycopg2://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+psycopg://", 1)

engine = None
try:
    test_engine = create_engine(DATABASE_URL, echo=False)
    with test_engine.connect() as conn:
        print("✓ Conexión exitosa a PostgreSQL")
    engine = test_engine
except Exception as err:
    print(f"⚠️ Nota de PostgreSQL: {err}")
    print("ℹ️ Usando almacenamiento local seguro (SQLite) mientras configuras tus credenciales de PostgreSQL en .env")
    engine = create_engine("sqlite:///./presupuesto.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
