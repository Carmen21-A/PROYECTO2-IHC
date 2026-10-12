from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import usuarios, movimientos, categorias, limite

from sqlalchemy import text, inspect

try:
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    if "movimientos" in inspector.get_table_names():
        columnas = [c["name"] for c in inspector.get_columns("movimientos")]
        if "estado" not in columnas:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE movimientos ADD COLUMN estado VARCHAR(20) DEFAULT 'pendiente' NOT NULL;"))
                conn.commit()
                print("[OK] Columna 'estado' agregada a tabla movimientos exitosamente.")
    if "usuarios" in inspector.get_table_names():
        columnas = [c["name"] for c in inspector.get_columns("usuarios")]
        if "limite_mensual" not in columnas:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE usuarios ADD COLUMN limite_mensual NUMERIC(10, 2) DEFAULT NULL;"))
                conn.commit()
                print("[OK] Columna 'limite_mensual' agregada a tabla usuarios exitosamente.")
    # Sin categorías en la BD, los movimientos se guardarían sin categoría y no se podrían filtrar
    from sqlalchemy.orm import Session
    with Session(engine) as db:
        if db.query(models.Categoria).count() == 0:
            db.add_all([models.Categoria(nombre=n, tipo=t, icono=i) for n, t, i in models.CATEGORIAS_INICIALES])
            db.commit()
            print("[OK] Categorias iniciales cargadas.")
except Exception as e:
    print(f"Nota de conexion a la base de datos: {e}")

app = FastAPI(
    title="Presupuesto Estudiantil API",
    description="API Backend para control de presupuesto estudiantil (IHC - Proyecto 2)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(movimientos.router)
app.include_router(categorias.router)
app.include_router(limite.router)

@app.get("/")
def ruta_raiz():
    return {
        "aplicacion": "Presupuesto Estudiantil API",
        "estado": "En línea 🚀",
        "documentacion": "/docs",
        "tarea": "Manejo de acceso (Tarea 1 - IHC)"
    }
