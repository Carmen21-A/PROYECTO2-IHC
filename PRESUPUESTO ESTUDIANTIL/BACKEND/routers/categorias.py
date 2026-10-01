from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("", response_model=List[schemas.CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).all()
    if not categorias:
        return [
            {"id": 1, "nombre": "Comida y Almuerzo", "tipo": "gasto", "icono": "utensils"},
            {"id": 2, "nombre": "Transporte", "tipo": "gasto", "icono": "bus"},
            {"id": 3, "nombre": "Libros y Copias", "tipo": "gasto", "icono": "book-open"},
            {"id": 4, "nombre": "Ocio y Salidas", "tipo": "gasto", "icono": "coffee"},
            {"id": 5, "nombre": "Beca Mensual", "tipo": "ingreso", "icono": "award"},
            {"id": 6, "nombre": "Apoyo Familiar", "tipo": "ingreso", "icono": "heart"},
            {"id": 7, "nombre": "Ingresos", "tipo": "ingreso", "icono": "dollar-sign"}
        ]
    return categorias
