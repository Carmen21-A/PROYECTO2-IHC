import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()                                                      #Carga las variables de entorno desde un archivo .env en la raíz del proyecto

DATABASE_URL = os.getenv(                                         #Busca la variable de entorno
    "DATABASE_URL",                                                #Si existe en el .env se usa
    "postgresql+psycopg://postgres:postgres@localhost:5432/presupuesto_estudiantil"  #Si no existe en el .env se usa esta direccion
)

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)  #Si la direccion empieza con postgresql:// lo reemplaza con postgresql+psycopg://
elif DATABASE_URL.startswith("postgresql+psycopg2://"):                              #Si la direccion empieza con postgresql+psycopg2:
    DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+psycopg://", 1) #lo reemplaza con postgresql+psycopg://

engine = None   
try:
    test_engine = create_engine(DATABASE_URL, echo=False)        #Crea un motor de SQLAlchemy que gestiona la conexión a PostgreSQL. echo=False desactiva el log de todas las consultas SQL en la consola
    with test_engine.connect() as conn:                          #Establece una conexión con la base de datos y la cierra automáticamente cuando sale del bloque
        print("[OK] Conexion exitosa a PostgreSQL")
    engine = test_engine                                        #Asigna el motor de prueba a la variable engine
except Exception as err:
    print(f"[Nota] PostgreSQL: {err}")
    print("[Info] Usando almacenamiento local seguro (SQLite) mientras configuras tus credenciales de PostgreSQL en .env")
    engine = create_engine("sqlite:///./presupuesto.db", connect_args={"check_same_thread": False})      #crea un motor con SQLite como respaldo local. check_same_thread: False permite que SQLite sea usado desde múltiples hilos

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)     #Crea una fábrica de sesiones que no guarda automáticamente, no envía datos automáticamente, y está conectada al motor de base de datos
Base = declarative_base()                                    #Crea una clase base a la que se conectarán tus modelos de base de datos

def get_db():
    db = SessionLocal()                                  #abre una sesión nueva
    try:
        yield db                                         #Entrega la sesión db
    finally:
        db.close()                                       #Cierra la sesión
    
