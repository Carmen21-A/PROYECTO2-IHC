from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas

#crea el grupo de endpoints de categorías, que vivirán en /categorias.
router = APIRouter(prefix="/categorias", tags=["Categorías"])
#endpoint de tipo GET. "" es la dirección dentro del router. response_model=List[schemas.CategoriaOut] define el formato de la respuesta: una lista (List) de objetos con la forma de CategoriaOut
@router.get("", response_model=List[schemas.CategoriaOut])
#listar_categorias recibe una conexión a la base de datos, que le da get_db, para poder consultar las categorías.
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
