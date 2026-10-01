from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import usuarios, movimientos, categorias

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Nota de conexión a la base de datos: {e}")

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

@app.get("/")
def ruta_raiz():
    return {
        "aplicacion": "Presupuesto Estudiantil API",
        "estado": "En línea 🚀",
        "documentacion": "/docs",
        "tarea": "Manejo de acceso (Tarea 1 - IHC)"
    }
