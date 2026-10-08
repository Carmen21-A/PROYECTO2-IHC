from pydantic import BaseModel
from typing import Optional, List

class UsuarioRegistro(BaseModel):
    nombre: str
    email: str
    password: str

class UsuarioLogin(BaseModel):
    email: str
    password: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    es_demo: bool = False

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    token: str
    usuario: UsuarioOut

class SolicitarCodigo(BaseModel):
    email: str

class VerificarCodigo(BaseModel):
    email: str
    codigo: str

class RestablecerPassword(BaseModel):
    email: str
    codigo: str
    nueva_password: str

class MovimientoCreate(BaseModel):
    descripcion: str
    categoria: Optional[str] = "General"
    monto: float
    tipo: Optional[str] = "gasto"
    fecha: Optional[str] = None
    estado: Optional[str] = "pendiente"

class MovimientoUpdate(BaseModel):
    descripcion: Optional[str] = None
    monto: Optional[float] = None
    fecha: Optional[str] = None

class MovimientoOut(BaseModel):
    id: int
    descripcion: str
    categoria: str
    monto: float
    tipo: str
    fecha: str
    estado: str = "pendiente"

    class Config:
        from_attributes = True

class ResumenFinanciero(BaseModel):
    saldo_disponible: float
    ingresos_del_mes: float
    gastos_del_mes: float
    movimientos: List[MovimientoOut]

class CategoriaOut(BaseModel):
    id: int
    nombre: str
    tipo: str
    icono: str

    class Config:
        from_attributes = True
